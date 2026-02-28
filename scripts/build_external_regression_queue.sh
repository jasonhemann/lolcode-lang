#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CANDIDATES_TSV="$ROOT_DIR/corpus/tier2/CANDIDATE_REPOS.tsv"
OUT_DIR="$ROOT_DIR/corpus/research/external_issues"
RAW_DIR="$OUT_DIR/raw"
WAVE_SIZE="${WAVE_SIZE:-10}"

mkdir -p "$OUT_DIR" "$RAW_DIR"

if ! command -v gh >/dev/null 2>&1; then
  echo "error: gh CLI not found" >&2
  echo "install GitHub CLI and run: gh auth login" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq not found" >&2
  exit 1
fi

if ! [[ "$WAVE_SIZE" =~ ^[0-9]+$ ]] || [ "$WAVE_SIZE" -le 0 ]; then
  echo "error: WAVE_SIZE must be a positive integer" >&2
  exit 1
fi

all_jsonl="$OUT_DIR/all_items.jsonl"
: > "$all_jsonl"

echo "building external issue/pr queue from candidate repos..."

while IFS=$'\t' read -r tier label repo kind oracle_priority corpus_priority source status; do
  [ -n "${tier:-}" ] || continue
  case "$tier" in
    \#*) continue ;;
  esac
  [ -n "${repo:-}" ] || continue
  [ -n "${label:-}" ] || continue

  issues_pages="$RAW_DIR/${label}.issues.pages.json"
  pulls_pages="$RAW_DIR/${label}.pulls.pages.json"
  issues_json="$RAW_DIR/${label}.issues.json"
  pulls_json="$RAW_DIR/${label}.pulls.json"

  echo "  - syncing $repo"
  if ! gh api --paginate --slurp "repos/$repo/issues?state=all&per_page=100" > "$issues_pages" 2>/dev/null; then
    echo "    warning: failed to fetch issues for $repo" >&2
    echo "[]" > "$issues_pages"
  fi

  if ! gh api --paginate --slurp "repos/$repo/pulls?state=all&per_page=100" > "$pulls_pages" 2>/dev/null; then
    echo "    warning: failed to fetch pulls for $repo" >&2
    echo "[]" > "$pulls_pages"
  fi

  jq '
    add
    | map(select(has("pull_request") | not))
    | map({
        item_type: "issue",
        number,
        title,
        state,
        created_at,
        updated_at,
        closed_at,
        comments,
        labels: [.labels[]?.name],
        url: .html_url
      })
    | sort_by(.number)
  ' "$issues_pages" > "$issues_json"

  jq '
    add
    | map({
        item_type: "pr",
        number,
        title,
        state,
        created_at,
        updated_at,
        closed_at,
        merged_at,
        draft,
        comments,
        labels: [.labels[]?.name],
        url: .html_url
      })
    | sort_by(.number)
  ' "$pulls_pages" > "$pulls_json"

  jq -c \
    --arg repo "$repo" \
    --arg label "$label" \
    --arg tier "$tier" \
    --arg kind "$kind" \
    '.[] | . + {repo: $repo, label: $label, tier: $tier, repo_kind: $kind, source: "github"}' \
    "$issues_json" >> "$all_jsonl"

  jq -c \
    --arg repo "$repo" \
    --arg label "$label" \
    --arg tier "$tier" \
    --arg kind "$kind" \
    '.[] | . + {repo: $repo, label: $label, tier: $tier, repo_kind: $kind, source: "github"}' \
    "$pulls_json" >> "$all_jsonl"
done < "$CANDIDATES_TSV"

all_items_json="$OUT_DIR/all_items.json"
ranked_all_json="$OUT_DIR/ranked_all_items.json"
candidate_json="$OUT_DIR/candidate_repros.json"
ranked_candidate_json="$OUT_DIR/candidate_repros_ranked.json"
candidate_tsv="$OUT_DIR/candidate_repros.tsv"
queue_md="$OUT_DIR/QUEUE.md"

jq -s '.' "$all_jsonl" > "$all_items_json"

jq '
  def t: (.title // "" | ascii_downcase);
  def cat:
    if (t | test("segfault|sigsev|buffer overflow|null pointer|double free|out of bounds|abort|panic|crash|realloc|overrun")) then "runtime-safety"
    elif (t | test("loop|scope|parse|parser|lexer|string|numbar|numbr|mkay|variadic|cast|type|slot|bukkit|switch|both saem|function|recurs|interpolation|unicode|\\bit\\b|tldr|btw|kthxbye|hai|literal|implicit")) then "language"
    elif (t | test("build|install|cmake|make error|windows|python|doxygen|appveyor|readline|compile|compilation")) then "tooling"
    elif (t | test("wishlist|suggestion|feature|support\\?|socket|file i/o|pipe library|multithreading|standalone|embed")) then "feature-request"
    elif (t | test("readme|license|link|docs|typo|namespace|cleanup|tests?")) then "docs"
    else "unknown"
    end;
  def score:
    (if cat == "runtime-safety" then 100
     elif cat == "language" then 80
     elif cat == "unknown" then 40
     elif cat == "tooling" then 15
     elif cat == "docs" then 10
     else 5 end)
    + (if .state == "open" then 10 else 0 end)
    + (if .repo == "justinmeza/lci" then 10 else 0 end);
  map(. + {
        category: cat,
        score: score,
        candidate_repro: (cat == "runtime-safety" or cat == "language")
      })
  | sort_by(-.score, .repo, .item_type, .number)
' "$all_items_json" > "$ranked_all_json"

jq '[ .[] | select(.candidate_repro) ]' "$ranked_all_json" > "$candidate_json"

jq --argjson wave_size "$WAVE_SIZE" '
  to_entries
  | map(.value + {
      rank: (.key + 1),
      wave: ((.key / $wave_size | floor) + 1)
    })
' "$candidate_json" > "$ranked_candidate_json"

jq -r '
  .[]
  | [.rank, .wave, .repo, .label, .item_type, .number, .state, .category, .score, .title, .url]
  | @tsv
' "$ranked_candidate_json" > "$candidate_tsv"

generated_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
total_items="$(jq 'length' "$all_items_json")"
candidate_items="$(jq 'length' "$ranked_candidate_json")"
max_wave="$(jq 'if length == 0 then 0 else max_by(.wave).wave end' "$ranked_candidate_json")"

{
  echo "# External Regression Queue"
  echo
  echo "- Generated at: $generated_at"
  echo "- Source catalog: \`corpus/tier2/CANDIDATE_REPOS.tsv\`"
  echo "- Total issues+PR items collected: $total_items"
  echo "- Candidate reproducible regression items: $candidate_items"
  echo "- Wave size: $WAVE_SIZE"
  echo "- Total waves currently: $max_wave"
  echo
  echo "## How To Process All Items"
  echo
  echo "1. Iterate \`wave = 1..$max_wave\` in \`candidate_repros.tsv\`."
  echo "2. For each row, create a minimal fixture/test + expected behavior."
  echo "3. Classify result in triage as \`fixed-here\`, \`known-divergence\`, \`spec-ambiguous\`, or \`out-of-spec\`."
  echo
  echo "## Wave Counts"
  echo
  jq -r '
    group_by(.wave)
    | .[]
    | "- Wave \((.[0].wave)): \(length) items"
  ' "$ranked_candidate_json"
  echo
  echo "## Top 30 Candidates"
  echo
  jq -r '
    .[:30]
    | .[]
    | "- [rank \(.rank), wave \(.wave)] \(.repo) \(.item_type) #\(.number): [\(.title)](\(.url)) [\(.category), score=\(.score)]"
  ' "$ranked_candidate_json"
  echo
  echo "## Output Files"
  echo
  echo "- \`$all_items_json\`"
  echo "- \`$ranked_all_json\`"
  echo "- \`$candidate_json\`"
  echo "- \`$ranked_candidate_json\`"
  echo "- \`$candidate_tsv\`"
} > "$queue_md"

echo "done."
echo "  $queue_md"
echo "  $candidate_tsv"

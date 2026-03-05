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
all_jsonl_tmp="${TMPDIR:-/tmp}/build-external-queue.$$.jsonl"
tmp_prefix="${TMPDIR:-/tmp}/build-external-queue.$$"
: > "$all_jsonl_tmp"
fetch_success_count=0
fetch_failure_count=0

cleanup() {
  rm -f "$all_jsonl_tmp"
  rm -f "${tmp_prefix}".*
}
trap cleanup EXIT

echo "building external issue/pr queue from candidate repos..."

while IFS=$'\t' read -r tier label repo kind oracle_priority corpus_priority source status; do
  [ -n "${tier:-}" ] || continue
  case "$tier" in
    \#*) continue ;;
  esac
  [ -n "${repo:-}" ] || continue
  [ -n "${label:-}" ] || continue

  issues_pages_raw="$RAW_DIR/${label}.issues.pages.json"
  pulls_pages_raw="$RAW_DIR/${label}.pulls.pages.json"
  commits_pages_raw="$RAW_DIR/${label}.commits.pages.json"
  issues_json_raw="$RAW_DIR/${label}.issues.json"
  pulls_json_raw="$RAW_DIR/${label}.pulls.json"
  commits_json_raw="$RAW_DIR/${label}.commits.json"
  issues_pages="${tmp_prefix}.${label}.issues.pages.json"
  pulls_pages="${tmp_prefix}.${label}.pulls.pages.json"
  commits_pages="${tmp_prefix}.${label}.commits.pages.json"
  issues_json="${tmp_prefix}.${label}.issues.json"
  pulls_json="${tmp_prefix}.${label}.pulls.json"
  commits_json="${tmp_prefix}.${label}.commits.json"
  issues_fetch_ok=0
  pulls_fetch_ok=0
  commits_fetch_ok=0

  echo "  - syncing $repo"
  if gh api --paginate --slurp "repos/$repo/issues?state=all&per_page=100" > "$issues_pages" 2>/dev/null; then
    issues_fetch_ok=1
    fetch_success_count=$((fetch_success_count + 1))
    cp "$issues_pages" "$issues_pages_raw"
  else
    fetch_failure_count=$((fetch_failure_count + 1))
    echo "    warning: failed to fetch issues for $repo" >&2
    if [ -s "$issues_pages_raw" ]; then
      echo "    using cached issues pages for $repo" >&2
      cp "$issues_pages_raw" "$issues_pages"
    else
      echo "[]" > "$issues_pages"
    fi
  fi

  if gh api --paginate --slurp "repos/$repo/pulls?state=all&per_page=100" > "$pulls_pages" 2>/dev/null; then
    pulls_fetch_ok=1
    fetch_success_count=$((fetch_success_count + 1))
    cp "$pulls_pages" "$pulls_pages_raw"
  else
    fetch_failure_count=$((fetch_failure_count + 1))
    echo "    warning: failed to fetch pulls for $repo" >&2
    if [ -s "$pulls_pages_raw" ]; then
      echo "    using cached pulls pages for $repo" >&2
      cp "$pulls_pages_raw" "$pulls_pages"
    else
      echo "[]" > "$pulls_pages"
    fi
  fi

  if gh api --paginate --slurp "repos/$repo/commits?per_page=100" > "$commits_pages" 2>/dev/null; then
    commits_fetch_ok=1
    fetch_success_count=$((fetch_success_count + 1))
    cp "$commits_pages" "$commits_pages_raw"
  else
    fetch_failure_count=$((fetch_failure_count + 1))
    echo "    warning: failed to fetch commits for $repo" >&2
    if [ -s "$commits_pages_raw" ]; then
      echo "    using cached commits pages for $repo" >&2
      cp "$commits_pages_raw" "$commits_pages"
    else
      echo "[]" > "$commits_pages"
    fi
  fi

  jq '
    (add // [])
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
  if [ "$issues_fetch_ok" -eq 1 ]; then
    cp "$issues_json" "$issues_json_raw"
  fi

  jq '
    (add // [])
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
  if [ "$pulls_fetch_ok" -eq 1 ]; then
    cp "$pulls_json" "$pulls_json_raw"
  fi

  jq '
    (add // [])
    | map({
        item_type: "commit",
        number: .sha,
        title: (.commit.message // "" | split("\n")[0]),
        state: "closed",
        created_at: (.commit.author.date // null),
        updated_at: (.commit.author.date // null),
        closed_at: (.commit.author.date // null),
        comments: 0,
        labels: [],
        url: .html_url
      })
    | sort_by(.created_at)
  ' "$commits_pages" > "$commits_json"
  if [ "$commits_fetch_ok" -eq 1 ]; then
    cp "$commits_json" "$commits_json_raw"
  fi

  jq -c \
    --arg repo "$repo" \
    --arg label "$label" \
    --arg tier "$tier" \
    --arg kind "$kind" \
    '.[] | . + {repo: $repo, label: $label, tier: $tier, repo_kind: $kind, source: "github"}' \
    "$issues_json" >> "$all_jsonl_tmp"

  jq -c \
    --arg repo "$repo" \
    --arg label "$label" \
    --arg tier "$tier" \
    --arg kind "$kind" \
    '.[] | . + {repo: $repo, label: $label, tier: $tier, repo_kind: $kind, source: "github"}' \
    "$pulls_json" >> "$all_jsonl_tmp"

  jq -c \
    --arg repo "$repo" \
    --arg label "$label" \
    --arg tier "$tier" \
    --arg kind "$kind" \
    '.[] | . + {repo: $repo, label: $label, tier: $tier, repo_kind: $kind, source: "github"}' \
    "$commits_json" >> "$all_jsonl_tmp"
done < "$CANDIDATES_TSV"

if [ "$fetch_success_count" -eq 0 ]; then
  existing_all_items_json="$OUT_DIR/all_items.json"
  if [ -s "$existing_all_items_json" ] && [ "$(jq 'length' "$existing_all_items_json" 2>/dev/null || echo 0)" -gt 0 ]; then
    echo "warning: no external data fetched; reusing existing snapshot from $existing_all_items_json" >&2
    jq -c '.[]' "$existing_all_items_json" > "$all_jsonl_tmp"
  else
    echo "error: no external data fetched (gh auth/network likely unavailable)." >&2
    echo "preserving existing queue outputs under $OUT_DIR" >&2
    exit 2
  fi
fi

all_items_json="$OUT_DIR/all_items.json"
ranked_all_json="$OUT_DIR/ranked_all_items.json"
candidate_json="$OUT_DIR/candidate_repros.json"
ranked_candidate_json="$OUT_DIR/candidate_repros_ranked.json"
candidate_tsv="$OUT_DIR/candidate_repros.tsv"
queue_md="$OUT_DIR/QUEUE.md"

cp "$all_jsonl_tmp" "$all_jsonl"
jq -s '.' "$all_jsonl_tmp" > "$all_items_json"

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
  def scope:
    if (.repo_kind == "extension")
      or (t | test("can has|string\\x27z|stdio|stdlib|socks|raylib|socket|file i/o|pipe library|wazzup|buhbye|color")) then "extension"
    elif (cat == "runtime-safety" or cat == "language") then "core-1.2-1.3"
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
    + (if .repo == "justinmeza/lci" then 10 else 0 end)
    + (if scope == "core-1.2-1.3" then 5 elif scope == "extension" then -30 else 0 end);
  map(. + {
        category: cat,
        spec_scope: scope,
        score: score,
        candidate_repro: ((cat == "runtime-safety" or cat == "language")
                          and scope != "extension")
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
  | [.rank, .wave, .repo, .label, .item_type, .number, .state, .category, .spec_scope, .score, .title, .url]
  | @tsv
' "$ranked_candidate_json" > "$candidate_tsv"

generated_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
total_items="$(jq 'length' "$all_items_json")"
candidate_items="$(jq 'length' "$ranked_candidate_json")"
core_items="$(jq '[.[] | select(.spec_scope == "core-1.2-1.3")] | length' "$ranked_all_json")"
extension_items="$(jq '[.[] | select(.spec_scope == "extension")] | length' "$ranked_all_json")"
unknown_scope_items="$(jq '[.[] | select(.spec_scope == "unknown")] | length' "$ranked_all_json")"
core_candidate_items="$(jq '[.[] | select(.spec_scope == "core-1.2-1.3")] | length' "$ranked_candidate_json")"
max_wave="$(jq 'if length == 0 then 0 else max_by(.wave).wave end' "$ranked_candidate_json")"

{
  echo "# External Regression Queue"
  echo
  echo "- Generated at: $generated_at"
  echo "- Source catalog: \`corpus/tier2/CANDIDATE_REPOS.tsv\`"
  echo "- Total issues+PR items collected: $total_items"
  echo "- Scope counts (all items): core=$core_items, extension=$extension_items, unknown=$unknown_scope_items"
  echo "- Candidate reproducible regression items: $candidate_items"
  echo "- Candidate core-1.2/1.3 items: $core_candidate_items"
  echo "- Wave size: $WAVE_SIZE"
  echo "- Total waves currently: $max_wave"
  if [ "$fetch_failure_count" -gt 0 ]; then
    echo "- Warning: partial fetch failures during sync: $fetch_failure_count"
  fi
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
    | "- [rank \(.rank), wave \(.wave)] \(.repo) \(.item_type) #\(.number): [\(.title)](\(.url)) [\(.category), \(.spec_scope), score=\(.score)]"
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

#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CATALOG_TSV="$REPO_ROOT/corpus/tier2/CANDIDATE_REPOS.tsv"
OUT_DIR="$REPO_ROOT/corpus/research/github_language_lolcode"
RAW_DIR="$OUT_DIR/raw"
TRASH_DIR="${CORPUS_TRASH_DIR:-$REPO_ROOT/.trash}"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/github-lolcode-search.XXXXXX")"

CODE_QUERY="${CODE_QUERY:-language:LOLCODE}"
REPO_QUERY="${REPO_QUERY:-language:LOLCODE}"
CODE_PAGE_LIMIT="${CODE_PAGE_LIMIT:-10}"
REPO_PAGE_LIMIT="${REPO_PAGE_LIMIT:-10}"
TOP_NEW_LIMIT="${TOP_NEW_LIMIT:-100}"
SELF_REPO=""

usage() {
  cat <<'EOF'
Usage:
  ./scripts/sync_github_language_lolcode.sh
  ./scripts/sync_github_language_lolcode.sh --code-page-limit 15 --repo-page-limit 10
  ./scripts/sync_github_language_lolcode.sh --code-query 'language:LOLCODE path:examples'

Outputs:
  corpus/research/github_language_lolcode/repo_search.json
  corpus/research/github_language_lolcode/code_hits.json
  corpus/research/github_language_lolcode/repos.json
  corpus/research/github_language_lolcode/repos.tsv
  corpus/research/github_language_lolcode/new_repos_to_review.tsv
  corpus/research/github_language_lolcode/summary.json
  corpus/research/github_language_lolcode/REPORT.md

Notes:
  - This is a discovery/evidence feed, not a strict conformance oracle.
  - GitHub search APIs can cap deep pagination; summary.json reports truncation risk.
EOF
}

trash_path() {
  local path="$1"
  [ -e "$path" ] || return 0

  if ! command -v trash >/dev/null 2>&1; then
    echo "Missing required command: trash" >&2
    return 1
  fi

  mkdir -p "$TRASH_DIR"
  if command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
    sudo trash --trash-dir "$TRASH_DIR" "$path" || trash --trash-dir "$TRASH_DIR" "$path"
  else
    trash --trash-dir "$TRASH_DIR" "$path"
  fi
}

cleanup_tmp() {
  trash_path "$TMP_DIR" || true
}
trap cleanup_tmp EXIT

require_cmds() {
  local missing=0
  for cmd in gh jq awk sed rg sort date mktemp trash; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "Missing required command: $cmd" >&2
      missing=1
    fi
  done
  [ "$missing" -eq 0 ]
}

urlencode() {
  local raw="$1"
  jq -nr --arg s "$raw" '$s|@uri'
}

is_posint() {
  [[ "$1" =~ ^[0-9]+$ ]] && [ "$1" -gt 0 ]
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --code-query)
      [ "$#" -lt 2 ] && { echo "Missing value for --code-query" >&2; exit 2; }
      CODE_QUERY="$2"
      shift 2
      ;;
    --repo-query)
      [ "$#" -lt 2 ] && { echo "Missing value for --repo-query" >&2; exit 2; }
      REPO_QUERY="$2"
      shift 2
      ;;
    --code-page-limit)
      [ "$#" -lt 2 ] && { echo "Missing value for --code-page-limit" >&2; exit 2; }
      CODE_PAGE_LIMIT="$2"
      shift 2
      ;;
    --repo-page-limit)
      [ "$#" -lt 2 ] && { echo "Missing value for --repo-page-limit" >&2; exit 2; }
      REPO_PAGE_LIMIT="$2"
      shift 2
      ;;
    --top-new-limit)
      [ "$#" -lt 2 ] && { echo "Missing value for --top-new-limit" >&2; exit 2; }
      TOP_NEW_LIMIT="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

require_cmds || exit 1

is_posint "$CODE_PAGE_LIMIT" || { echo "--code-page-limit must be a positive integer" >&2; exit 2; }
is_posint "$REPO_PAGE_LIMIT" || { echo "--repo-page-limit must be a positive integer" >&2; exit 2; }
is_posint "$TOP_NEW_LIMIT" || { echo "--top-new-limit must be a positive integer" >&2; exit 2; }

mkdir -p "$OUT_DIR" "$RAW_DIR"

if remote_url="$(git config --get remote.origin.url 2>/dev/null || true)"; then
  if [[ "$remote_url" =~ github\.com[:/]([^/]+/[^/.]+)(\.git)?$ ]]; then
    SELF_REPO="${BASH_REMATCH[1]}"
  fi
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "error: gh auth unavailable. Run: gh auth login" >&2
  exit 1
fi

fetch_search() {
  local kind="$1"
  local query="$2"
  local page_limit="$3"
  local raw_prefix="$4"
  local out_items="$5"
  local out_meta="$6"

  local page=1
  local pages_fetched=0
  local total_count=0
  local last_count=0
  local used_cache=0
  local fetched_live=0
  local pages_jsonl="$TMP_DIR/${raw_prefix}.pages.jsonl"
  : > "$pages_jsonl"

  while [ "$page" -le "$page_limit" ]; do
    local page_tmp="$TMP_DIR/${raw_prefix}.page${page}.json"
    local raw_page="$RAW_DIR/${raw_prefix}.page$(printf '%03d' "$page").json"
    local query_encoded
    local endpoint
    query_encoded="$(urlencode "$query")"
    endpoint="https://api.github.com/search/${kind}?q=${query_encoded}&per_page=100&page=${page}"

    if gh api -X GET "$endpoint" > "$page_tmp" 2>/dev/null; then
      fetched_live=1
      cp "$page_tmp" "$raw_page"
    elif [ -s "$raw_page" ]; then
      used_cache=1
      cp "$raw_page" "$page_tmp"
    else
      if [ "$page" -eq 1 ]; then
        echo "error: failed to fetch ${kind} page 1 and no cache exists for ${raw_prefix}" >&2
        return 1
      fi
      break
    fi

    if [ "$page" -eq 1 ]; then
      total_count="$(jq -r '.total_count // 0' "$page_tmp")"
    fi

    last_count="$(jq -r '.items | length' "$page_tmp")"
    if [ "$last_count" -eq 0 ]; then
      break
    fi

    pages_fetched="$page"
    cat "$page_tmp" >> "$pages_jsonl"
    printf '\n' >> "$pages_jsonl"

    if [ "$last_count" -lt 100 ]; then
      break
    fi

    page=$((page + 1))
  done

  if [ "$pages_fetched" -eq 0 ]; then
    printf '[]\n' > "$out_items"
  else
    jq -s 'map(.items // []) | add // []' "$pages_jsonl" > "$out_items"
  fi

  jq -n \
    --arg kind "$kind" \
    --arg query "$query" \
    --argjson page_limit "$page_limit" \
    --argjson pages_fetched "$pages_fetched" \
    --argjson total_count "$total_count" \
    --argjson last_page_count "$last_count" \
    --argjson fetched_live "$fetched_live" \
    --argjson used_cache "$used_cache" \
    '{
      kind: $kind,
      query: $query,
      page_limit: $page_limit,
      pages_fetched: $pages_fetched,
      total_count: $total_count,
      last_page_count: $last_page_count,
      fetched_live: ($fetched_live == 1),
      used_cache: ($used_cache == 1),
      likely_truncated: (($pages_fetched == $page_limit) and ($last_page_count == 100) and ($total_count > ($pages_fetched * 100)))
    }' > "$out_meta"
}

code_items_json="$TMP_DIR/code-items.json"
code_meta_json="$TMP_DIR/code-meta.json"
repo_items_json="$TMP_DIR/repo-items.json"
repo_meta_json="$TMP_DIR/repo-meta.json"

fetch_search "code" "$CODE_QUERY" "$CODE_PAGE_LIMIT" "code" "$code_items_json" "$code_meta_json"
fetch_search "repositories" "$REPO_QUERY" "$REPO_PAGE_LIMIT" "repos" "$repo_items_json" "$repo_meta_json"

repo_search_json="$OUT_DIR/repo_search.json"
code_hits_json="$OUT_DIR/code_hits.json"
repos_json="$OUT_DIR/repos.json"
repos_tsv="$OUT_DIR/repos.tsv"
new_repos_tsv="$OUT_DIR/new_repos_to_review.tsv"
summary_json="$OUT_DIR/summary.json"
report_md="$OUT_DIR/REPORT.md"

jq '
  map({
    repo: .full_name,
    stars: (.stargazers_count // 0),
    forks: (.forks_count // 0),
    watchers: (.watchers_count // 0),
    open_issues: (.open_issues_count // 0),
    created_at,
    updated_at,
    pushed_at,
    archived: (.archived // false),
    html_url
  })
  | unique_by(.repo)
  | sort_by(.repo)
' "$repo_items_json" > "$repo_search_json"

jq --arg self_repo "$SELF_REPO" '
  map({
    repo: .repository.full_name,
    path,
    sha,
    url: .html_url,
    score: (.score // 0)
  })
  | map(select(($self_repo == "") or (.repo != $self_repo)))
  | unique_by(.repo, .path, .sha)
  | sort_by(.repo, .path, .sha)
' "$code_items_json" > "$code_hits_json"

catalog_repos_json="$TMP_DIR/catalog-repos.json"
awk 'NF && $1 !~ /^#/ {print $3}' "$CATALOG_TSV" \
  | sort -u \
  | jq -R . \
  | jq -s . > "$catalog_repos_json"

code_repos_json="$TMP_DIR/code-repos.json"
jq '
  group_by(.repo)
  | map({
      repo: .[0].repo,
      code_hit_count: length,
      sample_paths: ((map(.path) | unique | sort)[:5]),
      sample_url: .[0].url
    })
  | sort_by(-.code_hit_count, .repo)
' "$code_hits_json" > "$code_repos_json"

jq -n \
  --slurpfile repo_search "$repo_search_json" \
  --slurpfile code_repos "$code_repos_json" \
  --slurpfile catalog "$catalog_repos_json" \
  '
  def index_by_repo(xs):
    reduce xs[] as $x ({}; .[$x.repo] = $x);

  ($repo_search[0]) as $repo_rows
  | ($code_repos[0]) as $code_rows
  | ($catalog[0]) as $catalog_rows
  | (index_by_repo($repo_rows)) as $repo_ix
  | (index_by_repo($code_rows)) as $code_ix
  | ((($repo_rows | map(.repo)) + ($code_rows | map(.repo))) | unique | sort) as $all_repos
  | $all_repos
  | map(
      . as $name
      | {
          repo: $name,
          in_catalog: ($catalog_rows | index($name) != null),
          in_repo_search: ($repo_ix[$name] != null),
          in_code_search: ($code_ix[$name] != null),
          code_hit_count: (($code_ix[$name].code_hit_count) // 0),
          stars: (($repo_ix[$name].stars) // 0),
          updated_at: (($repo_ix[$name].updated_at) // null),
          pushed_at: (($repo_ix[$name].pushed_at) // null),
          archived: (($repo_ix[$name].archived) // false),
          html_url: (($repo_ix[$name].html_url) // ("https://github.com/" + $name)),
          sample_paths: (($code_ix[$name].sample_paths) // [])
        }
    )
  | sort_by(.in_catalog, -.code_hit_count, -.stars, .repo)
' > "$repos_json"

{
  printf 'repo\tin_catalog\tin_repo_search\tin_code_search\tcode_hit_count\tstars\tarchived\tupdated_at\thtml_url\n'
  jq -r '.[] | [
      .repo,
      (if .in_catalog then "yes" else "no" end),
      (if .in_repo_search then "yes" else "no" end),
      (if .in_code_search then "yes" else "no" end),
      (.code_hit_count | tostring),
      (.stars | tostring),
      (if .archived then "yes" else "no" end),
      (.updated_at // ""),
      .html_url
    ] | @tsv' "$repos_json"
} > "$repos_tsv"

{
  printf 'tier\tlabel\trepo\tkind\toracle_priority\tcorpus_priority\tsource\tstatus\tcode_hit_count\tstars\thtml_url\n'
  jq -r --arg source_tag "github-language-lolcode-$(date -u +%F)" '
    [ .[]
      | select(.in_catalog | not)
      | select(($self_repo == "") or (.repo != $self_repo))
      | . + {label: (.repo | ascii_downcase | gsub("[^a-z0-9]+"; "-"))}
    ]
    | .[]
    | [
        "tier2",
        .label,
        .repo,
        "corpus",
        "P3",
        "P2",
        $source_tag,
        "discovered",
        (.code_hit_count | tostring),
        (.stars | tostring),
        .html_url
      ] | @tsv
  ' --arg self_repo "$SELF_REPO" "$repos_json"
} > "$new_repos_tsv"

jq -n \
  --arg generated_at "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
  --slurpfile code_meta "$code_meta_json" \
  --slurpfile repo_meta "$repo_meta_json" \
  --argjson repo_total "$(jq 'length' "$repos_json")" \
  --argjson in_catalog_total "$(jq '[.[] | select(.in_catalog)] | length' "$repos_json")" \
  --argjson new_repo_total "$(jq '[.[] | select(.in_catalog | not)] | length' "$repos_json")" \
  --argjson code_hit_total "$(jq 'length' "$code_hits_json")" \
  --argjson top_new_limit "$TOP_NEW_LIMIT" \
  '{
    generated_at: $generated_at,
    code_search: $code_meta[0],
    repo_search: $repo_meta[0],
    capture_gap_possible: (($code_meta[0].total_count // 0) > $code_hit_total),
    totals: {
      repos_combined_unique: $repo_total,
      repos_in_catalog: $in_catalog_total,
      repos_new_not_in_catalog: $new_repo_total,
      code_hits: $code_hit_total,
      top_new_limit: $top_new_limit
    }
  }' > "$summary_json"

{
  echo "# GitHub LOLCODE Discovery Snapshot"
  echo
  echo "- Generated: $(jq -r '.generated_at' "$summary_json")"
  echo "- Query (code): \`$(jq -r '.code_search.query' "$summary_json")\`"
  echo "- Query (repos): \`$(jq -r '.repo_search.query' "$summary_json")\`"
  echo "- Combined unique repos: \`$(jq -r '.totals.repos_combined_unique' "$summary_json")\`"
  echo "- Already in catalog: \`$(jq -r '.totals.repos_in_catalog' "$summary_json")\`"
  echo "- New (not in catalog): \`$(jq -r '.totals.repos_new_not_in_catalog' "$summary_json")\`"
  echo "- Code hits captured: \`$(jq -r '.totals.code_hits' "$summary_json")\`"
  echo
  echo "## Search Integrity"
  echo
  echo "- Code search pages fetched: \`$(jq -r '.code_search.pages_fetched' "$summary_json")\`/\`$(jq -r '.code_search.page_limit' "$summary_json")\`"
  echo "- Code search likely truncated: \`$(jq -r '.code_search.likely_truncated' "$summary_json")\`"
  echo "- Code capture gap possible (reported total > captured hits): \`$(jq -r '.capture_gap_possible' "$summary_json")\`"
  echo "- Repo search pages fetched: \`$(jq -r '.repo_search.pages_fetched' "$summary_json")\`/\`$(jq -r '.repo_search.page_limit' "$summary_json")\`"
  echo "- Repo search likely truncated: \`$(jq -r '.repo_search.likely_truncated' "$summary_json")\`"
  echo
  echo "## Top New Repos (Review Queue)"
  echo
  echo "| Repo | Code hits | Stars | Updated | Link |"
  echo "|---|---:|---:|---|---|"
  jq -r --argjson top_n "$TOP_NEW_LIMIT" --arg self_repo "$SELF_REPO" '
    [ .[]
      | select(.in_catalog | not)
      | select(($self_repo == "") or (.repo != $self_repo))
    ]
    | .[:$top_n]
    | .[]
    | "| `\(.repo)` | \(.code_hit_count) | \(.stars) | \(.updated_at // "-") | [repo](\(.html_url)) |"
  ' "$repos_json"
  echo
  echo "## Output Files"
  echo
  echo "- \`corpus/research/github_language_lolcode/repo_search.json\`"
  echo "- \`corpus/research/github_language_lolcode/code_hits.json\`"
  echo "- \`corpus/research/github_language_lolcode/repos.json\`"
  echo "- \`corpus/research/github_language_lolcode/repos.tsv\`"
  echo "- \`corpus/research/github_language_lolcode/new_repos_to_review.tsv\`"
  echo "- \`corpus/research/github_language_lolcode/summary.json\`"
} > "$report_md"

echo "wrote $report_md"
echo "wrote $new_repos_tsv"

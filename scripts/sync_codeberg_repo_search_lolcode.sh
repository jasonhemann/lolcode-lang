#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$REPO_ROOT/corpus/research/codeberg_repo_search_lolcode"
RAW_DIR="$OUT_DIR/raw"
TRASH_DIR="${CORPUS_TRASH_DIR:-$REPO_ROOT/.trash}"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/codeberg-repo-lolcode.XXXXXX")"

QUERY="${QUERY:-lolcode}"
PAGE_LIMIT="${PAGE_LIMIT:-10}"
PER_PAGE="${PER_PAGE:-50}"
TOP_NEW_LIMIT="${TOP_NEW_LIMIT:-100}"

CATALOG_TSV="$REPO_ROOT/corpus/tier2/CANDIDATE_REPOS.tsv"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/sync_codeberg_repo_search_lolcode.sh
  ./scripts/sync_codeberg_repo_search_lolcode.sh --query 'lolcode'

Outputs:
  corpus/research/codeberg_repo_search_lolcode/repo_search.json
  corpus/research/codeberg_repo_search_lolcode/repos.json
  corpus/research/codeberg_repo_search_lolcode/repos.tsv
  corpus/research/codeberg_repo_search_lolcode/new_repos_to_review.tsv
  corpus/research/codeberg_repo_search_lolcode/summary.json
  corpus/research/codeberg_repo_search_lolcode/REPORT.md

Notes:
  - This uses Codeberg's public Forgejo repo-search API.
  - Repo identities are host-qualified as `codeberg:owner/name`.
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
  trash --trash-dir "$TRASH_DIR" "$path"
}

cleanup_tmp() {
  trash_path "$TMP_DIR" || true
}
trap cleanup_tmp EXIT

require_cmds() {
  local missing=0
  for cmd in curl jq awk sed sort date mktemp trash; do
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
    --query)
      [ "$#" -lt 2 ] && { echo "Missing value for --query" >&2; exit 2; }
      QUERY="$2"
      shift 2
      ;;
    --page-limit)
      [ "$#" -lt 2 ] && {
        echo "Missing value for --page-limit" >&2
        exit 2
      }
      PAGE_LIMIT="$2"
      shift 2
      ;;
    --per-page)
      [ "$#" -lt 2 ] && { echo "Missing value for --per-page" >&2; exit 2; }
      PER_PAGE="$2"
      shift 2
      ;;
    --top-new-limit)
      [ "$#" -lt 2 ] && {
        echo "Missing value for --top-new-limit" >&2
        exit 2
      }
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

is_posint "$PAGE_LIMIT" || {
  echo "--page-limit must be a positive integer" >&2
  exit 2
}
is_posint "$PER_PAGE" || {
  echo "--per-page must be a positive integer" >&2
  exit 2
}
is_posint "$TOP_NEW_LIMIT" || {
  echo "--top-new-limit must be a positive integer" >&2
  exit 2
}

mkdir -p "$OUT_DIR" "$RAW_DIR"

fetch_repo_search() {
  local page=1
  local pages_fetched=0
  local last_count=0
  local used_cache=0
  local fetched_live=0
  local pages_jsonl="$TMP_DIR/repos.pages.jsonl"
  : > "$pages_jsonl"

  while [ "$page" -le "$PAGE_LIMIT" ]; do
    local page_tmp="$TMP_DIR/repos.page${page}.json"
    local raw_page="$RAW_DIR/repos.page$(printf '%03d' "$page").json"
    local query_encoded endpoint

    query_encoded="$(urlencode "$QUERY")"
    endpoint="https://codeberg.org/api/v1/repos/search?q=${query_encoded}&limit=${PER_PAGE}&page=${page}"

    if curl -fsSL --max-time 30 "$endpoint" > "$page_tmp" 2>/dev/null; then
      fetched_live=1
      cp "$page_tmp" "$raw_page"
    elif [ -s "$raw_page" ]; then
      used_cache=1
      cp "$raw_page" "$page_tmp"
    else
      if [ "$page" -eq 1 ]; then
        echo "error: failed to fetch Codeberg page 1 and no cache exists" >&2
        return 1
      fi
      break
    fi

    last_count="$(jq -r '.data | length' "$page_tmp")"
    if [ "$last_count" -eq 0 ]; then
      break
    fi

    pages_fetched="$page"
    cat "$page_tmp" >> "$pages_jsonl"
    printf '\n' >> "$pages_jsonl"

    if [ "$last_count" -lt "$PER_PAGE" ]; then
      break
    fi

    page=$((page + 1))
  done

  if [ "$pages_fetched" -eq 0 ]; then
    printf '[]\n' > "$TMP_DIR/repos.items.json"
  else
    jq -s 'map(.data // []) | add // []' "$pages_jsonl" \
      > "$TMP_DIR/repos.items.json"
  fi

  jq -n \
    --arg query "$QUERY" \
    --argjson page_limit "$PAGE_LIMIT" \
    --argjson per_page "$PER_PAGE" \
    --argjson pages_fetched "$pages_fetched" \
    --argjson last_page_count "$last_count" \
    --argjson fetched_live "$fetched_live" \
    --argjson used_cache "$used_cache" \
    '{
      host: "codeberg",
      kind: "repositories",
      query: $query,
      page_limit: $page_limit,
      per_page: $per_page,
      pages_fetched: $pages_fetched,
      last_page_count: $last_page_count,
      fetched_live: ($fetched_live == 1),
      used_cache: ($used_cache == 1),
      likely_truncated:
        (($pages_fetched == $page_limit)
         and ($last_page_count == $per_page))
    }' > "$TMP_DIR/repos.meta.json"
}

fetch_repo_search

repo_search_json="$OUT_DIR/repo_search.json"
repos_json="$OUT_DIR/repos.json"
repos_tsv="$OUT_DIR/repos.tsv"
new_repos_tsv="$OUT_DIR/new_repos_to_review.tsv"
summary_json="$OUT_DIR/summary.json"
report_md="$OUT_DIR/REPORT.md"
dir_readme="$OUT_DIR/README.md"

jq '
  map({
    host: "codeberg",
    repo_path: .full_name,
    repo: ("codeberg:" + .full_name),
    language: (.language // ""),
    description: (.description // ""),
    stars: (.stars_count // 0),
    forks: (.forks_count // 0),
    watchers: (.watchers_count // 0),
    open_issues: (.open_issues_count // 0),
    archived: (.archived // false),
    created_at: .created_at,
    updated_at: .updated_at,
    pushed_at: (.updated_at // null),
    html_url
  })
  | unique_by(.repo)
  | sort_by(.repo)
' "$TMP_DIR/repos.items.json" > "$repo_search_json"

jq \
  --rawfile catalog_tsv "$CATALOG_TSV" \
  '
  def catalog_repos:
    ($catalog_tsv
     | split("\n")
     | map(select(length > 0))
     | map(select(startswith("#") | not))
     | map(split("\t"))
     | map(select(length >= 3))
     | map(.[2]));

  (catalog_repos) as $catalog
  | map(
      . as $repo
      | $repo + {
        in_candidate_catalog_by_path:
          ($catalog | index($repo.repo_path) != null)
      }
    )
  | sort_by(-.stars, .repo)
' "$repo_search_json" > "$repos_json"

{
  printf 'repo\thost\trepo_path\tlanguage\tstars\tin_candidate_catalog_by_path\thtml_url\n'
  jq -r '
    .[]
    | [
        .repo,
        .host,
        .repo_path,
        .language,
        (.stars | tostring),
        (if .in_candidate_catalog_by_path then "yes" else "no" end),
        .html_url
      ]
    | @tsv
  ' "$repos_json"
} > "$repos_tsv"

{
  printf 'repo\thost\trepo_path\tlanguage\tstars\tsource\tstatus\thtml_url\n'
  jq -r --arg source_tag "codeberg-repo-search-lolcode-$(date -u +%F)" \
    --argjson top_new_limit "$TOP_NEW_LIMIT" '
    [ .[]
      | select(.in_candidate_catalog_by_path | not)
    ]
    | sort_by(-.stars, .repo)
    | .[:$top_new_limit]
    | .[]
    | [
        .repo,
        .host,
        .repo_path,
        .language,
        (.stars | tostring),
        $source_tag,
        "discovered",
        .html_url
      ]
    | @tsv
  ' "$repos_json"
} > "$new_repos_tsv"

jq -n \
  --slurpfile repo_meta "$TMP_DIR/repos.meta.json" \
  --slurpfile repos "$repos_json" \
  --arg generated_at "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
  --arg catalog_path "corpus/tier2/CANDIDATE_REPOS.tsv" \
  '{
    generated_at: $generated_at,
    repo_search: $repo_meta[0],
    inputs: {
      candidate_catalog: $catalog_path
    },
    totals: {
      repos_seen: ($repos[0] | length),
      repos_in_candidate_catalog_by_path:
        ([ $repos[0][]
           | select(.in_candidate_catalog_by_path) ] | length),
      repos_not_in_candidate_catalog_by_path:
        ([ $repos[0][]
           | select(.in_candidate_catalog_by_path | not) ] | length)
    }
  }' > "$summary_json"

{
  echo '# Codeberg Broad `lolcode` Repository Search Snapshot'
  echo
  printf -- '- Generated: %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  printf -- '- Query: `%s`\n' "$QUERY"
  echo '- Search mode: Codeberg public repo-search API'
  echo '- Repo identities are host-qualified as `codeberg:owner/name`'
  echo
  echo '## Totals'
  echo
  printf -- '- Repos seen: `%s`\n' \
    "$(jq -r '.totals.repos_seen' "$summary_json")"
  printf -- '- Path matches already in candidate catalog: `%s`\n' \
    "$(jq -r '.totals.repos_in_candidate_catalog_by_path' "$summary_json")"
  printf -- '- New vs candidate catalog: `%s`\n' \
    "$(jq -r '.totals.repos_not_in_candidate_catalog_by_path' \
      "$summary_json")"
  echo
  echo '## Notes'
  echo
  echo '- This is a non-GitHub discovery lane.'
  echo '- Host-qualified repo IDs avoid cross-forge collisions.'
  echo '- Catalog overlap is a simple path match against existing'
  echo '  `owner/name` GitHub-style entries; it is advisory only.'
  echo
  echo '## Output Files'
  echo
  echo '- `corpus/research/codeberg_repo_search_lolcode/repo_search.json`'
  echo '- `corpus/research/codeberg_repo_search_lolcode/repos.json`'
  echo '- `corpus/research/codeberg_repo_search_lolcode/repos.tsv`'
  echo '- `corpus/research/codeberg_repo_search_lolcode/new_repos_to_review.tsv`'
  echo '- `corpus/research/codeberg_repo_search_lolcode/summary.json`'
} > "$report_md"

{
  echo '# Codeberg `lolcode` Repo Search Artifacts'
  echo
  echo 'This directory stores Codeberg discovery results for `q=lolcode`.'
  echo
  echo 'Canonical outputs:'
  echo
  echo '- `REPORT.md`'
  echo '- `repos.json`'
  echo '- `new_repos_to_review.tsv`'
} > "$dir_readme"

echo "wrote $report_md"
echo "wrote $repos_json"
echo "wrote $new_repos_tsv"

#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$REPO_ROOT/corpus/research/github_repo_search_lolcode"
RAW_DIR="$OUT_DIR/raw"
TRASH_DIR="${CORPUS_TRASH_DIR:-$REPO_ROOT/.trash}"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/github-repo-lolcode.XXXXXX")"

QUERY="${QUERY:-lolcode}"
PAGE_LIMIT="${PAGE_LIMIT:-10}"
TOP_NEW_LIMIT="${TOP_NEW_LIMIT:-200}"

CATALOG_TSV="$REPO_ROOT/corpus/tier2/CANDIDATE_REPOS.tsv"
LANGUAGE_REPOS_JSON="$REPO_ROOT/corpus/research/github_language_lolcode/repos.json"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/sync_github_repo_search_lolcode.sh
  ./scripts/sync_github_repo_search_lolcode.sh --query 'lolcode' --page-limit 10

Outputs:
  corpus/research/github_repo_search_lolcode/repo_search.json
  corpus/research/github_repo_search_lolcode/repos.json
  corpus/research/github_repo_search_lolcode/repos.tsv
  corpus/research/github_repo_search_lolcode/new_repos_to_review.tsv
  corpus/research/github_repo_search_lolcode/summary.json
  corpus/research/github_repo_search_lolcode/REPORT.md

Notes:
  - This tracks broad GitHub repository search for `lolcode`, not
    `language:LOLCODE`.
  - It complements `corpus/research/github_language_lolcode/`.
  - This is a discovery/evidence feed, not a conformance oracle.
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
    sudo trash --trash-dir "$TRASH_DIR" "$path" \
      || trash --trash-dir "$TRASH_DIR" "$path"
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
  for cmd in gh jq awk sed sort date mktemp trash; do
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
      [ "$#" -lt 2 ] && { echo "Missing value for --page-limit" >&2; exit 2; }
      PAGE_LIMIT="$2"
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

is_posint "$PAGE_LIMIT" || {
  echo "--page-limit must be a positive integer" >&2
  exit 2
}
is_posint "$TOP_NEW_LIMIT" || {
  echo "--top-new-limit must be a positive integer" >&2
  exit 2
}

mkdir -p "$OUT_DIR" "$RAW_DIR"

if ! gh auth status >/dev/null 2>&1; then
  echo "error: gh auth unavailable. Run: gh auth login" >&2
  exit 1
fi

fetch_repo_search() {
  local page=1
  local pages_fetched=0
  local total_count=0
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
    endpoint="https://api.github.com/search/repositories?q=${query_encoded}&per_page=100&page=${page}"

    if gh api -X GET "$endpoint" > "$page_tmp" 2>/dev/null; then
      fetched_live=1
      cp "$page_tmp" "$raw_page"
    elif [ -s "$raw_page" ]; then
      used_cache=1
      cp "$raw_page" "$page_tmp"
    else
      if [ "$page" -eq 1 ]; then
        echo "error: failed to fetch repository page 1 and no cache exists" >&2
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
    printf '[]\n' > "$TMP_DIR/repos.items.json"
  else
    jq -s 'map(.items // []) | add // []' "$pages_jsonl" \
      > "$TMP_DIR/repos.items.json"
  fi

  jq -n \
    --arg query "$QUERY" \
    --argjson page_limit "$PAGE_LIMIT" \
    --argjson pages_fetched "$pages_fetched" \
    --argjson total_count "$total_count" \
    --argjson last_page_count "$last_count" \
    --argjson fetched_live "$fetched_live" \
    --argjson used_cache "$used_cache" \
    '{
      kind: "repositories",
      query: $query,
      page_limit: $page_limit,
      pages_fetched: $pages_fetched,
      total_count: $total_count,
      last_page_count: $last_page_count,
      fetched_live: ($fetched_live == 1),
      used_cache: ($used_cache == 1),
      likely_truncated:
        (($pages_fetched == $page_limit)
         and ($last_page_count == 100)
         and ($total_count > ($pages_fetched * 100)))
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
    repo: .full_name,
    language: (.language // ""),
    description: (.description // ""),
    stars: (.stargazers_count // 0),
    forks: (.forks_count // 0),
    watchers: (.watchers_count // 0),
    open_issues: (.open_issues_count // 0),
    archived: (.archived // false),
    created_at,
    updated_at,
    pushed_at,
    html_url
  })
  | unique_by(.repo)
  | sort_by(.repo)
' "$TMP_DIR/repos.items.json" > "$repo_search_json"

jq \
  --slurpfile repo_meta "$TMP_DIR/repos.meta.json" \
  --slurpfile language_repos "$LANGUAGE_REPOS_JSON" \
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

  def known_catalog: catalog_repos;
  def known_language_map:
    ($language_repos[0] // [])
    | map({ key: .repo, value: . })
    | from_entries;

  (known_catalog) as $catalog
  | (known_language_map) as $language_map
  | map(
      . as $repo
      | ($language_map[$repo.repo]) as $lang_hit
      | $repo + {
          in_candidate_catalog: ($catalog | index($repo.repo) != null),
          in_language_snapshot: ($lang_hit != null),
          code_hit_count: ($lang_hit.code_hit_count // 0),
          language_snapshot_url: ($lang_hit.html_url // null)
        }
    )
  | sort_by(-.stars, -.code_hit_count, .repo)
' "$repo_search_json" > "$repos_json"

{
  printf 'repo\tlanguage\tstars\tcode_hit_count\tin_candidate_catalog\tin_language_snapshot\thtml_url\n'
  jq -r '
    .[]
    | [
        .repo,
        .language,
        (.stars | tostring),
        (.code_hit_count | tostring),
        (if .in_candidate_catalog then "yes" else "no" end),
        (if .in_language_snapshot then "yes" else "no" end),
        .html_url
      ]
    | @tsv
  ' "$repos_json"
} > "$repos_tsv"

{
  printf 'repo\tlanguage\tstars\tcode_hit_count\tsource\tstatus\thtml_url\n'
  jq -r --arg source_tag "github-repo-search-lolcode-$(date -u +%F)" \
    --argjson top_new_limit "$TOP_NEW_LIMIT" '
    [ .[]
      | select(.in_candidate_catalog | not)
    ]
    | sort_by(-.stars, -.code_hit_count, .repo)
    | .[:$top_new_limit]
    | .[]
    | [
        .repo,
        .language,
        (.stars | tostring),
        (.code_hit_count | tostring),
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
  --arg language_snapshot "corpus/research/github_language_lolcode/repos.json" \
  '{
    generated_at: $generated_at,
    repo_search: $repo_meta[0],
    inputs: {
      candidate_catalog: $catalog_path,
      language_snapshot: $language_snapshot
    },
    totals: {
      repos_seen: ($repos[0] | length),
      repos_in_candidate_catalog:
        ([ $repos[0][] | select(.in_candidate_catalog) ] | length),
      repos_not_in_candidate_catalog:
        ([ $repos[0][] | select(.in_candidate_catalog | not) ] | length),
      repos_also_in_language_snapshot:
        ([ $repos[0][] | select(.in_language_snapshot) ] | length),
      repos_only_in_broad_search:
        ([ $repos[0][]
           | select((.in_candidate_catalog | not)
                    and (.in_language_snapshot | not)) ] | length)
    }
  }' > "$summary_json"

{
  echo '# GitHub Broad `lolcode` Repository Search Snapshot'
  echo
  printf -- '- Generated: %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  printf -- '- Query: `%s`\n' "$QUERY"
  echo '- Search mode: GitHub repository text search, not `language:LOLCODE`'
  echo
  echo '## Totals'
  echo
  printf -- '- Repos seen: `%s`\n' \
    "$(jq -r '.totals.repos_seen' "$summary_json")"
  printf -- '- Already in candidate catalog: `%s`\n' \
    "$(jq -r '.totals.repos_in_candidate_catalog' "$summary_json")"
  printf -- '- New vs candidate catalog: `%s`\n' \
    "$(jq -r '.totals.repos_not_in_candidate_catalog' "$summary_json")"
  printf -- '- Also present in `github_language_lolcode`: `%s`\n' \
    "$(jq -r '.totals.repos_also_in_language_snapshot' "$summary_json")"
  printf -- '- Broad-search-only repos: `%s`\n' \
    "$(jq -r '.totals.repos_only_in_broad_search' "$summary_json")"
  echo
  echo '## Why This Exists'
  echo
  echo '- `language:LOLCODE` discovery is good at finding repos that actually contain'
  echo '  LOLCODE files.'
  echo '- Broad `q=lolcode` repo search finds implementations, editors, docs, and'
  echo '  related tooling that do not necessarily have LOLCODE as the dominant repo'
  echo '  language.'
  echo '- The two feeds overlap, but neither subsumes the other.'
  echo
  echo '## Output Files'
  echo
  echo '- `corpus/research/github_repo_search_lolcode/repo_search.json`'
  echo '- `corpus/research/github_repo_search_lolcode/repos.json`'
  echo '- `corpus/research/github_repo_search_lolcode/repos.tsv`'
  echo '- `corpus/research/github_repo_search_lolcode/new_repos_to_review.tsv`'
  echo '- `corpus/research/github_repo_search_lolcode/summary.json`'
} > "$report_md"

{
  echo '# GitHub Broad `lolcode` Repo Search Artifacts'
  echo
  echo 'This directory stores full-tail GitHub repository search results for'
  echo '`q=lolcode`, enriched with cross-references to:'
  echo
  echo '- `corpus/tier2/CANDIDATE_REPOS.tsv`'
  echo '- `corpus/research/github_language_lolcode/repos.json`'
  echo
  echo 'Use this lane for implementations, editor/tooling repos, docs, and other'
  echo 'projects that mention LOLCODE but are not necessarily dominated by LOLCODE'
  echo 'source files.'
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

#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$REPO_ROOT/corpus/research/github_repo_search_lolcode"
RAW_DIR="$OUT_DIR/enriched_raw"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/github-repo-lolcode-enrich.XXXXXX")"
TRASH_DIR="${CORPUS_TRASH_DIR:-$REPO_ROOT/.trash}"

IN_JSON="$OUT_DIR/repos.json"
OUT_JSON="$OUT_DIR/repos_enriched.json"
OUT_REPORT="$OUT_DIR/ENRICHMENT_REPORT.md"
OUT_FAILURES="$OUT_DIR/enrichment_failures.tsv"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/enrich_github_repo_search_lolcode.sh
  ./scripts/enrich_github_repo_search_lolcode.sh --combine-only

Inputs:
  - corpus/research/github_repo_search_lolcode/repos.json

Outputs:
  - corpus/research/github_repo_search_lolcode/repos_enriched.json
  - corpus/research/github_repo_search_lolcode/ENRICHMENT_REPORT.md
  - corpus/research/github_repo_search_lolcode/enrichment_failures.tsv

Notes:
  - Fetches per-repo metadata and root contents for the full broad-search lane.
  - `--combine-only` skips live GitHub fetches and rebuilds outputs from cached raw
    responses already present under `enriched_raw/`.
  - Uses cached raw responses when live fetches fail.
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
  for cmd in gh jq mktemp trash sort wc; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "Missing required command: $cmd" >&2
      missing=1
    fi
  done
  [ "$missing" -eq 0 ]
}

repo_label() {
  printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's#[^a-z0-9]#-#g'
}

fetch_or_cache() {
  local endpoint="$1"
  local out_path="$2"
  local failure_tag="$3"

  if gh api "$endpoint" > "$out_path.tmp" 2>/dev/null; then
    mv "$out_path.tmp" "$out_path"
    printf 'ok\t%s\n' "$failure_tag" >> "$TMP_DIR/results.tsv"
    return 0
  fi

  rm -f "$out_path.tmp"

  if [ -s "$out_path" ]; then
    printf 'cached\t%s\n' "$failure_tag" >> "$TMP_DIR/results.tsv"
    return 0
  fi

  printf 'fail\t%s\n' "$failure_tag" >> "$TMP_DIR/results.tsv"
  return 1
}

combine_only=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --combine-only)
      combine_only=1
      shift
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

[ -f "$IN_JSON" ] || {
  echo "Missing input: $IN_JSON" >&2
  echo "Run ./scripts/sync_github_repo_search_lolcode.sh first." >&2
  exit 1
}

mkdir -p "$RAW_DIR"
: > "$TMP_DIR/results.tsv"
: > "$OUT_FAILURES"

if [ "$combine_only" -eq 0 ]; then
  if ! gh auth status >/dev/null 2>&1; then
    echo "error: gh auth unavailable. Run: gh auth login" >&2
    exit 1
  fi

  while IFS= read -r repo; do
    [ -n "$repo" ] || continue
    label="$(repo_label "$repo")"
    meta_path="$RAW_DIR/$label.meta.json"
    root_path="$RAW_DIR/$label.root.json"

    fetch_or_cache "repos/$repo" "$meta_path" "$repo/meta" || true
    fetch_or_cache "repos/$repo/contents" "$root_path" "$repo/root" || true
  done < <(jq -r '.[].repo' "$IN_JSON")
fi

python3 "$REPO_ROOT/scripts/combine_github_repo_search_lolcode_enrichment.py"

total_repos="$(jq 'length' "$OUT_JSON")"
meta_ok="$(jq '[.[] | select(.meta_fetch_ok)] | length' "$OUT_JSON")"
root_ok="$(jq '[.[] | select(.root_fetch_ok)] | length' "$OUT_JSON")"
fail_count="$(( $(wc -l < "$OUT_FAILURES") - 1 ))"
root_missing_count="$(awk -F '\t' 'NR > 1 && $1 == "root-missing" { count += 1 } END { print count + 0 }' "$OUT_FAILURES")"

{
  echo '# GitHub Broad `lolcode` Enrichment Report'
  echo
  printf -- '- Generated: %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  printf -- '- Repos enriched: `%s`\n' "$total_repos"
  printf -- '- Metadata fetch/cache available: `%s`\n' "$meta_ok"
  printf -- '- Root listing fetch/cache available: `%s`\n' "$root_ok"
  printf -- '- Root listing missing: `%s`\n' "$root_missing_count"
  printf -- '- Failure rows: `%s`\n' "$fail_count"
  echo
  echo 'Inspection status:'
  echo
  printf -- '- `%s` repos currently remain partially inspected because GitHub root listings were unavailable or missing.\n' "$root_missing_count"
  echo
  echo 'Outputs:'
  echo
  echo '- `corpus/research/github_repo_search_lolcode/repos_enriched.json`'
  echo '- `corpus/research/github_repo_search_lolcode/enrichment_failures.tsv`'
} > "$OUT_REPORT"

echo "wrote $OUT_JSON"
echo "wrote $OUT_FAILURES"
echo "wrote $OUT_REPORT"

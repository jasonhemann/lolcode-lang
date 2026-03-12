#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DISCOVERY_DIR="$REPO_ROOT/corpus/research/github_language_lolcode"
HITS_JSON="$DISCOVERY_DIR/code_hits.json"
OUT_ROOT="$DISCOVERY_DIR/hits_files"
REPORT_JSON="$DISCOVERY_DIR/hits_fetch_summary.json"
REPORT_TSV="$DISCOVERY_DIR/hits_fetch_results.tsv"
TRASH_DIR="${CORPUS_TRASH_DIR:-$REPO_ROOT/.trash}"

ONLY_LOL=true
KEEP_EXISTING=false
MAX_TIME_SEC="${MAX_TIME_SEC:-25}"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/sync_github_code_hits_files.sh
  ./scripts/sync_github_code_hits_files.sh --all-extensions
  ./scripts/sync_github_code_hits_files.sh --keep-existing
  ./scripts/sync_github_code_hits_files.sh --hits-json path/to/code_hits.json

Behavior:
  - Downloads raw files for each entry in code_hits.json under:
      corpus/research/github_language_lolcode/hits_files/<repo>/<sha>/<path>
  - Default mode downloads only *.lol paths.
  - Produces:
      hits_fetch_results.tsv
      hits_fetch_summary.json
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

url_encode_path_preserving_slash() {
  local raw_path="$1"
  jq -nr --arg p "$raw_path" '$p|@uri' | sed 's/%2[Ff]/\//g'
}

blob_url_to_raw_url() {
  local blob_url="$1"
  if printf '%s' "$blob_url" | grep -Eq '^https://github\.com/[^/]+/[^/]+/blob/'; then
    printf '%s' "$blob_url" \
      | sed 's#^https://github.com/#https://raw.githubusercontent.com/#; s#/blob/#/#'
    return 0
  fi
  return 1
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --all-extensions)
      ONLY_LOL=false
      shift
      ;;
    --keep-existing)
      KEEP_EXISTING=true
      shift
      ;;
    --hits-json)
      [ "$#" -lt 2 ] && { echo "Missing value for --hits-json" >&2; exit 2; }
      HITS_JSON="$2"
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

for cmd in curl jq sed mkdir dirname trash date; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 1
  fi
done

[ -f "$HITS_JSON" ] || {
  echo "Missing input: $HITS_JSON" >&2
  echo "Run ./scripts/sync_github_language_lolcode.sh first." >&2
  exit 1
}

mkdir -p "$DISCOVERY_DIR"

if [ "$KEEP_EXISTING" = false ]; then
  trash_path "$OUT_ROOT"
fi
mkdir -p "$OUT_ROOT"

tmp_tsv="$(mktemp "${TMPDIR:-/tmp}/github-hits-fetch.XXXXXX.tsv")"
cleanup_tmp() {
  rm -f "$tmp_tsv"
}
trap cleanup_tmp EXIT

printf 'status\trepo\tsha\tpath\traw_url\tnote\n' > "$tmp_tsv"

total=0
selected=0
downloaded=0
skipped_non_lol=0
skipped_existing=0
failed=0

while IFS=$'\t' read -r repo path sha blob_url; do
  [ -n "$repo" ] || continue
  total=$((total + 1))

  if [ "$ONLY_LOL" = true ] && ! printf '%s' "$path" | grep -Eiq '\.lol$'; then
    skipped_non_lol=$((skipped_non_lol + 1))
    printf 'skip-non-lol\t%s\t%s\t%s\t\tfiltered-by-extension\n' "$repo" "$sha" "$path" >> "$tmp_tsv"
    continue
  fi

  selected=$((selected + 1))

  raw_url=""
  if ! raw_url="$(blob_url_to_raw_url "$blob_url")"; then
    encoded_path="$(url_encode_path_preserving_slash "$path")"
    raw_url="https://raw.githubusercontent.com/$repo/$sha/$encoded_path"
  fi
  dest="$OUT_ROOT/$repo/$sha/$path"

  if [ -f "$dest" ]; then
    skipped_existing=$((skipped_existing + 1))
    printf 'skip-existing\t%s\t%s\t%s\t%s\talready-present\n' "$repo" "$sha" "$path" "$raw_url" >> "$tmp_tsv"
    continue
  fi

  mkdir -p "$(dirname "$dest")"
  if curl -sS -L --globoff --fail --max-time "$MAX_TIME_SEC" "$raw_url" > "$dest"; then
    downloaded=$((downloaded + 1))
    printf 'ok\t%s\t%s\t%s\t%s\t\n' "$repo" "$sha" "$path" "$raw_url" >> "$tmp_tsv"
  else
    failed=$((failed + 1))
    rm -f "$dest"
    printf 'failed\t%s\t%s\t%s\t%s\tcurl-failed\n' "$repo" "$sha" "$path" "$raw_url" >> "$tmp_tsv"
  fi
done < <(jq -r '.[] | [.repo, .path, .sha, .url] | @tsv' "$HITS_JSON")

cp "$tmp_tsv" "$REPORT_TSV"

jq -n \
  --arg generated_at "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
  --arg hits_json "${HITS_JSON#$REPO_ROOT/}" \
  --arg out_root "${OUT_ROOT#$REPO_ROOT/}" \
  --arg report_tsv "${REPORT_TSV#$REPO_ROOT/}" \
  --argjson only_lol "$([ "$ONLY_LOL" = true ] && echo true || echo false)" \
  --argjson keep_existing "$([ "$KEEP_EXISTING" = true ] && echo true || echo false)" \
  --argjson total "$total" \
  --argjson selected "$selected" \
  --argjson downloaded "$downloaded" \
  --argjson skipped_non_lol "$skipped_non_lol" \
  --argjson skipped_existing "$skipped_existing" \
  --argjson failed "$failed" \
  '{
    generated_at: $generated_at,
    input: {
      hits_json: $hits_json
    },
    output: {
      out_root: $out_root,
      report_tsv: $report_tsv
    },
    options: {
      only_lol: $only_lol,
      keep_existing: $keep_existing
    },
    totals: {
      entries_seen: $total,
      entries_selected: $selected,
      downloaded: $downloaded,
      skipped_non_lol: $skipped_non_lol,
      skipped_existing: $skipped_existing,
      failed: $failed
    }
  }' > "$REPORT_JSON"

echo "wrote $REPORT_JSON"
echo "wrote $REPORT_TSV"

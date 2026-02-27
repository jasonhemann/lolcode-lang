#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORPUS_ROOT="$REPO_ROOT/corpus"
CATALOG_PATH="$CORPUS_ROOT/tier2/CANDIDATE_REPOS.tsv"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/corpus-sync.XXXXXX")"
TRASH_DIR="${CORPUS_TRASH_DIR:-$REPO_ROOT/.trash}"

trash_path() {
  local path="$1"
  [ -e "$path" ] || return 0

  if ! command -v trash >/dev/null 2>&1; then
    echo "Missing required command: trash" >&2
    return 1
  fi

  mkdir -p "$TRASH_DIR"

  # Prefer `sudo trash` when non-interactive sudo is available; otherwise use trash.
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

declare -a TARGET_TIERS=()
SYNC_ALL=true

usage() {
  cat <<'EOF'
Usage:
  ./scripts/sync_corpus.sh
  ./scripts/sync_corpus.sh --tier tier1 --tier tier2

Behavior:
  - No flags: sync all tiers found in corpus/tier2/CANDIDATE_REPOS.tsv.
  - --tier: sync only the specified tier(s).
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --tier)
      [ "$#" -lt 2 ] && { echo "Missing value for --tier" >&2; exit 1; }
      TARGET_TIERS+=("$2")
      SYNC_ALL=false
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

require_cmds() {
  local missing=0
  for cmd in curl jq rg awk sed xargs find wc date mktemp trash; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "Missing required command: $cmd" >&2
      missing=1
    fi
  done
  [ "$missing" -eq 0 ]
}

require_cmds || exit 1

declare -a FEATURE_PATTERNS=(
  "CAN HAS [A-Z]+\\?"
  "HAI [0-9]+\\.[0-9]+"
  "HOW IZ I"
  "IF U SAY SO"
  "FOUND YR"
  "IM IN YR"
  "IM OUTTA YR"
  "UPPIN YR"
  "NERFIN YR"
  "TIL"
  "WILE"
  "O RLY\\?"
  "YA RLY"
  "MEBBE"
  "NO WAI"
  "OIC"
  "WTF\\?"
  "OMGWTF"
  "OMG "
  "SMOOSH"
  "MAEK"
  "IS NOW A"
  "I IZ"
  "I HAS A"
  "HAS A"
  "ITZ A BUKKIT"
  "LIEK A"
  "'Z "
  "SRS "
  "GIMMEH"
  "VISIBLE"
  "INVISIBLE"
  "BOTH SAEM"
  "DIFFRINT"
  "BOTH OF"
  "EITHER OF"
  "WON OF"
  "ALL OF"
  "ANY OF"
  "NOT"
)

mkdir -p "$CORPUS_ROOT"

matches_requested_tier() {
  local tier="$1"
  if [ "$SYNC_ALL" = true ]; then
    return 0
  fi
  local t
  for t in "${TARGET_TIERS[@]}"; do
    if [ "$t" = "$tier" ]; then
      return 0
    fi
  done
  return 1
}

download_repo_snapshot() {
  local tier="$1"
  local label="$2"
  local repo="$3"
  local out="$CORPUS_ROOT/$tier/$label"
  local tree_json="$TMP_DIR/${tier}-${label}-tree.json"
  local selected="$TMP_DIR/${tier}-${label}-files.txt"
  local branch
  local file_failures=0

  trash_path "$out"
  mkdir -p "$out/files"

  if ! curl -sS -L --max-time 20 "https://api.github.com/repos/$repo" > "$out/metadata.json"; then
    echo "failed:metadata-fetch"
    return 1
  fi

  branch="$(jq -r '.default_branch // empty' "$out/metadata.json")"
  if [ -z "$branch" ]; then
    echo "failed:no-default-branch"
    return 1
  fi

  if ! curl -sS -L --max-time 20 "https://api.github.com/repos/$repo/git/trees/$branch?recursive=1" > "$tree_json"; then
    echo "failed:tree-fetch"
    return 1
  fi

  jq -r '.tree[]? | select(.type=="blob") | .path' "$tree_json" \
    | awk '
      /\.lol$/ ||
      /^README(\..*)?$/ ||
      /(^|\/)README(\..*)?$/ ||
      /(^|\/)Makefile$/ ||
      /\.sh$/ ||
      /\.tsv$/ { print }
    ' \
    > "$selected"

  while IFS= read -r path; do
    [ -z "$path" ] && continue
    mkdir -p "$out/files/$(dirname "$path")"
    if ! curl -sS -L --max-time 20 "https://raw.githubusercontent.com/$repo/$branch/$path" > "$out/files/$path"; then
      file_failures=$((file_failures + 1))
    fi
  done < "$selected"

  if [ "$file_failures" -gt 0 ]; then
    echo "ok:partial:$file_failures"
  else
    echo "ok"
  fi
  return 0
}

rows_path="$TMP_DIR/catalog-rows.tsv"
awk 'NF && $1 !~ /^#/' "$CATALOG_PATH" > "$rows_path"

entries_jsonl="$TMP_DIR/entries.jsonl"
: > "$entries_jsonl"

declare -a SELECTED_TIERS=()

tier_in_selected() {
  local needle="$1"
  local t
  for t in "${SELECTED_TIERS[@]}"; do
    if [ "$t" = "$needle" ]; then
      return 0
    fi
  done
  return 1
}

while IFS=$'\t' read -r tier label repo kind oracle_priority corpus_priority source status; do
  [ -z "$tier" ] && continue

  if ! matches_requested_tier "$tier"; then
    continue
  fi

  if ! tier_in_selected "$tier"; then
    SELECTED_TIERS+=("$tier")
  fi

  if [ "$status" = "archive" ]; then
    jq -n \
      --arg tier "$tier" \
      --arg label "$label" \
      --arg repo "$repo" \
      --arg kind "$kind" \
      --arg oracle_priority "$oracle_priority" \
      --arg corpus_priority "$corpus_priority" \
      --arg source "$source" \
      --arg status "$status" \
      --arg sync_state "skipped" \
      --arg sync_note "archive-entry" \
      '
      {
        tier: $tier,
        label: $label,
        repo: $repo,
        kind: $kind,
        oracle_priority: $oracle_priority,
        corpus_priority: $corpus_priority,
        source: $source,
        status: $status,
        sync_state: $sync_state,
        sync_note: $sync_note
      }' >> "$entries_jsonl"
    continue
  fi

  sync_note="$(download_repo_snapshot "$tier" "$label" "$repo" || true)"
  sync_state="ok"
  case "$sync_note" in
    ok|ok:partial:*)
      sync_state="ok"
      ;;
    failed:*)
      sync_state="failed"
      ;;
    *)
      sync_state="failed"
      [ -z "$sync_note" ] && sync_note="failed:unknown"
      ;;
  esac

  jq -n \
    --arg tier "$tier" \
    --arg label "$label" \
    --arg repo "$repo" \
    --arg kind "$kind" \
    --arg oracle_priority "$oracle_priority" \
    --arg corpus_priority "$corpus_priority" \
    --arg source "$source" \
    --arg status "$status" \
    --arg sync_state "$sync_state" \
    --arg sync_note "$sync_note" \
    '
    {
      tier: $tier,
      label: $label,
      repo: $repo,
      kind: $kind,
      oracle_priority: $oracle_priority,
      corpus_priority: $corpus_priority,
      source: $source,
      status: $status,
      sync_state: $sync_state,
      sync_note: $sync_note
    }' >> "$entries_jsonl"
done < "$rows_path"

if [ "${#SELECTED_TIERS[@]}" -eq 0 ]; then
  echo "No matching tiers selected. Available tiers are defined in $CATALOG_PATH." >&2
  exit 1
fi

now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

jq -s \
  --arg generated_at "$now" \
  --arg catalog "corpus/tier2/CANDIDATE_REPOS.tsv" \
  '
  {
    generated_at: $generated_at,
    catalog: $catalog,
    entries: .
  }' \
  "$entries_jsonl" \
  > "$CORPUS_ROOT/manifest.json"

generate_feature_profile() {
  local tier="$1"
  local out="$CORPUS_ROOT/$tier/FEATURE_PROFILE.md"

  mkdir -p "$CORPUS_ROOT/$tier"

  {
    echo "# $tier Feature Profile"
    echo
    echo "Generated: \`$now\`"
    echo
  } > "$out"

  while IFS=$'\t' read -r row_tier label repo kind oracle_priority corpus_priority source status; do
    [ -z "$row_tier" ] && continue
    [ "$row_tier" != "$tier" ] && continue

    local repo_dir="$CORPUS_ROOT/$tier/$label/files"
    local lol_count=0
    local line_count=0

    if [ -d "$repo_dir" ]; then
      lol_count="$(find "$repo_dir" -type f -name "*.lol" | wc -l | awk "{print \$1}")"
      if [ "$lol_count" -gt 0 ]; then
        line_count="$(find "$repo_dir" -type f -name "*.lol" -print0 | xargs -0 cat | wc -l | awk "{print \$1}")"
      fi
    fi

    {
      echo "## $label"
      echo
      echo "- Repo: \`$repo\`"
      echo "- Kind: \`$kind\`"
      echo "- Status: \`$status\`"
      echo "- LOLCODE files: \`$lol_count\`"
      echo "- Total LOLCODE lines: \`$line_count\`"
      echo
      echo "| Construct | Count |"
      echo "| --- | ---: |"
    } >> "$out"

    for pattern in "${FEATURE_PATTERNS[@]}"; do
      local count=0
      if [ "$lol_count" -gt 0 ]; then
        count="$(
          find "$repo_dir" -type f -name "*.lol" -print0 \
            | xargs -0 rg -o -N "$pattern" \
            | wc -l \
            | awk "{print \$1}" \
            || true
        )"
      fi
      if [ "$count" -gt 0 ]; then
        printf '| `%s` | %s |\n' "$pattern" "$count" >> "$out"
      fi
    done
    echo >> "$out"
  done < "$rows_path"
}

for tier in "${SELECTED_TIERS[@]}"; do
  mkdir -p "$CORPUS_ROOT/$tier"

  jq \
    --arg tier "$tier" \
    --arg generated_at "$now" \
    '
    {
      generated_at: $generated_at,
      tier: $tier,
      entries: [.entries[] | select(.tier == $tier)]
    }' \
    "$CORPUS_ROOT/manifest.json" \
    > "$CORPUS_ROOT/$tier/manifest.json"

  generate_feature_profile "$tier"
done

echo "Synced corpus tiers: ${SELECTED_TIERS[*]}"
echo "Manifest: $CORPUS_ROOT/manifest.json"

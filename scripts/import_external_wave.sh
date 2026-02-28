#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANDIDATE_TSV="$ROOT_DIR/corpus/research/external_issues/candidate_repros.tsv"
EVIDENCE_DIR="$ROOT_DIR/tests/regression-evidence/external"
FIXTURES_DIR="$EVIDENCE_DIR/fixtures"
MANIFEST="$EVIDENCE_DIR/manifest.rktd"

usage() {
  cat <<USAGE
usage: $0 WAVE_NUMBER

Imports one wave from candidate_repros.tsv into:
  - tests/regression-evidence/external/manifest.rktd
  - tests/regression-evidence/external/fixtures/<project>/wave_<NN>/<kind>_<id>/repro.lol
USAGE
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

WAVE="$1"
if ! [[ "$WAVE" =~ ^[0-9]+$ ]] || [[ "$WAVE" -le 0 ]]; then
  echo "error: WAVE_NUMBER must be a positive integer" >&2
  exit 1
fi

if [[ ! -f "$CANDIDATE_TSV" ]]; then
  echo "error: missing candidate repro list: $CANDIDATE_TSV" >&2
  exit 1
fi

mkdir -p "$FIXTURES_DIR"
if [[ ! -f "$MANIFEST" ]]; then
  cat > "$MANIFEST" <<'EOF_MANIFEST'
(
)
EOF_MANIFEST
fi

sanitize_slug() {
  local s="$1"
  s="$(printf '%s' "$s" | tr '[:upper:]' '[:lower:]')"
  s="$(printf '%s' "$s" | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+//; s/-+$//')"
  if [[ -z "$s" ]]; then
    s="unknown"
  fi
  printf '%s' "$s"
}

sanitize_id_token() {
  local s="$1"
  s="$(printf '%s' "$s" | tr '[:upper:]' '[:lower:]')"
  s="$(printf '%s' "$s" | sed -E 's/[^a-z0-9]+/_/g; s/^_+//; s/_+$//')"
  if [[ -z "$s" ]]; then
    s="unknown"
  fi
  printf '%s' "$s"
}

append_manifest_entry() {
  local manifest_path="$1"
  local entry="$2"
  local tmp
  tmp="$(mktemp "${TMPDIR:-/tmp}/manifest-entry.XXXXXX")"

  local last
  last="$(
    awk '/^[[:space:]]*\)[[:space:]]*$/ { line = NR } END { print line + 0 }' "$manifest_path"
  )"

  if [[ "$last" -eq 0 ]]; then
    {
      echo "("
      cat "$manifest_path"
      echo
      printf '%s\n' "$entry"
      echo ")"
    } > "$tmp"
  else
    awk -v last="$last" 'NR < last { print }' "$manifest_path" > "$tmp"
    echo >> "$tmp"
    printf '%s\n' "$entry" >> "$tmp"
    echo ")" >> "$tmp"
    awk -v last="$last" 'NR > last { print }' "$manifest_path" >> "$tmp"
  fi

  mv "$tmp" "$manifest_path"
}

printf -v wave_dir "wave_%02d" "$WAVE"
today="$(date +%F)"

imported=0
existing=0
skipped=0

while IFS=$'\t' read -r rank wave repo label item_type number state category score title url; do
  if [[ "$wave" == "wave" ]]; then
    continue
  fi

  if [[ "$wave" != "$WAVE" ]]; then
    continue
  fi

  kind="$item_type"
  case "$kind" in
    issue) source_origin="issue-body" ;;
    pr) source_origin="pr-description" ;;
    commit) source_origin="commit-message" ;;
    *)
      echo "skip: unsupported item_type '$kind' for row rank=$rank" >&2
      skipped=$((skipped + 1))
      continue
      ;;
  esac

  project="${label:-}"
  if [[ -z "$project" ]]; then
    project="${repo##*/}"
  fi

  project_slug="$(sanitize_slug "$project")"
  project_id="$(sanitize_id_token "$project_slug")"

  source_id="${number:-}"
  source_token=""
  if [[ -n "$source_id" && "$source_id" =~ ^[0-9]+$ ]]; then
    printf -v source_token "%04d" "$source_id"
  else
    if [[ -z "$source_id" ]]; then
      source_id="${url##*/}"
    fi
    source_token="$(sanitize_id_token "$source_id")"
  fi

  case_id="ext_${project_id}_${kind}_${source_token}"

  fixture_rel="fixtures/${project_slug}/${wave_dir}/${kind}_${source_token}/repro.lol"
  fixture_abs="$EVIDENCE_DIR/$fixture_rel"

  if rg -Fq "(id . \"$case_id\")" "$MANIFEST"; then
    existing=$((existing + 1))
    continue
  fi

  mkdir -p "$(dirname "$fixture_abs")"
  if [[ ! -f "$fixture_abs" ]]; then
    cat > "$fixture_abs" <<EOF_FIXTURE
HAI 1.2
BTW External evidence fixture scaffold.
BTW Source: $url
BTW Title: $title
KTHXBYE
EOF_FIXTURE
  fi

  notes="Imported from candidate_repros.tsv rank=${rank} state=${state} category=${category} score=${score} title=${title}"
  notes_escaped="${notes//\"/\\\"}"

  entry=$(
    printf '%s\n' \
      "  #hasheq(" \
      "    (id . \"$case_id\")" \
      "    (wave . $WAVE)" \
      "    (source-file . \"$fixture_rel\")" \
      "    (source-project . \"$project_slug\")" \
      "    (source-repo . \"$repo\")" \
      "    (source-kind . \"$kind\")" \
      "    (source-id . \"$source_id\")" \
      "    (source-url . \"$url\")" \
      "    (source-origin . \"$source_origin\")" \
      "    (spec-scope . (\"unknown\"))" \
      "    (spec-refs . ())" \
      "    (oracle-class . \"external-evidence\")" \
      "    (triage-status . \"candidate\")" \
      "    (hypothesis . \"unknown\")" \
      "    (notes . \"$notes_escaped\")" \
      "    (added-on . \"$today\"))"
  )

  append_manifest_entry "$MANIFEST" "$entry"
  imported=$((imported + 1))
done < "$CANDIDATE_TSV"

echo "wave=$WAVE imported=$imported existing=$existing skipped=$skipped"
echo "manifest=$MANIFEST"

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESEARCH_DIR="$ROOT_DIR/corpus/research"
CANONICAL_JSON="$RESEARCH_DIR/CANONICAL_ARTIFACTS.json"
REPORT_OUT=""
QUIET=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --report-out)
      REPORT_OUT="$2"
      shift 2
      ;;
    --quiet)
      QUIET=1
      shift
      ;;
    *)
      echo "usage: $0 [--report-out PATH] [--quiet]" >&2
      exit 2
      ;;
  esac
done

for cmd in jq sed grep find; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "error: required command missing: $cmd" >&2
    exit 2
  fi
done

tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/research-drift.XXXXXX")"
cleanup_tmpdir() {
  find "$tmpdir" -type f -exec rm -f {} + 2>/dev/null || true
  find "$tmpdir" -depth -type d -exec rmdir {} + 2>/dev/null || true
}
trap cleanup_tmpdir EXIT

# Default to an ephemeral report path so advisory checks are read-only unless
# callers explicitly request a persisted report.
if [[ -z "${REPORT_OUT:-}" ]]; then
  REPORT_OUT="$tmpdir/drift-report.json"
fi

warnings_jsonl="$tmpdir/warnings.jsonl"
: > "$warnings_jsonl"

missing_artifacts_count=0
duplicate_paths_count=0
top_level_dated_count=0
md_json_leak_count=0
readme_drift_count=0
rendered_md_count=0
doc_ref_missing_count=0

add_warning() {
  local category="$1"
  local path="$2"
  local message="$3"
  jq -nc \
    --arg category "$category" \
    --arg path "$path" \
    --arg message "$message" \
    '{category: $category, path: $path, message: $message}' \
    >> "$warnings_jsonl"
}

if [[ ! -f "$CANONICAL_JSON" ]]; then
  add_warning "missing-canonical-map" "corpus/research/CANONICAL_ARTIFACTS.json" "canonical artifact map is missing"
else
  if ! jq empty "$CANONICAL_JSON" >/dev/null 2>&1; then
    add_warning "invalid-canonical-map" "corpus/research/CANONICAL_ARTIFACTS.json" "canonical artifact map is not valid JSON"
  else
    while IFS= read -r rel_path; do
      [[ -z "$rel_path" ]] && continue
      if [[ ! -e "$ROOT_DIR/$rel_path" ]]; then
        add_warning "missing-artifact" "$rel_path" "canonical artifact missing on disk"
        missing_artifacts_count=$((missing_artifacts_count + 1))
      fi
    done < <(jq -r '.artifacts[].path' "$CANONICAL_JSON")

    while IFS= read -r dup_path; do
      [[ -z "$dup_path" ]] && continue
      add_warning "duplicate-artifact-path" "$dup_path" "duplicate path appears in CANONICAL_ARTIFACTS.json"
      duplicate_paths_count=$((duplicate_paths_count + 1))
    done < <(jq -r '.artifacts[].path' "$CANONICAL_JSON" | sort | uniq -d)

    while IFS=$'\t' read -r md_path src_path; do
      [[ -z "$md_path" ]] && continue
      abs_md="$ROOT_DIR/$md_path"
      if [[ -f "$abs_md" ]]; then
        if ! grep -q "Generated:" "$abs_md"; then
          add_warning "rendered-md-metadata" "$md_path" "rendered markdown is missing Generated metadata"
          rendered_md_count=$((rendered_md_count + 1))
        fi
        if ! grep -Fq "$src_path" "$abs_md"; then
          add_warning "rendered-md-source-reference" "$md_path" "rendered markdown does not reference expected JSON source: $src_path"
          rendered_md_count=$((rendered_md_count + 1))
        fi
      fi
    done < <(jq -r '.artifacts[] | select(.kind == "md" and (.rendered_from != null)) | [.path, .rendered_from] | @tsv' "$CANONICAL_JSON")
  fi
fi

while IFS= read -r path; do
  base="$(basename "$path")"
  if [[ "$base" =~ [0-9]{4}-[0-9]{2}-[0-9]{2} ]]; then
    add_warning "top-level-dated-file" "corpus/research/$base" "dated file exists at top-level research directory; should be archived"
    top_level_dated_count=$((top_level_dated_count + 1))
  fi
done < <(find "$RESEARCH_DIR" -maxdepth 1 -type f | sort)

while IFS= read -r path; do
  rel="${path#$ROOT_DIR/}"
  add_warning "md-json-leak" "$rel" "*.md.json artifact found outside archive"
  md_json_leak_count=$((md_json_leak_count + 1))
done < <(find "$RESEARCH_DIR" -type f -name '*.md.json' ! -path "$RESEARCH_DIR/archive/*" | sort)

readme_path="$RESEARCH_DIR/README.md"
if [[ -f "$readme_path" && -f "$CANONICAL_JSON" ]] && jq empty "$CANONICAL_JSON" >/dev/null 2>&1; then
  expected_paths="$tmpdir/readme.expected"
  actual_paths="$tmpdir/readme.actual"
  : > "$expected_paths"
  : > "$actual_paths"

  jq -r '.artifacts[] | select(.include_in_readme == true) | .path' "$CANONICAL_JSON" \
    | sort -u > "$expected_paths"

  if ! grep -q "canonical-readme:start" "$readme_path" || ! grep -q "canonical-readme:end" "$readme_path"; then
    add_warning "readme-missing-canonical-markers" "corpus/research/README.md" "README.md is missing canonical-readme marker block"
    readme_drift_count=$((readme_drift_count + 1))
  else
    sed -n '/canonical-readme:start/,/canonical-readme:end/p' "$readme_path" \
      | sed -n 's/.*`\([^`]*\)`.*/\1/p' \
      | sort -u > "$actual_paths"

    while IFS= read -r p; do
      [[ -z "$p" ]] && continue
      add_warning "readme-canonical-missing" "$p" "path is in canonical map but missing from README canonical list"
      readme_drift_count=$((readme_drift_count + 1))
    done < <(comm -23 "$expected_paths" "$actual_paths")

    while IFS= read -r p; do
      [[ -z "$p" ]] && continue
      add_warning "readme-canonical-extra" "$p" "path is listed as canonical in README but absent from canonical map"
      readme_drift_count=$((readme_drift_count + 1))
    done < <(comm -13 "$expected_paths" "$actual_paths")
  fi
fi

for doc in "$RESEARCH_DIR/README.md" "$RESEARCH_DIR/INDEX.md"; do
  [[ -f "$doc" ]] || continue
  while IFS= read -r rel; do
    [[ -z "$rel" ]] && continue
    if [[ ! -e "$ROOT_DIR/$rel" ]]; then
      add_warning "doc-reference-missing" "${doc#$ROOT_DIR/}" "document references missing path: $rel"
      doc_ref_missing_count=$((doc_ref_missing_count + 1))
    fi
  done < <(sed -n 's/.*`\([^`]*\)`.*/\1/p' "$doc" | grep -E '^(corpus/|scripts/)' || true)
done

warnings_count="$(jq -s 'length' "$warnings_jsonl")"
generated_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

mkdir -p "$(dirname "$REPORT_OUT")"
jq -s \
  --arg generated_at "$generated_at" \
  --arg mode "advisory" \
  --arg map_path "corpus/research/CANONICAL_ARTIFACTS.json" \
  --arg report_path "${REPORT_OUT#$ROOT_DIR/}" \
  --argjson missing_artifacts_count "$missing_artifacts_count" \
  --argjson duplicate_paths_count "$duplicate_paths_count" \
  --argjson top_level_dated_count "$top_level_dated_count" \
  --argjson md_json_leak_count "$md_json_leak_count" \
  --argjson readme_drift_count "$readme_drift_count" \
  --argjson rendered_md_count "$rendered_md_count" \
  --argjson doc_ref_missing_count "$doc_ref_missing_count" \
  '
  {
    generated_at: $generated_at,
    mode: $mode,
    canonical_map: $map_path,
    report_path: $report_path,
    warnings_count: (length),
    checks: [
      {name: "missing-artifacts", count: $missing_artifacts_count},
      {name: "duplicate-artifact-paths", count: $duplicate_paths_count},
      {name: "top-level-dated-files", count: $top_level_dated_count},
      {name: "md-json-leaks", count: $md_json_leak_count},
      {name: "readme-canonical-drift", count: $readme_drift_count},
      {name: "rendered-md-metadata", count: $rendered_md_count},
      {name: "doc-reference-missing", count: $doc_ref_missing_count}
    ],
    warnings: .
  }
  ' "$warnings_jsonl" > "$REPORT_OUT"

if [[ "$QUIET" -eq 0 ]]; then
  echo "[research-drift] mode=advisory warnings=$warnings_count report=${REPORT_OUT#$ROOT_DIR/}"
  if [[ "$warnings_count" -gt 0 ]]; then
    jq -r '.warnings[] | "- [" + .category + "] " + .path + " :: " + .message' "$REPORT_OUT"
  else
    echo "- no drift detected"
  fi
fi

# Advisory mode never blocks.
exit 0

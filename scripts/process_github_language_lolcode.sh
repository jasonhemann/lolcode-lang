#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DISCOVERY_DIR="$REPO_ROOT/corpus/research/github_language_lolcode"
HITS_ROOT="$DISCOVERY_DIR/hits_files"

SKIP_DISCOVERY=false
SKIP_FETCH=false
SKIP_EVAL=false
SKIP_GAPS=false
FETCH_ALL_EXTENSIONS=false

usage() {
  cat <<'EOF'
Usage:
  ./scripts/process_github_language_lolcode.sh
  ./scripts/process_github_language_lolcode.sh --skip-discovery
  ./scripts/process_github_language_lolcode.sh --skip-fetch --skip-gaps
  ./scripts/process_github_language_lolcode.sh --fetch-all-extensions

Pipeline:
  1. sync_github_language_lolcode.sh
  2. sync_github_code_hits_files.sh
  3. eval_tier2_corpus.sh over hits_files
  4. analyze_corpus_gaps.rkt over hits_files
  5. write PIPELINE_SUMMARY.md
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --skip-discovery)
      SKIP_DISCOVERY=true
      shift
      ;;
    --skip-fetch)
      SKIP_FETCH=true
      shift
      ;;
    --skip-eval)
      SKIP_EVAL=true
      shift
      ;;
    --skip-gaps)
      SKIP_GAPS=true
      shift
      ;;
    --fetch-all-extensions)
      FETCH_ALL_EXTENSIONS=true
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

if [ "$SKIP_DISCOVERY" = false ]; then
  "$REPO_ROOT/scripts/sync_github_language_lolcode.sh"
fi

if [ "$SKIP_FETCH" = false ]; then
  if [ "$FETCH_ALL_EXTENSIONS" = true ]; then
    "$REPO_ROOT/scripts/sync_github_code_hits_files.sh" --all-extensions
  else
    "$REPO_ROOT/scripts/sync_github_code_hits_files.sh"
  fi
fi

if [ "$SKIP_EVAL" = false ]; then
  "$REPO_ROOT/scripts/eval_tier2_corpus.sh" \
    --corpus-root "$HITS_ROOT" \
    --json-out "$DISCOVERY_DIR/hits-eval-classified.json" \
    --md-out "$DISCOVERY_DIR/hits-eval-classified.md"
fi

if [ "$SKIP_GAPS" = false ]; then
  racket "$REPO_ROOT/scripts/analyze_corpus_gaps.rkt" \
    --corpus-root "$HITS_ROOT" \
    --json-out "$DISCOVERY_DIR/hits-language-gaps.json" \
    --md-out "$DISCOVERY_DIR/HITS_LANGUAGE_GAPS_REPORT.md"
fi

summary_md="$DISCOVERY_DIR/PIPELINE_SUMMARY.md"
generated_at="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"

hits_seen=0
hits_selected=0
hits_downloaded=0
hits_failed=0
eval_files=0
eval_likely=0
eval_ok=0
eval_parse=0
eval_runtime=0
eval_nonprog=0
gaps_core=0
gaps_extension=0
gaps_unknown=0

if [ -f "$DISCOVERY_DIR/hits_fetch_summary.json" ]; then
  hits_seen="$(jq -r '.totals.entries_seen // 0' "$DISCOVERY_DIR/hits_fetch_summary.json")"
  hits_selected="$(jq -r '.totals.entries_selected // 0' "$DISCOVERY_DIR/hits_fetch_summary.json")"
  hits_downloaded="$(jq -r '.totals.downloaded // 0' "$DISCOVERY_DIR/hits_fetch_summary.json")"
  hits_failed="$(jq -r '.totals.failed // 0' "$DISCOVERY_DIR/hits_fetch_summary.json")"
fi

if [ -f "$DISCOVERY_DIR/hits-eval-classified.json" ]; then
  eval_files="$(jq -r '.summary.totals.files // 0' "$DISCOVERY_DIR/hits-eval-classified.json")"
  eval_likely="$(jq -r '.summary.totals["likely-programs"] // 0' "$DISCOVERY_DIR/hits-eval-classified.json")"
  eval_nonprog="$(jq -r '.summary.totals["non-programs"] // 0' "$DISCOVERY_DIR/hits-eval-classified.json")"
  eval_ok="$(jq -r '((.summary["outcome-counts-likely-programs"] | map(select(.label=="ok") | .count) | add) // 0)' "$DISCOVERY_DIR/hits-eval-classified.json")"
  eval_parse="$(jq -r '((.summary["outcome-counts-likely-programs"] | map(select(.label=="parse-error") | .count) | add) // 0)' "$DISCOVERY_DIR/hits-eval-classified.json")"
  eval_runtime="$(jq -r '((.summary["outcome-counts-likely-programs"] | map(select(.label=="runtime-error" or .label=="runtime-exn") | .count) | add) // 0)' "$DISCOVERY_DIR/hits-eval-classified.json")"
fi

if [ -f "$DISCOVERY_DIR/hits-language-gaps.json" ]; then
  if jq -e 'has("issues")' "$DISCOVERY_DIR/hits-language-gaps.json" >/dev/null 2>&1; then
    gaps_core="$(jq -r '[.issues[]? | select(.issue_class=="core-1.2/1.3")] | length' "$DISCOVERY_DIR/hits-language-gaps.json")"
    gaps_extension="$(jq -r '[.issues[]? | select(.issue_class=="extension-or-noncore")] | length' "$DISCOVERY_DIR/hits-language-gaps.json")"
    gaps_unknown="$(jq -r '[.issues[]? | select(.issue_class=="unknown")] | length' "$DISCOVERY_DIR/hits-language-gaps.json")"
  else
    gaps_core="$(jq -r '[.["issue-triage-counts"][]? | select(.label=="parse-core-suspect" or .label=="runtime-core-suspect") | .count] | add // 0' "$DISCOVERY_DIR/hits-language-gaps.json")"
    gaps_extension="$(jq -r '[.["issue-triage-counts"][]? | select(.label=="extension-or-noncore") | .count] | add // 0' "$DISCOVERY_DIR/hits-language-gaps.json")"
    gaps_unknown="$(jq -r '[.["issue-triage-counts"][]? | select((.label=="parse-core-suspect" or .label=="runtime-core-suspect" or .label=="extension-or-noncore") | not) | .count] | add // 0' "$DISCOVERY_DIR/hits-language-gaps.json")"
  fi
fi

{
  echo "# GitHub LOLCODE Pipeline Summary"
  echo
  echo "- Generated: $generated_at"
  echo
  echo "## Fetch"
  echo
  echo "- Hits seen: \`$hits_seen\`"
  echo "- Hits selected: \`$hits_selected\`"
  echo "- Files downloaded: \`$hits_downloaded\`"
  echo "- Fetch failures: \`$hits_failed\`"
  echo
  echo "## Dynamic Eval"
  echo
  echo "- Files scanned: \`$eval_files\`"
  echo "- Likely programs: \`$eval_likely\`"
  echo "- Non-programs: \`$eval_nonprog\`"
  echo "- Likely-program outcomes: ok=\`$eval_ok\`, parse-error=\`$eval_parse\`, runtime-error/exn=\`$eval_runtime\`"
  echo
  echo "## Static Gap Classes"
  echo
  echo "- core-1.2/1.3: \`$gaps_core\`"
  echo "- extension-or-noncore: \`$gaps_extension\`"
  echo "- unknown: \`$gaps_unknown\`"
  echo
  echo "## Artifacts"
  echo
  echo "- \`corpus/research/github_language_lolcode/hits_fetch_summary.json\`"
  echo "- \`corpus/research/github_language_lolcode/hits_fetch_results.tsv\`"
  echo "- \`corpus/research/github_language_lolcode/hits-eval-classified.json\`"
  echo "- \`corpus/research/github_language_lolcode/hits-eval-classified.md\`"
  echo "- \`corpus/research/github_language_lolcode/hits-language-gaps.json\`"
  echo "- \`corpus/research/github_language_lolcode/HITS_LANGUAGE_GAPS_REPORT.md\`"
} > "$summary_md"

echo "wrote $summary_md"

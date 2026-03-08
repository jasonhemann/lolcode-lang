#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_MD="$ROOT_DIR/corpus/research/CURRENT_STATUS.md"

tier1_json="$(ls -1t "$ROOT_DIR"/corpus/research/tier1-eval-classified*.json 2>/dev/null | head -n1 || true)"
tier2_json="$(ls -1t "$ROOT_DIR"/corpus/research/tier2-eval-classified*.json 2>/dev/null | head -n1 || true)"
manifest_json="$ROOT_DIR/corpus/manifest.json"
rejected_json="$ROOT_DIR/corpus/research/PROMOTED_1_3_REJECTED_NONCOMPLIANT.json"
external_queue_json="$ROOT_DIR/corpus/research/external_issues/candidate_repros_ranked.json"
external_report_json="$ROOT_DIR/corpus/research/external-evidence-report.json"
lci_issues_json="$ROOT_DIR/corpus/research/lci_issues/issues.json"
lci_pulls_json="$ROOT_DIR/corpus/research/lci_issues/pulls.json"

render_outcome_rows() {
  local json_path="$1"
  jq -r '
    .summary["outcome-counts-likely-programs"]
    | sort_by(-.count, .label)
    | .[]
    | "| `" + .label + "` | " + (.count|tostring) + " |"
  ' "$json_path"
}

total_outcome_count() {
  local json_path="$1"
  local label="$2"
  jq -r --arg label "$label" '
    ((.summary["outcome-counts-likely-programs"]
      | map(select(.label == $label) | .count)
      | add) // 0)
  ' "$json_path"
}

{
  echo "# Corpus Current Status"
  echo
  echo "- Generated: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  echo "- Policy scope: strict \`HAI 1.3\` implementation target"
  echo
  echo "## Canonical Sources"
  echo
  echo "- Manifest + extraction progress: \`corpus/manifest.json\`"
  echo "- Tier evaluation snapshots:"
  echo "  - \`${tier1_json#$ROOT_DIR/}\`"
  echo "  - \`${tier2_json#$ROOT_DIR/}\`"
  echo "- Strict reject list: \`corpus/research/PROMOTED_1_3_REJECTED_NONCOMPLIANT.json\`"
  echo "- External bug/issue queue: \`corpus/research/external_issues/candidate_repros_ranked.json\`"
  echo "- External evidence rollup: \`corpus/research/external-evidence-report.json\`"
  echo "- LCI backlog snapshot: \`corpus/research/lci_issues/{issues.json,pulls.json}\`"
  echo
  echo "## Program Classification (Good vs Not Yet Passing)"
  echo
  if [[ -n "$tier1_json" && -f "$tier1_json" ]]; then
    echo "### Tier1"
    echo
    echo "- Snapshot generated-at: $(jq -r '.summary["generated-at"]' "$tier1_json")"
    echo "- Files: $(jq -r '.summary.totals.files' "$tier1_json")"
    echo "- Likely programs: $(jq -r '.summary.totals["likely-programs"]' "$tier1_json")"
    echo "- Non-programs: $(jq -r '.summary.totals["non-programs"]' "$tier1_json")"
    echo
    echo "| Outcome (likely programs) | Count |"
    echo "|---|---:|"
    render_outcome_rows "$tier1_json"
    echo
  fi

  if [[ -n "$tier2_json" && -f "$tier2_json" ]]; then
    echo "### Tier2"
    echo
    echo "- Snapshot generated-at: $(jq -r '.summary["generated-at"]' "$tier2_json")"
    echo "- Files: $(jq -r '.summary.totals.files' "$tier2_json")"
    echo "- Likely programs: $(jq -r '.summary.totals["likely-programs"]' "$tier2_json")"
    echo "- Non-programs: $(jq -r '.summary.totals["non-programs"]' "$tier2_json")"
    echo
    echo "| Outcome (likely programs) | Count |"
    echo "|---|---:|"
    render_outcome_rows "$tier2_json"
    echo
  fi

  tier1_ok=0
  tier2_ok=0
  if [[ -n "$tier1_json" && -f "$tier1_json" ]]; then
    tier1_ok="$(total_outcome_count "$tier1_json" "ok")"
  fi
  if [[ -n "$tier2_json" && -f "$tier2_json" ]]; then
    tier2_ok="$(total_outcome_count "$tier2_json" "ok")"
  fi
  combined_ok=$((tier1_ok + tier2_ok))

  echo "### Tracking Buckets"
  echo
  echo "- Good (strict-1.3 currently passing): \`$combined_ok\`"
  if [[ -f "$rejected_json" ]]; then
    rejected_count="$(jq -r '.rejected_files | length' "$rejected_json")"
    echo "- Irredeemably bad for strict-1.3 (explicit reject list): \`$rejected_count\`"
  fi
  echo "- Fixed-here (from corpus manifest extraction progress): \`$(jq -r '[.entries[] | .extraction_progress.fixed_here_total // 0] | add' "$manifest_json")\`"
  echo

  echo "## Implementation/Bug Harvest Progress"
  echo
  echo "- Corpus manifest entries: $(jq -r '.entries | length' "$manifest_json")"
  echo "- Sync state counts:"
  jq -r '
    .entries
    | group_by(.sync_state)
    | sort_by(.[0].sync_state)
    | .[]
    | "- `\(. [0].sync_state)`: \(.|length)"
  ' "$manifest_json"
  echo
  echo "- Aggregated extraction totals (manifest):"
  echo "  - external_items_total: $(jq -r '[.entries[] | .extraction_progress.external_items_total // 0] | add' "$manifest_json")"
  echo "  - candidate_repros_total: $(jq -r '[.entries[] | .extraction_progress.candidate_repros_total // 0] | add' "$manifest_json")"
  echo "  - imported_test_cases_total: $(jq -r '[.entries[] | .extraction_progress.imported_test_cases_total // 0] | add' "$manifest_json")"
  echo "  - known_divergences_total: $(jq -r '[.entries[] | .extraction_progress.known_divergences_total // 0] | add' "$manifest_json")"
  echo "  - known_failures_total: $(jq -r '[.entries[] | .extraction_progress.known_failures_total // 0] | add' "$manifest_json")"
  echo "  - fixed_here_total: $(jq -r '[.entries[] | .extraction_progress.fixed_here_total // 0] | add' "$manifest_json")"
  echo "  - candidate_triage_total: $(jq -r '[.entries[] | .extraction_progress.candidate_triage_total // 0] | add' "$manifest_json")"
  echo

  if [[ -f "$external_queue_json" ]]; then
    echo "- External regression candidate queue:"
    echo "  - total candidates: $(jq 'length' "$external_queue_json")"
    echo "  - core-1.2/1.3 candidates: $(jq '[.[] | select(.spec_scope == "core-1.2-1.3")] | length' "$external_queue_json")"
    echo "  - extension candidates: $(jq '[.[] | select(.spec_scope == "extension")] | length' "$external_queue_json")"
    echo "  - unknown-scope candidates: $(jq '[.[] | select(.spec_scope == "unknown")] | length' "$external_queue_json")"
    echo "  - waves: $(jq 'if length == 0 then 0 else (max_by(.wave).wave) end' "$external_queue_json")"
    echo
  fi

  if [[ -f "$external_report_json" ]]; then
    echo "- External evidence report totals:"
    echo "  - cases: $(jq -r '.totals.cases' "$external_report_json")"
    jq -r '
      .["bucket-counts"]
      | sort_by(-.count, .label)
      | .[]
      | "  - bucket:" + .label + " = " + (.count|tostring)
    ' "$external_report_json"
    echo
  fi

  if [[ -f "$lci_issues_json" && -f "$lci_pulls_json" ]]; then
    echo "- LCI backlog snapshot:"
    echo "  - issues total/open/closed: $(jq 'length' "$lci_issues_json")/$(jq '[.[]|select(.state=="open")]|length' "$lci_issues_json")/$(jq '[.[]|select(.state=="closed")]|length' "$lci_issues_json")"
    echo "  - pulls total/open/closed: $(jq 'length' "$lci_pulls_json")/$(jq '[.[]|select(.state=="open")]|length' "$lci_pulls_json")/$(jq '[.[]|select(.state=="closed")]|length' "$lci_pulls_json")"
    echo
  fi

  echo "## Refresh Commands"
  echo
  printf '%s\n' '```bash'
  echo "./scripts/sync_corpus.sh"
  echo "./scripts/build_external_regression_queue.sh"
  echo "./scripts/sync_lci_issue_backlog.sh"
  echo "./scripts/eval_tier2_corpus.sh"
  echo "./scripts/update_corpus_status.sh"
  printf '%s\n' '```'
} > "$OUT_MD"

echo "wrote $OUT_MD"

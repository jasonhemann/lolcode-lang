#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESEARCH_DIR="$ROOT_DIR/corpus/research"
CANONICAL_JSON="$RESEARCH_DIR/CANONICAL_ARTIFACTS.json"
RUN_JSON="$RESEARCH_DIR/current_run.json"
DRIFT_JSON="$RESEARCH_DIR/drift-report.json"

OFFLINE=0
SNAPSHOT_TAG=""
SKIP_EXTERNAL_EVIDENCE_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --offline)
      OFFLINE=1
      shift
      ;;
    --snapshot-tag)
      SNAPSHOT_TAG="$2"
      shift 2
      ;;
    --skip-external-evidence-run)
      SKIP_EXTERNAL_EVIDENCE_RUN=1
      shift
      ;;
    *)
      echo "usage: $0 [--offline] [--snapshot-tag TAG] [--skip-external-evidence-run]" >&2
      exit 2
      ;;
  esac
done

tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/refresh-research.XXXXXX")"
cleanup_tmpdir() {
  find "$tmpdir" -type f -exec rm -f {} + 2>/dev/null || true
  find "$tmpdir" -depth -type d -exec rmdir {} + 2>/dev/null || true
}
trap cleanup_tmpdir EXIT

steps_jsonl="$tmpdir/steps.jsonl"
: > "$steps_jsonl"

run_step() {
  local name="$1"
  shift
  local start_epoch end_epoch duration exit_code status
  local started_at ended_at
  start_epoch="$(date +%s)"
  started_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  if "$@"; then
    exit_code=0
    status="ok"
  else
    exit_code=$?
    status="failed"
  fi
  end_epoch="$(date +%s)"
  ended_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  duration=$((end_epoch - start_epoch))
  jq -nc \
    --arg name "$name" \
    --arg status "$status" \
    --arg started_at "$started_at" \
    --arg ended_at "$ended_at" \
    --argjson duration_seconds "$duration" \
    --argjson exit_code "$exit_code" \
    '{
      name: $name,
      status: $status,
      started_at: $started_at,
      ended_at: $ended_at,
      duration_seconds: $duration_seconds,
      exit_code: $exit_code
    }' >> "$steps_jsonl"
  return "$exit_code"
}

snapshot_canonical_artifacts() {
  local tag="$1"
  local destination="$RESEARCH_DIR/archive/snapshots/$tag"
  mkdir -p "$destination"
  while IFS= read -r rel_path; do
    [[ -z "$rel_path" ]] && continue
    if [[ -e "$ROOT_DIR/$rel_path" ]]; then
      mkdir -p "$destination/$(dirname "$rel_path")"
      cp "$ROOT_DIR/$rel_path" "$destination/$rel_path"
    fi
  done < <(jq -r '.artifacts[].path' "$CANONICAL_JSON")
}

generate_archive_index() {
  local index_file="$RESEARCH_DIR/archive/INDEX.md"
  local generated_at
  generated_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  mkdir -p "$(dirname "$index_file")"
  {
    echo "# Research Archive Index"
    echo
    echo "- Generated: $generated_at"
    echo "- Purpose: historical snapshots and one-off reports moved from canonical top-level surfaces."
    echo
    echo "## Snapshot Paths"
    echo
    find "$RESEARCH_DIR/archive" -type f \
      ! -path "$RESEARCH_DIR/archive/INDEX.md" \
      | sed "s#^$ROOT_DIR/##" \
      | sort \
      | sed 's#^#- `#; s#$#`#'
    echo
  } > "$index_file"
}

run_started_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
run_status="ok"
failed_step=""

jq -nc \
  --arg generated_at "$run_started_at" \
  '{
    generated_at: $generated_at,
    mode: "advisory",
    status: "in-progress",
    steps: []
  }' > "$RUN_JSON"

if [[ "$OFFLINE" -eq 0 ]]; then
  run_step "sync-corpus" "$ROOT_DIR/scripts/sync_corpus.sh" || { run_status="failed"; failed_step="sync-corpus"; }
  if [[ "$run_status" == "ok" ]]; then
    run_step "build-external-queue" "$ROOT_DIR/scripts/build_external_regression_queue.sh" || { run_status="failed"; failed_step="build-external-queue"; }
  fi
  if [[ "$run_status" == "ok" ]]; then
    run_step "sync-lci-backlog" "$ROOT_DIR/scripts/sync_lci_issue_backlog.sh" || { run_status="failed"; failed_step="sync-lci-backlog"; }
  fi
fi

if [[ "$run_status" == "ok" ]]; then
  run_step "eval-tier1" "$ROOT_DIR/scripts/eval_tier2_corpus.sh" \
    --corpus-root "$ROOT_DIR/corpus/tier1" \
    --json-out "$ROOT_DIR/corpus/research/tier1-eval-classified.json" \
    --md-out "$ROOT_DIR/corpus/research/tier1-eval-classified.md" || { run_status="failed"; failed_step="eval-tier1"; }
fi
if [[ "$run_status" == "ok" ]]; then
  run_step "eval-tier2" "$ROOT_DIR/scripts/eval_tier2_corpus.sh" || { run_status="failed"; failed_step="eval-tier2"; }
fi
if [[ "$run_status" == "ok" ]]; then
  run_step "eval-tier3" "$ROOT_DIR/scripts/eval_tier2_corpus.sh" \
    --corpus-root "$ROOT_DIR/corpus/tier3" \
    --json-out "$ROOT_DIR/corpus/research/tier3-eval-classified.json" \
    --md-out "$ROOT_DIR/corpus/research/tier3-eval-classified.md" || { run_status="failed"; failed_step="eval-tier3"; }
fi
if [[ "$run_status" == "ok" ]]; then
  run_step "analyze-language-gaps" "$ROOT_DIR/scripts/analyze_corpus_gaps.sh" || { run_status="failed"; failed_step="analyze-language-gaps"; }
fi
if [[ "$run_status" == "ok" && "$SKIP_EXTERNAL_EVIDENCE_RUN" -eq 0 ]]; then
  run_step "run-external-evidence" "$ROOT_DIR/scripts/test_external_evidence.sh" || { run_status="failed"; failed_step="run-external-evidence"; }
fi
if [[ "$run_status" == "ok" ]]; then
  run_step "analyze-external-evidence" "$ROOT_DIR/scripts/analyze_external_evidence.sh" || { run_status="failed"; failed_step="analyze-external-evidence"; }
fi
if [[ "$run_status" == "ok" ]]; then
  run_step "update-current-status" "$ROOT_DIR/scripts/update_corpus_status.sh" || { run_status="failed"; failed_step="update-current-status"; }
fi

run_step "check-research-drift" "$ROOT_DIR/scripts/check_research_drift.sh" --report-out "$DRIFT_JSON" || true

if [[ "$run_status" == "ok" && -n "$SNAPSHOT_TAG" ]]; then
  run_step "snapshot-canonical-artifacts" snapshot_canonical_artifacts "$SNAPSHOT_TAG" \
    || { run_status="failed"; failed_step="snapshot-canonical-artifacts"; }
fi

generate_archive_index

run_ended_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
drift_warnings=0
if [[ -f "$DRIFT_JSON" ]]; then
  drift_warnings="$(jq -r '.warnings_count // 0' "$DRIFT_JSON" 2>/dev/null || echo 0)"
fi

jq -s \
  --arg generated_at "$run_ended_at" \
  --arg started_at "$run_started_at" \
  --arg ended_at "$run_ended_at" \
  --arg status "$run_status" \
  --arg failed_step "$failed_step" \
  --argjson offline "$OFFLINE" \
  --argjson skip_external_evidence_run "$SKIP_EXTERNAL_EVIDENCE_RUN" \
  --arg snapshot_tag "$SNAPSHOT_TAG" \
  --argjson drift_warnings "$drift_warnings" \
  '{
    generated_at: $generated_at,
    mode: "advisory",
    started_at: $started_at,
    ended_at: $ended_at,
    offline: ($offline == 1),
    skip_external_evidence_run: ($skip_external_evidence_run == 1),
    snapshot_tag: (if $snapshot_tag == "" then null else $snapshot_tag end),
    status: $status,
    failed_step: (if $failed_step == "" then null else $failed_step end),
    drift_warnings: $drift_warnings,
    steps: .
  }' "$steps_jsonl" > "$RUN_JSON"

echo "[refresh-research] status=$run_status offline=$OFFLINE drift_warnings=$drift_warnings"
echo "[refresh-research] run metadata: ${RUN_JSON#$ROOT_DIR/}"
echo "[refresh-research] drift report: ${DRIFT_JSON#$ROOT_DIR/}"

if [[ "$run_status" != "ok" ]]; then
  exit 1
fi

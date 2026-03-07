# Corpus Research Docs

This directory has two kinds of files:

1. Active tracking surfaces (edit/read first).
2. Historical snapshots (dated investigation notes and one-off reports).

## Active Tracking Surfaces

- `CURRENT_STATUS.md`
  - Canonical high-level status for:
    - strict-1.3 good/rejected/fixed buckets
    - corpus sync/extraction progress
    - external issue/PR harvesting backlog
- `external_issues/QUEUE.md`
  - Current ranked wave queue for issue/PR-based repro import.
- `lci_issues/TRIAGE.md`
  - LCI-specific triage workflow and candidate list.
- `availability/AVAILABILITY_REPORT.md`
  - Live/archive availability of candidate repos.
- `SPEC_1_2_1_3_IMPLEMENTATION_STATUS.md`
  - Core strict-spec implementation status summary.

## Regeneration Workflow

```bash
./scripts/sync_corpus.sh
./scripts/build_external_regression_queue.sh
./scripts/sync_lci_issue_backlog.sh
./scripts/eval_tier2_corpus.sh
./scripts/update_corpus_status.sh
```

## Historical Snapshots

Files with date-stamped names (for example `*_2026-03-02.md`) are retained as provenance snapshots and are not canonical policy/tracking sources.

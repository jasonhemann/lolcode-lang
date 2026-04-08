# Corpus Research

Canonical policy:

- JSON files are the source of truth.
- Markdown files are rendered views and summaries.
- The canonical map is `corpus/research/CANONICAL_ARTIFACTS.json`.

## Canonical Tracking Surfaces

<!-- canonical-readme:start -->
- `corpus/research/CURRENT_STATUS.md`
- `corpus/research/tier1-eval-classified.md`
- `corpus/research/tier2-eval-classified.md`
- `corpus/research/tier3-eval-classified.md`
- `corpus/research/LANGUAGE_GAPS_REPORT.md`
- `corpus/research/EXTERNAL_EVIDENCE_REPORT.md`
- `corpus/research/external_issues/QUEUE.md`
- `corpus/research/lci_issues/TRIAGE.md`
- `corpus/research/availability/AVAILABILITY_REPORT.md`
<!-- canonical-readme:end -->

## Refresh Workflow

```bash
./scripts/refresh_research.sh
```

Offline/advisory refresh:

```bash
./scripts/refresh_research.sh --offline
```

Faster local advisory refresh (skip external evidence replay):

```bash
./scripts/refresh_research.sh --offline --skip-external-evidence-run
```

Standalone advisory drift check:

```bash
./scripts/check_research_drift.sh
```

Persist the drift report to a tracked path only when explicitly requested:

```bash
./scripts/check_research_drift.sh --report-out corpus/research/drift-report.json
```

Install local non-blocking pre-push hook:

```bash
./scripts/install_research_prepush_hook.sh
```

The installed hook is read-only: it runs advisory drift checks but does not run refresh/generation steps.

## Advisory Discovery Lanes

These are maintained discovery/inventory surfaces. They are useful inputs to
promotion and later comparison work, but they are not release-blocking
conformance surfaces.

- `corpus/research/github_language_lolcode/`
- `corpus/research/github_repo_search_lolcode/`
- `corpus/research/codeberg_repo_search_lolcode/`

The broad GitHub repo-search lane keeps JSON/TSV as source of truth and
Markdown as rendered summary. The current snapshot is still partially
inspected: `22` repos are missing root listings and remain marked that way.

Current non-GitHub host status is tracked in:

- `corpus/research/NON_GITHUB_DISCOVERY_STATUS.md`

The staged plan for later external implementation comparison lives in:

- `corpus/research/EXTERNAL_IMPLEMENTATION_MATRIX_TRANCHES.md`

## Historical Snapshots

Historical snapshots and one-off reports live under:

- `corpus/research/archive/`

They are retained for provenance and are not canonical active surfaces.

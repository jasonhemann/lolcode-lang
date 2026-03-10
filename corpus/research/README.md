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

Install local non-blocking pre-push hook:

```bash
./scripts/install_research_prepush_hook.sh
```

## Historical Snapshots

Historical snapshots and one-off reports live under:

- `corpus/research/archive/`

They are retained for provenance and are not canonical active surfaces.

# Corpus Current Status

- Generated: 2026-03-08T05:40:42Z
- Policy scope: strict `HAI 1.3` implementation target

## Canonical Sources

- Manifest + extraction progress: `corpus/manifest.json`
- Tier evaluation snapshots:
  - `corpus/research/tier1-eval-classified.json`
  - `corpus/research/tier2-eval-classified.json`
- Strict reject list: `corpus/research/PROMOTED_1_3_REJECTED_NONCOMPLIANT.json`
- External bug/issue queue: `corpus/research/external_issues/candidate_repros_ranked.json`
- External evidence rollup: `corpus/research/external-evidence-report.json`
- LCI backlog snapshot: `corpus/research/lci_issues/{issues.json,pulls.json}`

## Program Classification (Good vs Not Yet Passing)

### Tier1

- Snapshot generated-at: Sunday, March 8th, 2026 12:40:35am
- Files: 352
- Likely programs: 350
- Non-programs: 2

| Outcome (likely programs) | Count |
|---|---:|
| `ok` | 264 |
| `parse-error` | 50 |
| `runtime-error` | 23 |
| `lex-error` | 12 |
| `timeout` | 1 |

### Tier2

- Snapshot generated-at: Sunday, March 8th, 2026 12:40:37am
- Files: 223
- Likely programs: 184
- Non-programs: 39

| Outcome (likely programs) | Count |
|---|---:|
| `parse-error` | 167 |
| `ok` | 8 |
| `lex-error` | 7 |
| `runtime-error` | 1 |
| `timeout` | 1 |

### Tracking Buckets

- Good (strict-1.3 currently passing): `272`
- Irredeemably bad for strict-1.3 (explicit reject list): `7`
- Fixed-here (from corpus manifest extraction progress): `0`

## Implementation/Bug Harvest Progress

- Corpus manifest entries: 40
- Sync state counts:
- `ok`: 30
- `skipped`: 10

- Aggregated extraction totals (manifest):
  - external_items_total: 2276
  - candidate_repros_total: 493
  - imported_test_cases_total: 352
  - known_divergences_total: 0
  - known_failures_total: 0
  - fixed_here_total: 0
  - candidate_triage_total: 50

- External regression candidate queue:
  - total candidates: 493
  - core-1.2/1.3 candidates: 493
  - extension candidates: 0
  - unknown-scope candidates: 0
  - waves: 50

- External evidence report totals:
  - cases: 422
  - bucket:strict-non-1.3-or-extension = 417
  - bucket:program-bug-or-non-spec-input = 4
  - bucket:ok = 1

- LCI backlog snapshot:
  - issues total/open/closed: 59/38/21
  - pulls total/open/closed: 27/6/21

## Refresh Commands

```bash
./scripts/sync_corpus.sh
./scripts/build_external_regression_queue.sh
./scripts/sync_lci_issue_backlog.sh
./scripts/eval_tier2_corpus.sh
./scripts/update_corpus_status.sh
```

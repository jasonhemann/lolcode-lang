# Tiered LOLCODE Corpus

This repository uses a tiered corpus model for implementation comparison and program harvesting.

## Tiers

- `tier1`: highest-value differential oracles (primary interpreter/compiler targets)
- `tier2`: secondary implementations plus non-normative real-world program corpora
- `tier3`: niche or extension-oriented implementations

## Source Catalog

Catalog file:

- `corpus/tier2/CANDIDATE_REPOS.tsv`

Columns:

- `tier`
- `label`
- `repo`
- `kind`
- `oracle_priority`
- `corpus_priority`
- `source`
- `status`

## Sync

Sync all tiers:

```bash
./scripts/sync_corpus.sh
```

Deletion policy for sync cleanup is non-destructive: replaced directories are moved into
`$REPO_ROOT/.trash` (override with `CORPUS_TRASH_DIR`).

Sync one tier:

```bash
./scripts/sync_corpus.sh --tier tier2
```

Backward-compatible tier2 wrapper:

```bash
./scripts/sync_tier2_corpus.sh
```

## Availability Audit

Probe live and archive availability for implementation links:

```bash
./scripts/check_implementation_availability.sh
```

Outputs:

- `corpus/research/availability/availability.json`
- `corpus/research/availability/AVAILABILITY_REPORT.md`

## External Regression Queue

Build an all-items external issue/PR queue and wave-based candidate repro backlog:

```bash
./scripts/build_external_regression_queue.sh
```

Outputs:

- `corpus/research/external_issues/QUEUE.md`
- `corpus/research/external_issues/candidate_repros.tsv`
- `corpus/research/external_issues/candidate_repros_ranked.json`

Update consolidated corpus tracking status:

```bash
./scripts/update_corpus_status.sh
```

Canonical status surface:

- `corpus/research/CURRENT_STATUS.md`
- `corpus/research/README.md`

Seed one wave into the non-gating evidence suite:

```bash
./scripts/import_external_wave.sh 1
```

## Classified Tier2 Eval (Step 1)

Classify tier2 `.lol` files into likely programs vs non-programs before lex/parse/eval:

```bash
./scripts/eval_tier2_corpus.sh
```

Options:

- `--corpus-root <dir>`
- `--timeout-seconds <seconds>`
- `--json-out <path>`
- `--md-out <path>`

Default outputs:

- `corpus/research/tier2-eval-classified.json`
- `corpus/research/tier2-eval-classified.md`

## Strict 1.3 Gap Analysis

Analyze deficiencies and feature/branch-shape coverage for strict `HAI 1.3` programs:

```bash
./scripts/analyze_corpus_gaps.sh
```

Default outputs:

- `corpus/research/language-gaps-report.json`
- `corpus/research/LANGUAGE_GAPS_REPORT_2026-03-02.md`

## 1.4 Extension Status

Current project position and tracked evidence for the unofficial "1.4" extension line:

- `corpus/research/SPEC_1_4_EXTENSION_STATUS.md`

## Research Snapshots

- `corpus/research/lollm/README.md` (mixed LOLCODE + lolspeak corpus snapshot from `justinmeza/lollm`)
- `./scripts/slice_lollm_corpus.sh` slices `lollm/lolspeak.txt` into individual programs + non-program text
- `corpus/research/IMPLEMENTATION_ORACLE_MATRIX.md` (ranked implementation oracle matrix + seeded external regression targets)
- `corpus/research/EXTERNAL_REGRESSION_WAVES.md` (wave-based backlog for next 10 + next 10 + next 10 external regressions)
- `corpus/research/lci_issues/` (`lci` issue/PR snapshots and triage notes)

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

## 1.4 Extension Status

Current project position and tracked evidence for the unofficial "1.4" extension line:

- `corpus/research/SPEC_1_4_EXTENSION_STATUS.md`

## Research Snapshots

- `corpus/research/lollm/README.md` (mixed LOLCODE + lolspeak corpus snapshot from `justinmeza/lollm`)
- `./scripts/slice_lollm_corpus.sh` slices `lollm/lolspeak.txt` into individual programs + non-program text
- `corpus/research/IMPLEMENTATION_ORACLE_MATRIX.md` (ranked implementation oracle matrix + seeded external regression targets)
- `corpus/research/lci_issues/` (`lci` issue/PR snapshots and triage notes)

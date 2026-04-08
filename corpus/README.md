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

## GitHub Language Discovery Snapshot

Collect GitHub `language:LOLCODE` discovery signals (code-hit repos + repo-language hits),
dedupe by repository, and produce a review queue for repos not yet in
`corpus/tier2/CANDIDATE_REPOS.tsv`:

```bash
./scripts/sync_github_language_lolcode.sh
```

Outputs:

- `corpus/research/github_language_lolcode/REPORT.md`
- `corpus/research/github_language_lolcode/repos.json`
- `corpus/research/github_language_lolcode/new_repos_to_review.tsv`

Create a scored, noise-reduced top candidate queue from that snapshot:

```bash
./scripts/curate_github_language_lolcode_candidates.sh
```

Outputs:

- `corpus/research/github_language_lolcode/CURATION_REPORT.md`
- `corpus/research/github_language_lolcode/curated_candidates.tsv`
- `corpus/research/github_language_lolcode/curated_top50.tsv`
- `corpus/research/github_language_lolcode/excluded_noise.tsv`

Run exhaustive static + dynamic processing over discovered GitHub code hits:

```bash
./scripts/process_github_language_lolcode.sh
```

Core outputs:

- `corpus/research/github_language_lolcode/hits_fetch_summary.json`
- `corpus/research/github_language_lolcode/hits-eval-classified.json`
- `corpus/research/github_language_lolcode/hits-language-gaps.json`
- `corpus/research/github_language_lolcode/PIPELINE_SUMMARY.md`

## GitHub Broad `lolcode` Repo Search

Collect the full-tail broad GitHub repository search for `q=lolcode`, and enrich
it with cross-references to the existing candidate catalog plus the
`github_language_lolcode` snapshot:

```bash
./scripts/sync_github_repo_search_lolcode.sh
```

Outputs:

- `corpus/research/github_repo_search_lolcode/REPORT.md`
- `corpus/research/github_repo_search_lolcode/repos.json`
- `corpus/research/github_repo_search_lolcode/new_repos_to_review.tsv`

Enrich that snapshot with cached/live repo metadata and root listings:

```bash
./scripts/enrich_github_repo_search_lolcode.sh
```

Rebuild the enriched outputs from cached raw responses only:

```bash
./scripts/enrich_github_repo_search_lolcode.sh --combine-only
```

Outputs:

- `corpus/research/github_repo_search_lolcode/repos_enriched.json`
- `corpus/research/github_repo_search_lolcode/ENRICHMENT_REPORT.md`
- `corpus/research/github_repo_search_lolcode/enrichment_failures.tsv`

The current snapshot remains partially inspected: `22` repos are missing root
listings and stay marked that way until enrichment can fill them in.

Classify the enriched broad-search repos into `implementation`, `tooling`,
`docs`, `corpus`, or `noise`, and emit the full long-tail priority queue:

```bash
./scripts/curate_github_repo_search_lolcode.sh
```

Outputs:

- `corpus/research/github_repo_search_lolcode/CURATION_REPORT.md`
- `corpus/research/github_repo_search_lolcode/classified_repos.tsv`
- `corpus/research/github_repo_search_lolcode/priority_candidates.tsv`

Promote only `obvious-keep` `implementation` and `corpus` rows from the
broad-search lane into the tiered candidate catalog:

```bash
./scripts/promote_github_repo_search_lolcode_candidates.sh
```

Outputs:

- `corpus/research/github_repo_search_lolcode/PROMOTION_REPORT.md`
- appended rows in `corpus/tier2/CANDIDATE_REPOS.tsv`

This tranche is inventory and promotion only. It stops before `sync_corpus`,
external installation, or differential execution of external implementations.

Future external-implementation comparison work is staged separately in:

- `corpus/research/EXTERNAL_IMPLEMENTATION_MATRIX_TRANCHES.md`

## Non-GitHub `lolcode` Discovery

Collect Codeberg repository search results for `q=lolcode`:

```bash
./scripts/sync_codeberg_repo_search_lolcode.sh
```

Outputs:

- `corpus/research/codeberg_repo_search_lolcode/REPORT.md`
- `corpus/research/codeberg_repo_search_lolcode/repos.json`
- `corpus/research/codeberg_repo_search_lolcode/new_repos_to_review.tsv`

Current host-status note:

- `corpus/research/NON_GITHUB_DISCOVERY_STATUS.md`

Current limitation:

- GitLab is not yet a stable discovery lane in this repo. As of
  `2026-04-06`, unauthenticated API search returned `500`, and the plain
  search surface returned `403` or JS-heavy explore pages that are not yet
  scripted here.
- Bitbucket does not currently have a verified public global repo-search lane
  analogous to GitHub in this repo.
- SourceHut and `gitea.com` were probed and currently produced `0` `lolcode`
  hits, so they are recorded only in the host-status note.

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

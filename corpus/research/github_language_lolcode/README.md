# GitHub `language:LOLCODE` Research Artifacts

This directory stores corpus-discovery snapshots, dynamic eval outputs, and follow-on experiment outputs used for strict `HAI 1.3` research triage.

## Canonical Pipeline Outputs

- Discovery snapshot: `REPORT.md`, `summary.json`, `repos.tsv`, `new_repos_to_review.tsv`.
- Curation snapshot: `CURATION_REPORT.md`, `curation_scored.json`, `curated_candidates.tsv`, `excluded_noise.tsv`.
- Eval + gap scan: `hits-eval-classified.{json,md}`, `hits-language-gaps.json`, `HITS_LANGUAGE_GAPS_REPORT.md`.
- Pipeline digest: `PIPELINE_SUMMARY.md`.

## Header-Salvage Experiment (2026-03-12)

- Location: `experiments/header-salvage-2026-03-12/`.
- Purpose: normalize header/opening failures so downstream parse/runtime behavior is measurable.
- Transform scope:
  - trim leading prefix before first `HAI` for targeted header-failure rows.
  - normalize opener to `HAI 1.3` (including split `HAI` + next-line version).
- Key effect:
  - parse-error reduced from `367` to `281` (`-86`).
  - `46` moved to `ok`; `39` moved to `runtime-error`; `1` moved to `timeout`.
- Important records from this run:
  - transform manifest: `experiments/header-salvage-2026-03-12/manifest.tsv`.
  - eval report: `experiments/header-salvage-2026-03-12/eval-salvaged.{json,md}`.
  - gap/categorization report: `experiments/header-salvage-2026-03-12/gaps-salvaged.{json,md}`.

## What Is Important vs Not

- Important:
  - changes in outcome classes after salvage (`ok`, `parse-error`, `runtime-error`, `lex-error`, `timeout`).
  - `gaps-salvaged` triage classes and message distributions for strict-core review.
  - parser/runtime behaviors newly exposed after opener/header normalization.
- Usually not important for strict-core triage:
  - unsupported versions.
  - import-like token dialects (`STDIO?`, `STRING?`, etc.).
  - known strict identifier-shape rejections.
  - expected strict lexical malformed-source failures.

## Reproduce

```bash
./scripts/process_github_language_lolcode.sh --skip-discovery --skip-fetch
racket scripts/header_salvage_experiment.rkt \
  corpus/research/github_language_lolcode/hits-eval-classified.json \
  corpus/research/github_language_lolcode/hits_files \
  corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged \
  corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/manifest.tsv
./scripts/eval_tier2_corpus.sh \
  --corpus-root corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged \
  --json-out corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/eval-salvaged.json \
  --md-out corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/eval-salvaged.md
racket scripts/analyze_corpus_gaps.rkt \
  --corpus-root corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged \
  --json-out corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/gaps-salvaged.json \
  --md-out corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/gaps-salvaged.md
```

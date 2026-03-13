# Header-Salvage Experiment (2026-03-12)

## Goal

Measure deeper parser/runtime behavior by neutralizing high-volume opener/header failures.

## Inputs

- Pre-salvage eval: `../../hits-eval-classified.json`
- Working tree copy: `hits_files_salvaged/`
- Transform manifest: `manifest.tsv`

## Transform Rules

- For targeted parse failures, trim content before first `HAI`.
- Normalize opener to `HAI 1.3`.
- Merge split opener forms (`HAI` followed by standalone numeric version line) to `HAI 1.3`.

## Primary Outputs

- Eval: `eval-salvaged.json`, `eval-salvaged.md`
- Gap scan: `gaps-salvaged.json`, `gaps-salvaged.md`

## Key Outcome Deltas (Likely Programs)

- Parse errors: `367 -> 281` (`-86`)
- OK: `72 -> 118` (`+46`)
- Runtime errors: `16 -> 55` (`+39`)
- Timeouts: `1 -> 2` (`+1`)
- Lex errors: `9 -> 9` (`0`)

Interpretation: salvage moved files out of opener/header failure and into deeper parse/runtime behavior, which is the intended effect.

## Important Signals

- Outcome-class shifts after salvage (`ok`, `parse-error`, `runtime-error`, `lex-error`, `timeout`).
- Gap-triage distributions in `gaps-salvaged.{json,md}` (`parse-core-suspect`, `runtime-core-suspect`, extension-like buckets).
- Runtime/timeouts that are not obvious strict type/cast failures.
- Parser divergences that remain after header noise is removed.

## Usually Non-Actionable Signals

- Unsupported-version failures.
- Import-like token dialect failures (`STDIO?`, `STRING?`, `MYLIB?`, `MANGO?`).
- Strict identifier-shape rejects.
- Strict lexical malformed-source rejects (unterminated strings/comments).

## Interpretation Caveats

- Reported outcomes are first-fatal-failure outcomes per file.
- Salvaged sources are transformed research artifacts; they are not the original corpus text.

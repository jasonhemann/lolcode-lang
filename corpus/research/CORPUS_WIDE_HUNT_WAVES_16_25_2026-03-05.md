# Corpus Wide Hunt (Waves 16-25) - 2026-03-05

## Scope

- Expanded external evidence import by 10 additional waves (`16..25`).
- Re-ran strict corpus triage and compared against prior (raw vs minimal-normalized) results.
- Evaluated whether minimal disagreement edits convert skipped/rejected files into useful tests.

## Import Results

- Waves imported: `16..25`.
- Imported entries this pass: `100` (10 per wave).
- External fixture total now: `252` `.lol` files in `tests/regression-evidence/external/fixtures`.

## Data Quality Issue Found and Fixed

### Issue

`scripts/import_external_wave.sh` parsed TSV rows with fixed 11 columns:

- `while IFS=$'\t' read ... title url`
- rows with tab characters inside `title` shifted fields;
- `source-url` was corrupted to `"<title>\t<url>"`, breaking manifest validation.

### Fix

- Updated importer row parsing to:
  - read the whole line,
  - split to array,
  - treat first 9 fields as fixed,
  - treat last field as `url`,
  - reconstruct `title` from fields `10..(N-1)`.
- Repaired existing corrupted `source-url` entries in `tests/regression-evidence/external/manifest.rktd`.
- Verified by re-running `./scripts/import_external_wave.sh 16` (`imported=0 existing=10 skipped=0`) and re-running external evidence harness.

## External Evidence Harness Status

- `./scripts/test_external_evidence.sh` now runs without manifest-schema failure.
- Current observed statuses (raw external fixtures): `parse-error: 252`.
- Reason: all imported fixtures are scaffolds (`HAI 1.2` + comments), not extracted repro programs.

## Minimal-Edit Augmentation Findings

### Tier1+Tier2 (raw strict vs minimal normalization)

Files considered (likely programs): `534` in both views.

Raw outcomes:

- `ok: 279`
- `parse-error: 214`
- `runtime-error: 22`
- `lex-error: 18`
- `timeout: 1`

Minimal-normalized outcomes:

- `ok: 353`
- `parse-error: 96`
- `runtime-error: 61`
- `lex-error: 18`
- `timeout: 6`

Transition matrix:

- `ok -> ok: 279`
- `parse-error -> ok: 74`
- `parse-error -> runtime-error: 39`
- `parse-error -> timeout: 5`
- `parse-error -> parse-error: 96`
- `runtime-error -> runtime-error: 22`
- `lex-error -> lex-error: 18`
- `timeout -> timeout: 1`

What this means:

- Minimal strict edits are useful for triage: they converted `118` parse failures into executable cases (`74 ok + 39 runtime + 5 timeout`).
- Those newly-executing runtime/timeouts are where higher-value semantic checks are now exposed.

### External Fixtures (raw vs minimal normalization)

- Raw external fixtures: all `parse-error` (mostly `HAI 1.2` policy failure).
- After minimal `HAI 1.3` normalization: all `ok`.
- But this does **not** increase semantic coverage: fixtures are all scaffold stubs, not real repro code.

## Remaining Failure Clusters (Normalized Tier1+Tier2)

Top parse-error clusters:

- `invalid identifier syntax: "STDIO?"` (`20`)
- `invalid identifier syntax: "SOCKS?"` (`3`)
- `invalid identifier syntax: "STDLIB?"` (`2`)
- `invalid identifier syntax: "STRING?"` (`2`)
- `invalid identifier syntax: "RAYLIB?"` (`2`)
- `unexpected ID ("-->begin")` (`3`)
- various infix/non-spec `VISIBLE` string-concat forms (multiple small clusters)

Top runtime-error clusters:

- `unknown identifier: WAZZUP` (`18`) (non-1.3 dialect form)
- numeric coercion failures involving `NOOB` (e.g., `SUM`, `BIGGR`, `SMALLR`)
- a few extension-only symbols (`COLOR`, `PINGING`, `LOWERIN`)

Lex-error cluster stays unchanged (`18`), largely malformed literal/input cases.

## Prioritized Conclusions

1. No new strict-core parser/runtime regression was uncovered by waves `16..25`.
2. Biggest remaining parse-error mass is extension syntax (especially `CAN HAS <LIB>?` ecosystem variants), which is currently out of strict scope by project policy.
3. Highest-value next corpus step is **not** more scaffold imports; it is extracting real repro snippets into external fixtures.
4. Importer robustness is now materially better and should prevent manifest corruption on future waves.

## Suggested Next Actions

1. Add extraction stage to `import_external_wave.sh` (or adjacent script) that attempts to populate fixture bodies from linked issue/PR/commit snippets when available.
2. Keep strict-core triage queue focused on parse->runtime/timeouts unlocked by normalization (`39 + 5` cases).
3. Continue wave imports only if accompanied by repro-content extraction; otherwise marginal test-value is near zero.

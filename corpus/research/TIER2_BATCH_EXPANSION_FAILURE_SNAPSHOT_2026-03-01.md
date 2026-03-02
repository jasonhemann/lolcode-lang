# Tier2 Batch Expansion Failure Snapshot (2026-03-01)

## Scope
- Added two additional external issue waves: wave 2 and wave 3.
- Expanded tier2 corpus via `./scripts/sync_tier2_corpus.sh`.
- Measured lex/parse/eval pass rates over all tier2 `.lol` files.
- This snapshot excludes 1.4 extension implementation work (`COLOR`, `SOCKS`) from priority recommendations.

## Corpus Size
- Tier2 programs before expansion: 42
- Tier2 programs after expansion: 88

Top tier2 source counts:
- `loleuler`: 18
- `lolcode-py-cmsc124`: 17
- `lokalise-lol-post`: 15
- `loco`: 15
- `lolcode-py-sada`: 10
- `eulol`: 8
- `lol-ruby`: 3
- `httpd.lol`: 1
- `httpd-lol`: 1

## External Waves (Bug Repros)
- Wave 2 imported: 10 entries
- Wave 3 imported: 10 entries
- Evidence harness status: all `ok` for both waves
- Assessment labels are still `unknown` for these scaffold repros, so they do not yet provide strong semantic failure signal.

## Tier2 Lex/Parse/Eval Results
- Total files: 88
- `lex_ok=86`, `lex_fail=2`
- `parse_ok=47`, `parse_fail=39`
- `eval_ok=37`, `eval_runtime=5`, `eval_timeout=5` (among parse-success files)

## Parser Compatibility Pass (Same Day Follow-up)
Implemented compatibility in parser front-end:
- Bare `HAI` header accepted by inserting default version token (`1.2`) before parsing.
- Legacy `ALL OF` / `ANY OF` lines missing `MKAY` accepted by line-level token normalization.

After this pass (same 88-file tier2 set):
- `lex_ok=86`, `lex_fail=2` (unchanged)
- `parse_ok=70`, `parse_fail=16` (improved from 47/39)
- `eval_ok=57`, `eval_runtime_error=6`, `eval_timeout=7` (more files now reach runtime)

Net parser gain:
- `+23` additional files parse successfully.

## Strict-Spec Runtime Semantics Pass (Same Day Follow-up)
Implemented 1.2/1.3-aligned runtime behavior updates:
- Function scope isolation: functions no longer capture outer block variables.
- Function return behavior:
  - `GTFO` inside function now returns `NOOB` (unless inside loop/switch where it still breaks nearest construct).
  - Falling off the end of a function/method returns current `IT`.
- `IT` side effects tightened:
  - `I HAS A ...` declarations no longer update `IT`.
  - `R` assignment statements no longer update `IT`.
- Loop counter scoping semantics aligned:
  - `UPPIN/NERFIN YR var` counter is temporary/local to loop.
  - If outer `var` exists, loop counter starts from that value (without mutating outer binding).
  - If outer `var` is absent, loop counter starts at `0` and does not leak after loop.
- `WTF?` case semantics tightened:
  - Duplicate `OMG` literals now produce an explicit runtime error.
  - `OMG` branches are parser-restricted to literals (`NUMBER`, `STRING`, `WIN`, `FAIL`, `NOOB`) per strict 1.2 behavior.
- YARN Unicode escape support added:
  - `:(<hex>)` now decodes to Unicode code points in string literals.
  - Invalid code points (including out-of-range/surrogates) now raise lexical errors.

Post-pass tier2 snapshot:
- `lex_ok=86`, `lex_fail=2`
- `parse_ok=70`, `parse_fail=16`
- `eval_ok=57`, `eval_runtime=7`, `eval_timeout=6`

Notable runtime shift:
- One corpus program moved from timeout to concrete runtime error (`unknown identifier: MEMLIMIT`), which is useful for triage and consistent with stricter scope semantics.

## Dominant Failure Modes (Initial Baseline)

### Parse failures by repo
- `loco`: 15
- `lolcode-py-cmsc124`: 12
- `lolcode-py-sada`: 9
- `lol-ruby`: 3

### Parse signatures (normalized)
- `unexpected NEWLINE after HAI`: 36/39 parse failures (dominant)
- Other isolated parse failures:
  - newline after long `ALL OF ...` form (likely missing/variant terminator handling)
  - `unexpected GTFO` in one sample

### Runtime errors by repo
- `loleuler`: 1
- `lokalise-lol-post`: 1
- `httpd-lol`: 1
- `httpd.lol`: 1
- `lolcode-py-cmsc124`: 1

### Runtime signatures (normalized)
- `unknown function: SOCKS'Z BIND` (2) -> 1.4/extension out-of-scope for current target
- `unknown identifier: COLOR` (1) -> 1.4/extension out-of-scope for current target
- `remainder: division by zero` (1)
- `/: division by zero` (1)

### Timeouts
- `loleuler`: 5 (heavy programs)

## Remaining Failure Modes After Parser Compatibility Pass

### Parse failures by repo
- `lolcode-py-sada`: 9
- `lolcode-py-cmsc124`: 3
- `lol-ruby`: 2
- `loco`: 2

### Parse signatures (normalized)
- `unexpected I` on indented `I HAS A ...` lines (dominant)
- `unexpected OF` on arithmetic expression forms in `lolcode-py-cmsc124`
- isolated dialect/shape issues: `IZ VAR ...`, `LOL VAR ...`, `VISIBLE ... !`, one `GTFO` placement case

### Runtime signatures (normalized)
- `unknown function: SOCKS'Z BIND` (2) -> out-of-scope 1.4 extension
- `unknown identifier: COLOR` (1) -> out-of-scope 1.4 extension
- `/: division by zero` (2)
- `remainder: division by zero` (1)

### Timeouts
- `loleuler`: 5
- `loco`: 1

## Priority Recommendations (1.2/1.3 Scope)
1. Parser robustness for indentation-sensitive/variant statement forms in `lolcode-py-*` corpora:
   - Remaining dominant parse signatures are `unexpected I` on indented `I HAS A ...` lines.
2. Parser compatibility for alternate dialect constructs:
   - `lol-ruby` samples include non-standard forms (`IZ VAR ...`, `LOL VAR R ...`) not in 1.2/1.3 grammar.
3. Loco-specific syntax variants:
   - Remaining issues include `VISIBLE ... !` placement and one loop/header style edge case.
4. Runtime arithmetic guards:
   - Confirm desired behavior/messages for divide/mod by zero in 1.2/1.3 mode.

## Deferred (Out-of-Scope for Current Pass)
- `COLOR` behavior
- `SOCKS*` import/bind behavior
- Other 1.4 ersatz extension surface forms

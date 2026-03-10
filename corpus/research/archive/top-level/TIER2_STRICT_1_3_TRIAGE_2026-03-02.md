# Tier2 Strict-1.3 Triage Snapshot

Generated: 2026-03-02
Source: `corpus/research/tier2-eval-classified.json`

## Current breakdown (likely programs only)

- Likely programs: `184`
- Pass (`ok`): `11`
- Failures: `173`

Failure buckets:

- Out-of-scope (version/header/dialect/extension): `165`
- Invalid input (unterminated strings): `6`
- Candidate 1.3 implementation gaps: `2`

Bucket details:

- `107` out-of-scope/missing-or-nonstandard-hai-header
- `46` out-of-scope/version
- `6` out-of-scope/dialect-syntax
- `6` invalid-input/unterminated-string
- `4` out-of-scope/nonstandard-hai-metadata
- `2` out-of-scope/extension-or-invalid-token
- `2` candidate-gap/expression-statement-before-O-RLY

## Candidate 1.3 gaps (current)

1. Expression statement form missing in parser (slot-read statement before `O RLY?`):
   - `corpus/tier2/flag-wars-3-lolcode/files/main.lol`
   - `corpus/tier2/flag-wars-3-lolcode/files/src/main.lol`

Observed errors:

- `parse-source: syntax error: unexpected NEWLINE at line 167, col 37`
- `parse-source: syntax error: unexpected NEWLINE at line 114, col 29`

Interpretation:

- Programs use a bare expression statement (`playerBullet'Z alive`) to set `IT`,
  then immediately branch with `O RLY?`.
- Current parser/runtime only partially supports statement-position expressions,
  which is consistent with the known limitation in
  `corpus/research/SPEC_1_2_1_3_IMPLEMENTATION_STATUS.md`.

## Trend across recent snapshots

For identical tier2 size (`223` files, `184` likely programs):

| Snapshot | ok | failures | out-of-scope | invalid-input | candidate-gap |
|---|---:|---:|---:|---:|---:|
| `tier2-eval-classified-fresh.json` | 11 | 173 | 156 | 6 | 11 |
| `tier2-eval-classified-after-method-syntax.json` | 11 | 173 | 156 | 6 | 11 |
| `tier2-eval-classified-after-dynamic-calls.json` | 8 | 176 | 164 | 6 | 6 |
| `tier2-eval-classified-after-slot-target-fix.json` | 11 | 173 | 165 | 6 | 2 |
| `tier2-eval-classified.json` (current) | 11 | 173 | 165 | 6 | 2 |

Key point:

- Actionable strict-1.3 gaps dropped from `11` to `2`.
- Remaining failures are mostly intentional strict-scope rejects, not core parser/runtime defects.

## Top 5 actionable parser/runtime items

1. Add full statement-position expression support (`stmt-expr`) in parser, not only call statements.
2. Ensure `stmt-expr` always evaluates expression and writes result into `IT`.
3. Add regression tests for slot-expression-before-`O RLY?` in both inline and newline/comma-separated forms.
4. Re-run tier2 classifier after (1)-(3) and confirm `flag-wars-3` parse failures move to either `ok` or a new concrete runtime diagnosis.
5. Keep strict policy gates explicit in classifier/docs so out-of-scope noise stays separated from real 1.3 regressions.

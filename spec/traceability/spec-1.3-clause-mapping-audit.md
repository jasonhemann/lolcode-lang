# Spec 1.3 Clause-to-Matrix Recalculation Audit

Date: 2026-03-05

## Method

- Re-extracted clause index from `spec/upstream/lolcode-spec-v1.3.md` using updated extractor logic in `scripts/extract_spec_clauses.rkt`.
- Clause index now records all non-empty lines outside fenced code (`heading`, `bullet`, `normative`, `prose`) and fenced code lines (`syntax`, `code`).
- Recomputed coverage by matching matrix `source-line` values in `spec/traceability/spec-1.3-matrix.rktd` against extracted clause lines.
- For strict clause gap accounting, used `kind=normative` rows.

## Summary

- Matrix entries: 61
- Unique matrix source lines: 60
- Extracted 1.3 clause rows: 573
- Extracted 1.3 normative rows: 65
- Normative rows mapped by matrix source line: 45
- Normative rows not mapped by matrix source line: 20

## Unmapped 1.3 Normative Clauses: Adjudication Ledger

All currently unmapped normative lines are now adjudicated as exactly one of:
- `new row` (explicit matrix row added)
- `merged` (line is semantically covered by one or more existing rows)
- `example-only` (syntax-introducer/example line with no independent semantic requirement)

| Line | Disposition | Resolution |
|---|---|---|
| 50 | merged | Covered by `comment.single-line-btw` (`source-line` 48) + lexer tests in `tests/spec/runtime-core-test.rkt`. |
| 67 | merged | Covered by `comment.block-obtw-tldr` (`source-line` 65) + unterminated block-comment negative test. |
| 241 | merged | Covered by `string.ignore-line-control-inside-yarn` (`source-line` 42) plus unterminated-string lexer failure tests in `tests/spec/parse-negative-test.rkt`. |
| 269 | merged | Covered by `op.prefix-nesting-composition` (`303`) + `op.mkay-variadic-form` (`286`). |
| 271 | example-only | Introduces unary syntax block; independent unary semantics are already covered by operator rows and tests. |
| 283 | example-only | Introduces variadic syntax block; independent closure semantics covered by `op.mkay-variadic-form`. |
| 324 | merged | Covered by `cast.implicit-operator-cast-errors` (`360`) and logic/comparison runtime regressions in `tests/spec/runtime-core-test.rkt`. |
| 346 | example-only | IT idiom prose; semantic rule is captured by `flow.expr-stmt-it-local-scope` (`407`). |
| 391 | merged | Syntax introducer for `GIMMEH`; semantics covered by `io.gimmeh` (`394`). |
| 582 | merged | Fixed-arity/single-word argument behavior covered by `fn.definition-call` (`574`) + parser arg-shape restrictions in tests. |
| 588 | merged | Return-introducer prose covered by `fn.return-semantics` (`590`). |
| 596 | merged | Call-syntax introducer prose covered by `fn.definition-call` (`574`) + `fn.call-i-namespace-marker` (`604`). |
| 612 | merged | Container/slot domain prose covered by `bukkit.declaration` (`619`) + `bukkit.slot-access` (`738`). |
| 616 | merged | Empty-object creation introducer covered by `bukkit.declaration` (`619`). |
| 678 | example-only | Inline explanatory comment in spec example; no separate normative rule. |
| 680 | example-only | Inline explanatory comment in spec example; no separate normative rule. |
| 741 | merged | Method call syntax introducer covered by `bukkit.slot-access` (`738`) and call regressions. |
| 770 | new row | Added `bukkit.special-slot-izmakin-hook` (`source-line` 770) with runtime regression in `tests/spec/runtime-core-test.rkt`. |
| 774 | merged | Prototype-object creation syntax introducer covered by `bukkit.parent-slot-prototype-link` (`790`). |
| 782 | merged | Alternate inheritance syntax introducer covered by `bukkit.alt-syntax` (`709`) + inheritance rows (`790`/`798`). |
| 810 | merged | Restatement/example line for receiver-based slot-function lookup, covered by `bukkit.slot-function-receiver-lookup` (`804`). |

## 1.2 \ 1.3 Normative Delta (text-normalized)

Derived by normalized text set difference over extracted `kind=normative` rows:

- 1.2 line 81: All LOLCODE programs must be opened with the command `HAI`. `HAI` should then be followed with the current LOLCODE language version number (1.2, in this case). There is no current standard behavior for implementations to treat the version number, though.
- 1.2 line 99: Variable identifiers may be in all uppercase or lowercase letters (or a mixture of the two). They must begin with a letter and may be followed only by other letters, numbers, and underscores. No spaces, dashes, or other symbols are allowed. Variable identifiers are CASE SENSITIVE – "cheezburger", "CheezBurger" and "CHEEZBURGER" would all be different variables.

Both 1.2-only normative lines are semantically represented in the current 1.3 matrix via:

- Program envelope/version handling (`program.envelope-hai-kthxbye`, `program.version-handling`)
- Identifier naming constraints (`var.identifier-shape`)

## Notes

- The 20 unmapped 1.3 normative lines are now fully adjudicated in the table above.
- Remaining unmapped lines are intentionally `merged` or `example-only`; no unresolved normative clause is left unclassified.
- This audit is intended to drive matrix refinement; it is stricter and broader than the previous clause-index extraction.

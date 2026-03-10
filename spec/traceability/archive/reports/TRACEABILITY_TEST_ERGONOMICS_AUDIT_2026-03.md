# Checklist Test Pair + Ergonomics Audit

Date: 2026-03-05

## Item 45: Positive/Negative Pair Coverage (01-43)

Legend:
- `paired`: explicit positive and negative coverage exists.
- `non-erroring`: clause is behavioral/non-erroring by nature; positive-only is expected.

| Item | Status       | Evidence anchor                                                                                                                         |
|------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| 01   | paired       | `tests/spec/runtime-core-test.rkt` comma+continuation execution; `tests/spec/parse-negative-test.rkt` malformed continuation placement. |
| 02   | paired       | continuation/comment positives and empty-line/marker negatives in `parse-negative-test.rkt`.                                            |
| 03   | paired       | one-line minimal positive + one-line malformed negatives (`parse-negative-test.rkt`).                                                   |
| 04   | paired       | `MAEK ... AS ...` negative and `AS`-identifier positive (`parse-negative-test.rkt`).                                                    |
| 05   | non-erroring | scope adjudication semantics exercised by runtime scope tests (local vs method IT).                                                     |
| 06   | paired       | duplicate declare/function collisions negative + assignment-overwrite positive (`runtime-core-test.rkt`).                               |
| 07   | non-erroring | `R NOOB` semantic behavior validated with positive binding/reference tests.                                                             |
| 08   | non-erroring | primitive immutability validated by positive no-mutation behavior test.                                                                 |
| 09   | paired       | optional `A` positives + required-article negatives (`parse-negative-test.rkt`).                                                        |
| 10   | paired       | declared assignment positive + undeclared assignment runtime-error negative (`runtime-core-test.rkt`).                                  |
| 11   | non-erroring | wording adjudication; behavior validated through full BUKKIT section tests.                                                             |
| 12   | paired       | positive TYPE/NOOB TROOF casts + cast-form rejection negatives.                                                                         |
| 13   | paired       | numeric truncation positives + malformed numeric literal negatives.                                                                     |
| 14   | paired       | valid escape positives + invalid codepoint/normative-name negatives.                                                                    |
| 15   | non-erroring | TYPE-domain cast behavior is positive semantic mapping.                                                                                 |
| 16   | paired       | nested variadic positive closure + malformed variadic parse negatives.                                                                  |
| 17   | paired       | omitted-`AN` positives + `AND` separator negatives.                                                                                     |
| 18   | paired       | equality/cast positives + strict no-implicit-cast equality negatives.                                                                   |
| 19   | non-erroring | local-cast-only behavior validated via positive non-mutation tests.                                                                     |
| 20   | non-erroring | declaration initializer-type behavior validated by positive inference tests.                                                            |
| 21   | paired       | continued `VISIBLE` positives + malformed delimiter/continuation negatives.                                                             |
| 22   | paired       | local IT/global-method-IT positives + invalid-context failures (`FOUND YR`/`GTFO`) negatives.                                           |
| 23   | paired       | canonical lvalue positives + non-lvalue assignment parse negatives.                                                                     |
| 24   | paired       | implicit-IT and branch-order positives + malformed `O RLY?` structure negatives.                                                        |
| 25   | paired       | escaped-placeholder positive + interpolated OMG literal negative.                                                                       |
| 26   | non-erroring | runtime propagation and empty-OMG behavior are positive semantic checks.                                                                |
| 27   | non-erroring | loop updater temp-scope behavior validated by positive non-leak tests.                                                                  |
| 28   | paired       | canonical arg-name positives + dynamic arg-name parse negatives.                                                                        |
| 29   | non-erroring | return semantics (`GTFO` => NOOB, implicit IT) are positive semantic checks.                                                            |
| 30   | paired       | canonical `I IZ` calls positive + malformed call-shape parse negatives.                                                                 |
| 31   | paired       | slot redeclare overwrite positive + slot declaration article negatives.                                                                 |
| 32   | paired       | canonical method definitions positive + nested method-def negative (strict).                                                            |
| 33   | paired       | lookup-order positive + missing/non-callable method negatives.                                                                          |
| 34   | paired       | `ME HAS A` positive + `ME` outside method negative.                                                                                     |
| 35   | non-erroring | inheritance/parent mutation behavior validated via positive semantic tests.                                                             |
| 36   | paired       | dynamic slot/method positives + missing/non-callable slot-call negatives.                                                               |
| 37   | non-erroring | dynamic method name (`SRS`) is positive semantic behavior.                                                                              |
| 38   | paired       | custom/default `omgwtf` behavior positives + missing-slot default error negative.                                                       |
| 39   | non-erroring | reparenting/cycle safety are positive behavioral checks.                                                                                |
| 40   | paired       | copy-on-write positive + inherited unknown-name assignment negative.                                                                    |
| 41   | non-erroring | receiver-projected slot-function lookup is positive behavioral rule.                                                                    |
| 42   | non-erroring | spec funkin/prefix behavior and assignment variant are positive semantic checks.                                                        |
| 43   | non-erroring | reverse-order mixin + static snapshot behavior are positive semantic checks.                                                            |

## Item 46: AST/Runtime Ergonomics Findings

### What stayed compositional

- Most semantics additions were local to `compile-expr` / `compile-stmt` branches in `src/lolcode/runtime.rkt` without parser surgery.
- Receiver-projected slot-function dispatch was implemented as runtime adaptation logic (`project-receiver-slot-frame` + sync-back), not grammar hacks.
- Strict-1.3 policy constraints (nested-def rejection, reserved-token identifiers) are parser checks isolated in `src/lolcode/parser.rkt`.

### Highest-friction points

1. Lvalue shape validation still mixes parser and runtime invariants.
   - Follow-up: split parser nonterminals into assignment-target vs general expression for fewer runtime shape guards.
2. Method/slot callable invocation paths still have near-duplicate adaptation branches.
   - Follow-up: unify into one internal callable protocol with explicit receiver strategy.
3. Clause traceability maintenance is manual.
   - Follow-up: generate a line->row adjudication report from matrix + clause index as a CI artifact.

### Net assessment

- No broad parser hacks were needed for the recent tranche.
- Most implementation pressure sits in runtime call adaptation and traceability bookkeeping, not AST expressiveness.

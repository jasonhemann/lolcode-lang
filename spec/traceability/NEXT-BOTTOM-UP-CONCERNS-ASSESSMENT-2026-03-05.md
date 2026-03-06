# Assessment: Next Bottom-Up Spec Concerns

Date: 2026-03-05  
Inputs checked:
- `NEXT-BOTTOM-UP-SPEC-CONCERNS-2026-03-05.md`
- `spec/upstream/lolcode-spec-v1.3.md`
- `tests/spec/runtime-core-test.rkt`
- `tests/spec/parse-negative-test.rkt`
- `tests/spec/spec-audit/known-gaps-failing-test.rkt`
- `spec/traceability/spec-1.3-matrix.rktd`

Status legend:
- `OK`: implemented and covered by targeted tests.
- `AMB`: spec text is ambiguous/conflicting; behavior is an adjudicated policy.
- `PART`: implemented but test coverage is incomplete for the specific edge.
- `GAP`: known divergence or missing behavior.

## Summary

- Total concerns reviewed: `48`
- `OK`: `25`
- `AMB` (policy-backed, currently acceptable): `8`
- `PART` (needs sharper tests/clarification): `14`
- `GAP`: `1`

Primary concrete gap:
- `#35` `MAEK` currently allows `BUKKIT` cast; strict 1.3 cast target set is `TROOF|YARN|NUMBR|NUMBAR|NOOB`.

Update delta (2026-03-06):
- `#35` is now resolved: parser rejects non-spec cast targets in `MAEK` and `IS NOW A` forms, and runtime no longer supports legacy `MAEK ... BUKKIT` cast behavior.
- Added targeted regressions in `tests/spec/parse-negative-test.rkt` and equality-policy coverage for complex values in `tests/spec/runtime-core-test.rkt`.
- `#3` now has explicit mutable-value coverage: mixin slot copy is adjudicated as shallow aliasing for BUKKIT slot values (call-by-sharing), with regression coverage.
- `#12`/`#13` `omgwtf` edge behavior is now pinned with explicit regressions: memoization under stateful mutation, return-value-vs-intermediate-mutation precedence, and deterministic same-slot re-entry error.
- Strict-case audit completed: removed residual case-insensitive keyword/type/literal/comment handling in runtime paths and added regressions for lowercase lookalike behavior.
- `#11` is now policy-pinned as expression-argument method calls (matching call-expression semantics); `#14`/`#15` now have explicit izmakin ordering and reentrancy coverage.
- `#25`/`#26`/`#30` are now resolved: side-effect call-argument ordering is pinned (`I IZ` and `<object> IZ`), loop update/condition ordering is matrix-covered for `UPPIN/NERFIN x TIL/WILE`, and `WTF?` duplicate/match equality now uses numeric-mode comparison for numeric pairs (`1` vs `1.0`) with non-coercing mixed-type behavior preserved.
- NUMBAR->YARN printing policy is now explicitly pinned to spec line 235 wording: truncate to a default maximum of two decimal places without forced zero-padding, and treat default precision as the only available mode in strict 1.3 (no precision-control syntax exists).

## Item-by-item results

| # | Status | Assessment |
|---|---|---|
| 1 | AMB + PART | Spec conflict (`849` vs `857/871-873`) on whether mixins include inherited slots; runtime copies own slots (`copy-own-into!`) only; no explicit inherited-slot mixin test. |
| 2 | OK | Reverse-order mixin precedence and parent replacement are implemented and tested (`mixin-object-src`, `mixin-parent-child-combo-src`). |
| 3 | AMB + OK | Copy depth remains spec-underdetermined, but policy is now explicit and tested: primitive slots are copied statically, while mutable BUKKIT slot values remain aliased (shallow copy). |
| 4 | AMB + PART | Non-BUKKIT `parent` mutation behavior is not specified; runtime treats non-object parent as chain termination; no dedicated spec test. |
| 5 | PART | Cycle-safe lookup is tested (`parent-cycle-lookup-terminates-src`), but explicit assignment-path behavior in cyclic graphs is not separately targeted. |
| 6 | OK | Copy-on-write assignment to inherited names is implemented and tested (`inherited-method-slot-independence-src`, `inherited-assignment-unknown-name-src`). |
| 7 | PART | Function-valued inherited slot assignment edge lacks direct test coverage. |
| 8 | PART | Special slots exist and are exercised (`parent`, `omgwtf`, `izmakin`), but full inheritance/shadow interaction matrix is not explicitly tested. |
| 9 | OK | Receiver-projected slot-function scope is implemented and tested (`slot-function-receiver-namespace-src`, `slot-function-receiver-assignment-src`). |
| 10 | OK | Dynamic method names via `SRS` are parsed and executed (`method-alt-call-dynamic-name-src`). |
| 11 | AMB + OK | Method-call arg wording conflicts with function-call expression prose; policy is expression-argument acceptance for coherence, now pinned with explicit method expression-arg regression. |
| 12 | OK | `omgwtf` fallback memoization is explicitly tested under stateful mutation and return-value precedence for synthesized slot values. |
| 13 | AMB + OK | Spec is underdetermined on `omgwtf` recursion; project policy now raises deterministic runtime error on same-slot re-entry, with regression coverage. |
| 14 | OK | `izmakin` ordering is explicitly tested: hook observes fully prototyped post-mixin object with declared parent restoration applied. |
| 15 | AMB + OK | Spec is underdetermined on `izmakin` reentrancy; policy allows reentrant prototype creation, with regression confirming per-prototype hook execution. |
| 16 | PART | `O HAI IM` slot-first lookup vs lexical local lookup inside object block is not directly isolated in tests. |
| 17 | OK | Parser/runtime separate `I` forms correctly in object block context (`object-alt-src`, method alt-def/call tests). |
| 18 | PART | `ME` outside method is tested negative and normal use is tested positive; nested helper-call context semantics remain untested. |
| 19 | OK | Method lookup order and namespace shadowing are covered (`method-lookup-order-src`, `method-shadow-src`). |
| 20 | OK | Parser distinguishes `HOW IZ I` and `HOW IZ <receiver> <slot>` forms; both families are covered in tests. |
| 21 | OK | Numeric slot-key path through `SRS` is covered (`bukkit-srs-numeric-slot-src`); parser supports identifier and `SRS` slot specs. |
| 22 | AMB | "current object's scope" wording is vague at top-level; current behavior is stable and tested with top-level bukkit declarations. |
| 23 | OK | `GTFO` precedence across function/switch/loop contexts is strongly covered (`function-gtfo-return-src`, `switch-break-inside-loop-src`, `function-switch-gtfo-scope-src`). |
| 24 | AMB | Spec line `584` conflicts with later method/global scope rules; current behavior is policy-backed and tested (`function-outer-scope-src`, `method-global-capture-src`). |
| 25 | OK | Call argument evaluation ordering is now pinned with side-effect regressions for both `I IZ` and `<object> IZ` paths (arguments evaluated before body entry, left-to-right). |
| 26 | OK | Loop condition/update ordering is now pinned by explicit updater/condition matrix coverage (`UPPIN/NERFIN` x `TIL/WILE`) confirming pre-body condition check and post-body updater execution. |
| 27 | OK | Loop updater temporary/local shadowing and restoration are well covered (`loop-counter-scope-src`, `loop-counter-no-leak-src`, `loop-counter-dynamic-name-src`). |
| 28 | AMB + OK | Dynamic labels via `SRS` are supported and tested (`loop-dynamic-label-src`, mismatch case). Spec leaves this under-specified. |
| 29 | OK | Nested infinite-loop termination controls are covered (`switch-break-inside-loop-src`, nested loop tests). |
| 30 | OK | `WTF?` duplicate literals and runtime matching now follow numeric-mode equality for numeric pairs (`1` duplicates/matches `1.0`) while preserving non-coercing mixed-type behavior (`\"1\"` distinct from `1`). |
| 31 | OK | Fallthrough plus default gating is now explicit: matched `OMG` cases may fall through subsequent `OMG` blocks but do not run `OMGWTF` when any `OMG` matched. |
| 32 | OK | IT local vs method-global lookup split is explicitly tested (`it-local-main-and-function-src`, `method-it-global-lookup-src`). |
| 33 | OK | Optional `AN` ambiguity and reserved-token handling are tested (`and-as-identifier-*`, reserved keyword negatives). |
| 34 | OK | EOL-based variadic closure in nested contexts is covered (`nested-variadic-closure-src`, known-gaps variadic regression test). |
| 35 | OK (resolved 2026-03-06) | Parser now rejects non-spec cast target designators for both `MAEK` and `IS NOW A`; runtime `cast-value` no longer accepts `BUKKIT` as cast target. |
| 36 | AMB + OK | Numeric bounds/precision are host-defined by spec; implementation intentionally follows Racket numeric model; formatting/truncation tested. |
| 37 | OK (resolved 2026-03-06) | Strict cast grammar now has direct negative coverage for malformed numeric forms (spaced sign, scientific notation, and leading-plus literals), matching spec numeric lexical constraints. |
| 38 | PART | `SRS` support is broad and tested in many positions; boundary cases (all "identifier positions") still not exhaustively enumerated. |
| 39 | OK | Comma-inline `OBTW/TLDR` examples are now pinned with direct runtime regression, and strict parser rejection is pinned for `TLDR` trailing statements without comma/newline. |
| 40 | PART | Unicode normative-name escape path is implemented with `codepoint` table and core tests, but alias/normalization edge coverage is limited. |
| 41 | OK | Version-policy gap is explicitly handled and tested (`unsupported-v12`, `unsupported-v14`, external strict triage partition docs). |
| 42 | OK | Distinction between variable declaration and slot declaration in object contexts is covered (object/block + slot-set parse/runtime tests). |
| 43 | OK | `HOW IZ I` vs `HOW IZ <object> <slot>` distinction is covered by parser/runtime tests for both definitions. |
| 44 | OK | `I IZ` vs `<object> IZ` call forms are covered by function and method call tests. |
| 45 | OK | Variable-lvalue vs slot-lvalue assignment split is covered (`assignment-*` negatives + slot assignment positives). |
| 46 | OK | `SMOOSH` expression vs mixin-constructor parse forms are both covered and disambiguated in tests. |
| 47 | OK | `GTFO` context-sensitive semantics are covered (outside-context negatives + nested-control positives). |
| 48 | OK | IT temporary vs method-global IT behavior is explicitly covered and stable. |

## Recommended next actions (ordered)

1. Done (2026-03-06): fixed/adjudicated `#35` (`MAEK ... BUKKIT`) and added strict regressions.
2. Continue targeted tests for mixin source-set ambiguity (`#1`); `#3` depth policy is now adjudicated/tested.
3. Done (2026-03-06): added explicit memoization + recursion-behavior tests for `omgwtf` (`#12`, `#13`).
4. Done (2026-03-06): added ordering/reentrancy tests for `izmakin` (`#14`, `#15`).
5. Continue parser/runtime tests for remaining partial syntax intersections (`#37`, `#38`, `#40`).

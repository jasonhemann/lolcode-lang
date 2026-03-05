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

## Item-by-item results

| # | Status | Assessment |
|---|---|---|
| 1 | AMB + PART | Spec conflict (`849` vs `857/871-873`) on whether mixins include inherited slots; runtime copies own slots (`copy-own-into!`) only; no explicit inherited-slot mixin test. |
| 2 | OK | Reverse-order mixin precedence and parent replacement are implemented and tested (`mixin-object-src`, `mixin-parent-child-combo-src`). |
| 3 | PART | Copy depth (shallow/deep) is under-specified; runtime is shallow for object/function values; tests only confirm static snapshot for primitive slot values. |
| 4 | AMB + PART | Non-BUKKIT `parent` mutation behavior is not specified; runtime treats non-object parent as chain termination; no dedicated spec test. |
| 5 | PART | Cycle-safe lookup is tested (`parent-cycle-lookup-terminates-src`), but explicit assignment-path behavior in cyclic graphs is not separately targeted. |
| 6 | OK | Copy-on-write assignment to inherited names is implemented and tested (`inherited-method-slot-independence-src`, `inherited-assignment-unknown-name-src`). |
| 7 | PART | Function-valued inherited slot assignment edge lacks direct test coverage. |
| 8 | PART | Special slots exist and are exercised (`parent`, `omgwtf`, `izmakin`), but full inheritance/shadow interaction matrix is not explicitly tested. |
| 9 | OK | Receiver-projected slot-function scope is implemented and tested (`slot-function-receiver-namespace-src`, `slot-function-receiver-assignment-src`). |
| 10 | OK | Dynamic method names via `SRS` are parsed and executed (`method-alt-call-dynamic-name-src`). |
| 11 | AMB + PART | Method-call arg grammar says `<variable>` in one place but function-call section allows expressions; parser currently allows expressions; coverage is positive-only. |
| 12 | PART | `omgwtf` missing-slot fallback is tested, but current tests do not explicitly prove memoization/caching behavior under stateful hook. |
| 13 | PART | `omgwtf` recursion hazard remains unspecified and untested. |
| 14 | PART | `izmakin` hook execution is tested, but relative ordering with mixin copy / parent finalization is not explicitly pinned by tests. |
| 15 | PART | `izmakin` reentrancy/recursive prototyping behavior is untested. |
| 16 | PART | `O HAI IM` slot-first lookup vs lexical local lookup inside object block is not directly isolated in tests. |
| 17 | OK | Parser/runtime separate `I` forms correctly in object block context (`object-alt-src`, method alt-def/call tests). |
| 18 | PART | `ME` outside method is tested negative and normal use is tested positive; nested helper-call context semantics remain untested. |
| 19 | OK | Method lookup order and namespace shadowing are covered (`method-lookup-order-src`, `method-shadow-src`). |
| 20 | OK | Parser distinguishes `HOW IZ I` and `HOW IZ <receiver> <slot>` forms; both families are covered in tests. |
| 21 | OK | Numeric slot-key path through `SRS` is covered (`bukkit-srs-numeric-slot-src`); parser supports identifier and `SRS` slot specs. |
| 22 | AMB | "current object's scope" wording is vague at top-level; current behavior is stable and tested with top-level bukkit declarations. |
| 23 | OK | `GTFO` precedence across function/switch/loop contexts is strongly covered (`function-gtfo-return-src`, `switch-break-inside-loop-src`, `function-switch-gtfo-scope-src`). |
| 24 | AMB | Spec line `584` conflicts with later method/global scope rules; current behavior is policy-backed and tested (`function-outer-scope-src`, `method-global-capture-src`). |
| 25 | PART | Arg evaluation before call is implemented (`fn.call-args-evaluated-before-call` row), but explicit side-effect ordering tests are sparse. |
| 26 | PART | Loop condition/update order appears correct from current loop tests, but no direct off-by-one assertion matrix for all updater forms. |
| 27 | OK | Loop updater temporary/local shadowing and restoration are well covered (`loop-counter-scope-src`, `loop-counter-no-leak-src`, `loop-counter-dynamic-name-src`). |
| 28 | AMB + OK | Dynamic labels via `SRS` are supported and tested (`loop-dynamic-label-src`, mismatch case). Spec leaves this under-specified. |
| 29 | OK | Nested infinite-loop termination controls are covered (`switch-break-inside-loop-src`, nested loop tests). |
| 30 | PART | Duplicate `OMG` literal checks exist (`duplicate-wtf-case-literal`), but mixed-type equality-mode edge cases are not explicitly tested. |
| 31 | PART | Fallthrough behavior is tested, but explicit "matched case must not run `OMGWTF`" target test is missing. |
| 32 | OK | IT local vs method-global lookup split is explicitly tested (`it-local-main-and-function-src`, `method-it-global-lookup-src`). |
| 33 | OK | Optional `AN` ambiguity and reserved-token handling are tested (`and-as-identifier-*`, reserved keyword negatives). |
| 34 | OK | EOL-based variadic closure in nested contexts is covered (`nested-variadic-closure-src`, known-gaps variadic regression test). |
| 35 | GAP | Runtime currently accepts `MAEK ... A BUKKIT`; strict 1.3 cast target text excludes BUKKIT (`365-368`). Needs adjudication/fix. |
| 36 | AMB + OK | Numeric bounds/precision are host-defined by spec; implementation intentionally follows Racket numeric model; formatting/truncation tested. |
| 37 | PART | Strict cast grammar rejects known bad forms (spaces/scientific), but edge matrix (e.g. plus-sign forms) is not exhaustive. |
| 38 | PART | `SRS` support is broad and tested in many positions; boundary cases (all "identifier positions") still not exhaustively enumerated. |
| 39 | PART | Block comment behavior is tested, but comma-inline `OBTW/TLDR` examples are not directly isolated as regressions. |
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

1. Fix or adjudicate `#35` (`MAEK ... BUKKIT`) and add strict regression.
2. Add targeted tests for mixin source-set/depth ambiguities (`#1`, `#3`).
3. Add explicit memoization + recursion-behavior tests for `omgwtf` (`#12`, `#13`).
4. Add ordering tests for `izmakin` vs mixin/parent finalize (`#14`, `#15`).
5. Add parser/runtime tests for remaining partial syntax intersections (`#11`, `#31`, `#39`).

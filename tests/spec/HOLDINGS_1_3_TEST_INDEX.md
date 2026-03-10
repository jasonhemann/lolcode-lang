# LOLCODE 1.3 Holdings Test Index

This index wires archival holdings (H01..H16) to concrete regression tests.
Primary runtime tests live in `tests/spec/runtime-core-test.rkt`.
Grammar/parse policy tests for H08 also reference `tests/spec/parse-negative-test.rkt`.

| Holding | Focus | Primary test IDs |
| --- | --- | --- |
| H01 | Distinct `I IZ` vs `<object> IZ` forms | `ast-function-vs-method-def-shape`, `method-defs-are-slot-callables` |
| H02 | Methods are slot values (no separate namespace) | `method-defs-are-slot-callables`, `function-storage` |
| H03 | Receiver-dynamic slot-call semantics | `slot-function-receiver-namespace`, `mixin-copied-function-receiver-late-binding` |
| H04 | Object-body `I HAS A` is object-local | `top-level-object-scope-does-not-leak`, `object-body-redeclare-overwrite-does-not-mutate-outer` |
| H05 | Bare method `IT` vs receiver slot `IT` distinction | `method-bare-it-distinct-from-slot-it`, `method-fallthrough-it-vs-slot-it` |
| H06 | Plain `BUKKIT` defaults `parent = NOOB` | `bukkit-default-parent-noob` |
| H07 | Parent-chain cycle safety + copy-on-write assignment | `parent-cycle-assignment-existing-name-copy-on-write`, `inherited-function-slot-assignment-copy-on-write`, `inherited-assignment-unknown-name` |
| H08 | Declaration/prototype grammar preserved as written | `mixin-declare` (parse-negative), `invalid-plain-a-parent-declare` (parse-negative) |
| H09 | Mixin source-set includes effective-visible; reverse-order static copy | `mixin-object`, `mixin-source-own-only-slots`, `mixin-source-own-only-methods`, `mixin-static-snapshot` |
| H10 | Special-slot copying with parent restoration | `mixin-special-parent-restored`, `mixin-special-omgwtf-copied`, `mixin-special-izmakin-copied` |
| H11 | `omgwtf` zero-arity, one-shot miss hook, memoized synthesis | `omgwtf-nonzero-arity-rejected`, `omgwtf-memoizes-missing-slot`, `method-call-miss-omgwtf-after-full-chain` |
| H12 | Slot-call on non-function after synthesis remains callable/type error | `method-call-noncallable-after-omgwtf-synthesis` |
| H13 | `izmakin` runs after full prototyping and parent restoration | `izmakin-ordering-parent-restore` |
| H14 | Bare function identifiers are values, not implicit calls | `function-storage`, `function-identifier-value-binding` |
| H15 | No true lexical closures; receiver-backed closure-like behavior only | `method-local-not-captured-by-global-function`, `extracted-slot-function-direct-call-namespace`, `slot-function-receiver-namespace` |
| H16 | `SMOOSH` eager/strict, no rollback of earlier side effects | `smoosh-eager-side-effect-before-error` |

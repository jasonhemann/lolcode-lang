# Tranche 1 Adjudication (Kickoff)

Date: 2026-03-06
Source list: `NEXT-BOTTOM-UP-SPEC-CONCERNS-2026-03-05.md`
Policy: `spec/traceability/SPEC_ADJUDICATION_POLICY.md`

Tranche 1 targets: `N02`, `N10`-`N15`, `N20`-`N24`, `N27`, `N34`.

## Decisions Started

1. `N02` (Call-form AST split)
Status: `adjudicated`
Decision: Keep distinct AST/runtime paths for `I IZ` and `<object> IZ`; no desugaring collapse.
Reason: receiver semantics and `ME` access differ by call form.

2. `N10` (Scope contradiction)
Status: `adjudicated`
Decision: Treat object-function lookup clauses as feature-specific override to broad early scope prose.
Reason: dedicated function-in-bukkit section is more specific and operational.

3. `N11` (No-closure vs object/global fallback)
Status: `adjudicated`
Decision: Ordinary functions do not capture lexical outer locals; method/slot-call path follows object-aware lookup.
Reason: keeps both clauses coherent with minimal extra machinery.

4. `N12` (`IT` local vs global-in-method)
Status: `adjudicated`
Decision: `IT` is local in ordinary scopes but method lookup of `IT` resolves via global namespace rule in bukkit function mode.
Reason: explicit method-scope clause is specific and already testable.

5. `N13` (`O HAI IM` lookup regime)
Status: `adjudicated`
Decision: keep slot-first then global lookup behavior.
Evidence: runtime regression `object-block-slot-first-over-global-src` in `tests/spec/runtime-core-test.rkt`.

6. `N14` (Function/variable namespace)
Status: `adjudicated`
Decision: single shared namespace with duplicate declaration errors in same frame.
Reason: direct prose statement and existing runtime behavior align.

7. `N15` (Receiver-projected slot-call semantics)
Status: `adjudicated`
Decision: callable in slot-call position executes with receiver-projected lookup, regardless of original storage source.
Reason: explicit slot-access function prose and existing receiver tests.

8. `N20` (`omgwtf` boundaries)
Status: `adjudicated`
Decision: missing-slot path routes through `omgwtf` and memoizes synthesized value to the slot.
Evidence: runtime regression `omgwtf-memoizes-missing-slot-src` in `tests/spec/runtime-core-test.rkt`.

9. `N21` (Parent-cycle safety)
Status: `adjudicated`
Decision: all parent-chain traversals are treated as cycle-safe.
Evidence: runtime regressions `parent-cycle-assignment-terminates-src` and `parent-cycle-method-call-terminates-src` in `tests/spec/runtime-core-test.rkt`, in addition to existing lookup-cycle test.

10. `N22` (Copy-on-write inherited assignment)
Status: `adjudicated`
Decision: child assignment to inherited name creates/updates child slot, never mutates ancestor slot.
Reason: explicit copy-on-write prose and current behavior.

11. `N23` (Special slot inheritance/shadowing)
Status: `spec-underdetermined`
Decision: keep explicit project policy table for `parent`, `omgwtf`, `izmakin` inheritance/copy behavior.
Action: write policy table + tests; mark as policy-governed until spec text narrows.

12. `N24` (Mixin source-set ambiguity)
Status: `spec-underdetermined`
Decision: keep own-slot copy as baseline pending policy table and cross-implementation evidence note.
Action: add tests for own-only vs inherited-on-mixin source and document chosen strict policy.

13. `N27` (`GTFO` nearest target)
Status: `adjudicated`
Decision: nearest enclosing valid control target wins (`loop`/`switch` break; function return-noob only in function context).
Reason: only coherent interpretation across nested contexts.

14. `N34` (Variadic closure on logical statements)
Status: `adjudicated`
Decision: implicit closure computed over logical statements after format preprocessing, not raw physical lines.
Reason: required to satisfy comma + continuation semantics together.

## Immediate Next Steps

1. Completed: targeted tests for `N13`, `N20`, `N21` were added and pass in `tests/spec/runtime-core-test.rkt`.
2. Write explicit policy tables/tests for `N23`, `N24`.
3. Re-run spec and corpus scripts after tranche-1 changes.

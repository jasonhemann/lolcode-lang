# Spec Adjudication Policy (Strict LOLCODE 1.3)

Date: 2026-03-06
Scope: `HAI 1.3` only, interpreted as 1.3 plus 1.2 baseline clauses not overridden by 1.3.

## Goals

1. Implement exactly what the spec defines.
2. Avoid silent extensions and ad hoc convenience behavior.
3. Keep parser/runtime behavior predictable and compositional.
4. Make every policy decision traceable to spec text and tests.

## Decision Ladder

Apply these in order for each disputed behavior.

1. Explicit normative grammar or direct normative prose wins.
2. If two clauses conflict, prefer the more specific clause over a broad umbrella clause.
3. If still conflicting, prefer the clause in the section dedicated to that feature over incidental mentions elsewhere.
4. Example code is informative but not authoritative over normative grammar/prose.
5. Choose the interpretation that requires the least unstated machinery and preserves coherence across adjacent clauses.
6. If one interpretation creates unavoidable parse ambiguity, reject it and keep the unambiguous interpretation.
7. If ambiguity remains irreducible, keep strict acceptance boundaries and surface explicit errors over hidden coercion or inference.
8. If the spec is truly silent and no coherent implied behavior can be derived, mark the item as `spec-underdetermined` and defer to an explicit project policy note.

## Reserved Keywords Policy

- Direct identifier positions use strict reserved-keyword rejection.
- Dynamic names must use `SRS` where the grammar permits dynamic identifiers.
- Rationale: allows deterministic parsing and prevents delimiter-vs-identifier ambiguity (`MKAY`, `AN`, etc.).

## Extension Policy

- No non-spec compatibility mode.
- No permissive grammar aliases unless the spec itself states equivalence.
- Corpus programs that rely on extensions are classified as out-of-scope, not used to widen grammar.

## Error Policy

- Prefer parse-time errors for syntactic invalidity.
- Prefer runtime errors for context misuse that cannot be determined statically (for example, invalid control context reached only dynamically).
- Do not auto-correct or provide ad hoc typo-specific behavior in semantics.

## Adjudication Workflow

For each concern:

1. Record exact clause anchors (file + line range).
2. Classify as `implemented`, `spec-conflict`, `spec-underdetermined`, or `missing`.
3. Decide behavior using the decision ladder.
4. Add or update tests:
   - one positive conformance test
   - one negative test, unless the clause is non-erroring by nature
5. Update traceability mapping and corpus classification notes.
6. Record final status and follow-up tasks.

## Implementation Safety Gate

Every tranche change must pass this gate before check-in:

1. Anchor each change to exact spec clauses first (no speculative edits).
2. Add or tighten targeted regression tests before broad refactors.
3. Keep edits minimal and local to the adjudicated concern.
4. Run focused suites for touched behavior, then full `./scripts/test_racket.sh`.
5. If parser acceptance/lexing changed, compare corpus classification deltas.
6. Update traceability docs with:
   - clause anchors
   - policy rationale
   - test references
7. Reject any acceptance broadening unless explicitly warranted by spec text.

## Evidence Requirements

A concern can be closed only when all are true:

1. Decision is documented with clause anchors.
2. Behavior is represented in parser/runtime code.
3. Tests pass and prevent regression.
4. Traceability docs are updated.

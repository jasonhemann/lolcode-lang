# Implementation House Style (Strict LOLCODE 1.3)

Purpose:
- Keep runtime/parser changes coherent with spec exegesis work.
- Prevent reintroduction of known artifacts (method tables, synthetic fallback, ad hoc compatibility behavior).

## Semantic Design Rules

1. One semantic path per surface construct.
   - `I IZ ...` is ordinary function call.
   - `<object> IZ ...` is slot-call dispatch.
   - `<object>'Z ...` is slot access.
   - Do not blur forms with hidden reinterpretation.

2. Methods are slot callables.
   - No separate method namespace/table semantics.
   - Rebinding a callable slot must affect `IZ` dispatch for that name.

3. Slot-call invocation must be receiver-projected and env-first.
   - Use a single helper path for receiver projection, `ME` binding, and sync-back.
   - Reuse it for normal slot-call and special hooks (`omgwtf`, `izmakin`).

4. No synthetic extension fallbacks.
   - Reject out-of-grammar forms with explicit errors.
   - Do not recover by fabricating identifier forms.

5. Missing-slot hook discipline.
   - Missing-slot resolution is explicit and memoized.
   - Re-entrancy on the same missing slot must be guarded and deterministic.

## Data Model Rules

1. Env bindings are always boxes (`Var -> Boxof Val`).
2. Env tables should only contain boxes; invariant violations are hard runtime errors.
3. Use sets for membership-only maps (avoid hash `name -> #t` patterns).

## Parser/Runtime Hygiene

1. Prefer strict grammar over permissive heuristics.
2. Prefer explicit helper functions for repeated structural behavior (slot-call, missing-slot resolution, callable creation).
3. Keep parser comments aligned with strict semantics; remove stale extension notes.

## Test Discipline

1. Every semantic correction needs at least one regression that fails under prior behavior.
2. Tests must distinguish:
   - spec-compelled behavior,
   - policy-pinned behavior in underspecified areas.
3. Run focused suites first, then full `./scripts/test_racket.sh` before check-in.

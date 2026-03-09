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
4. Prefer direct recursive helpers over local named-`let`/internal loop definitions when behavior is equivalent.
   - Use local loop bindings only when they materially improve clarity (e.g., mutually recursive local helpers, tightly scoped accumulators).
5. Avoid alias-only wrapper functions that just forward to another function unchanged.
   - If there is no behavior, contract, or boundary value, inline call sites to the canonical function name.
   - Exception: explicit public-API compatibility shims may remain when intentionally documented.
6. Target small functions: generally keep method/function bodies under ~50 lines.
   - Not a hard cap; exceptions are allowed when complexity is intrinsic and clearly documented.
   - Multiple nested local helper functions are a refactor signal: split behavior into top-level or separately testable units.
7. Reserve `!` suffix for mutation.
   - Use `!` only when function behavior mutates state (boxes, object slots, hash tables, ports, etc.).
   - Do not use `!` merely because a function may raise an error.
8. Prefer immutable local state.
   - Default to pure/immutable local transformations instead of `set!` in function bodies.
   - Allow localized mutation only when it materially improves clarity or performance (e.g., stream scanners/tokenizers), and keep it tightly scoped with a short comment.

## Test Discipline

1. Every semantic correction needs at least one regression that fails under prior behavior.
2. Tests must distinguish:
   - spec-compelled behavior,
   - policy-pinned behavior in underspecified areas.
3. Run focused suites first, then full `./scripts/test_racket.sh` before check-in.

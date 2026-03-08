# Expert Review Action TODO (2026-03-07)

Scope:
- Strict `HAI 1.3` target only.
- Incorporates the updated deep-audit delta and checklist pass.
- Converts adjudication into an implementation/action queue with evidence.

## 1) What Was Corrected In This Pass

1. Removed method/slot split from runtime semantics.
2. Removed synthetic receiver fallback (`I IZ ghost'Z hi MKAY` extension behavior).
3. Fixed `omgwtf` calling-convention crash (`env-table` contract violation).
4. Added regressions:
   - `method-defs-are-slot-callables`
   - `omgwtf-slot-function-call-convention`
5. Revalidated full suite (`./scripts/test_racket.sh`).

## 2) Statutory-Style Interpretation Notes (Why These Fixes Are Required)

### A. Methods are slot values, not a separate namespace

Textual basis:
- Object/function prose describes functions stored in bukkit slots and called via slot-call syntax.
- The language surface distinguishes call forms (`I IZ ...` vs `<object> IZ ...`), not callable value categories.

Reasoning:
- A separate method table allows outcomes the text does not license:
  - callable by `IZ` while missing from `'Z`;
  - slot rebinding not affecting dispatch for same name.
- That interpretation adds machinery beyond the text and breaks single-name coherence.
- Therefore, the coherent strict reading is: method declarations produce callable slot values.

### B. Synthetic fallback for unbound receiver identifiers is non-textual

Textual basis:
- Grammar defines ordinary calls and slot calls explicitly.
- No clause defines reinterpretation of an unbound receiver identifier into a fabricated namespaced function symbol.

Reasoning:
- The fallback accepts programs outside defined forms and introduces asymmetries (notably with `SRS`) that are not spec-grounded.
- Under strict exegesis, ambiguous/non-licensed forms must be rejected rather than silently reinterpreted.

### C. `omgwtf` callable convention must match normal function values

Textual basis:
- Functions are invoked with normal function semantics; slot-called functions are still function values.
- `omgwtf` is a slot hook, not a distinct callable type in the spec.

Reasoning:
- Passing an object where env is expected is an implementation defect, not a semantic choice.
- Hook invocation must use the same receiver-projected env-first callable path as other slot calls.

## 3) Prioritized Outstanding Queue

Priority A (semantic contradictions):
1. DONE (2026-03-08): `IT` contradiction cluster (`C1/C2/C3`) closed with conservative exegesis policy.
   - Ordinary execution contexts keep activation-local `IT` semantics.
   - In method context, bare `IT` bypasses receiver slot namespace and resolves to method activation-local `IT` (never receiver/global aliased).
2. DONE (2026-03-08): default return semantics in method context now follow ordinary function rule (fallthrough returns method activation-local `IT`).
3. DONE (2026-03-08): provisional pins promoted: `N12`/`N60`/`N74` are now policy+implemented.

Priority B (special slots / object lifecycle):
3. DONE (2026-03-08): `omgwtf` trigger boundary for `<object> IZ <slot> ... MKAY` miss path aligned to slot-access semantics (full chain then one-shot hook on original receiver, with memoization).
   - Closed pieces: `E4`/`E5` one-shot miss-path semantics.
   - Related still-open boundary: synthesized non-function slot-call behavior (`G4`) remains tracked separately.

Priority C (underspecified feature intersections):
4. OPEN: evaluation-order policy hardening for side-effecting expressions (`SMOOSH`/logic intersections).
   - Provisional pins: `N40`/`N75` cover currently implemented eager/left-to-right call/operand sequencing, but remain provisional pending fuller textual exegesis for variadic/side-effect intersections (`G1`-`G3`).
5. CLOSED (resolved by `N63`): expression-level TYPE-word binding policy is adjudicated and implemented as dual-role contextual semantics (TYPE literals in expression position; declaration/prototype forms disambiguated by grammar).

Priority D (process/traceability hygiene):
6. In progress: reconcile status drift between `ITEM_BY_ITEM_RESOLUTION_MAP.md`, expert checklist, and pass-level adjudication docs.
7. CLOSED (process pass complete): no generic “remaining pass1 prompts” bucket remains.
   - Residual concrete queue is now explicit:
     - evaluation-order textual grounding for `SMOOSH`/logic intersections (`G1`-`G3`).

## 4) De-duplicated Document Ownership

Use this ownership map to avoid policy fragmentation:

1. Canonical adjudication rules:
   - `spec/traceability/SPEC_ADJUDICATION_POLICY.md`
2. Expert item dispositions and status:
   - `spec/traceability/ITEM_BY_ITEM_RESOLUTION_MAP.md`
3. Delta discoveries and tranche updates:
   - `spec/traceability/spec-1.3-clause-mapping-audit.md`
4. Implementation/refactor house style:
   - `spec/traceability/IMPLEMENTATION_HOUSE_STYLE.md`
5. Clause-level matrix truth source:
   - `spec/traceability/spec-1.3-matrix.rktd`

Rule:
- When decisions conflict, update policy first, then pass-level adjudication, then matrix/test evidence.

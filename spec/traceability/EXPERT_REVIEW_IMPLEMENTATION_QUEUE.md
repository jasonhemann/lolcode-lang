# Expert Review Implementation Queue (2026-03-07)

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
   - Regression pins include:
     - `method-fallthrough-it-vs-slot-it`
     - `method-explicit-me-slot-it`
     - `object-body-it-slot-construction`

Priority B (special slots / object lifecycle):
4. DONE (2026-03-08): `omgwtf` trigger boundary for `<object> IZ <slot> ... MKAY` miss path aligned to slot-access semantics (full chain then one-shot hook on original receiver, with memoization).
   - Closed pieces: `E4`/`E5` one-shot miss-path semantics.
5. DONE (2026-03-09): synthesized non-function slot-call boundary (`G4`) closed.
   - Policy pin: `omgwtf` applies to missing-slot lookup failure; after synthesis, slot-call remains callable-only and errors on non-function values.
   - Regression pin: `method-call-noncallable-after-omgwtf-synthesis`.

Priority C (underspecified feature intersections):
6. DONE (2026-03-08; updated 2026-03-09): evaluation-order policy hardening for side-effecting expressions (`SMOOSH`/logic intersections) is now pinned.
   - Adjudicated policy: expression operands evaluate left-to-right; `SMOOSH` remains eager, while variadic logical forms (`ALL OF`/`ANY OF`) short-circuit.
   - Side effects from earlier operands remain visible even when a later operand errors.
   - `N40`/`N75` promoted from provisional to policy+implemented.
7. CLOSED (resolved by `N63`): expression-level TYPE-word binding policy is adjudicated and implemented as dual-role contextual semantics (TYPE literals in expression position; declaration/prototype forms disambiguated by grammar).

Priority D (process/traceability hygiene):
8. DONE (2026-03-09): reconciled status drift between `ITEM_BY_ITEM_RESOLUTION_MAP.md`, expert checklist, and pass-level adjudication docs for the `IT`/`omgwtf` clusters.
9. CLOSED (process pass complete): no generic “remaining pass1 prompts” bucket remains.
   - Residual concrete queue is now explicit:
     - (none in this queue section after `G1`-`G3` closure).

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

## 5) Next Tranche (Post-Closure Work)

With the expert-checklist adjudication queue closed, the next useful work is evidence expansion and drift prevention:

1. DONE (2026-03-09): Corpus expansion wave refresh and reclassification pass.
   - Queue rebuild reused cached upstream snapshots (network fetches timed out in this run), then refreshed newest waves (`49`, `50`) and reconciled manifest/queue.
   - Evidence stats rerun via:
     - `./scripts/test_external_evidence.sh`
     - `./scripts/eval_tier2_corpus.sh`
     - `./scripts/analyze_external_evidence.sh`
     - `./scripts/update_corpus_status.sh`
2. DONE (2026-03-09): Traceability hard-linking for `Nxx` test names.
   - Added generated ledger:
     - `spec/traceability/NXX_TEST_ANCHORS.md`
   - Added generator:
     - `scripts/generate_nxx_test_anchors.rkt`
3. DONE (2026-03-09): Regression hygiene (release-blocking gate) pinned.
   - Required boundary regressions:
     - `method-fallthrough-it-vs-slot-it`
     - `method-explicit-me-slot-it`
     - `object-body-it-slot-construction`
     - `method-call-noncallable-after-omgwtf-synthesis`
   - These remain in `tests/spec/runtime-core-test.rkt` (always executed by `./scripts/test_racket.sh`), and traceability audit now checks their presence.

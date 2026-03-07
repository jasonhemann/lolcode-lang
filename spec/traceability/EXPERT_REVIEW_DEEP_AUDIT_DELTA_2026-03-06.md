



# Expert Review Deep Audit Delta (2026-03-06)

Scope:
- Compare `lolcode_1_3_expert_review_adjudication_pass1.md` against current implementation and existing traceability notes.
- Focus on high-complexity object/slot/inheritance/`omgwtf`/`izmakin`/`IT` intersections.

Inputs:
- `spec/traceability/lolcode_1_3_expert_review_adjudication_pass1.md`
- `spec/traceability/ITEM_BY_ITEM_RESOLUTION_MAP.md`
- `spec/traceability/ORDERED_NOTES_ADJUDICATION_CHECKLIST.md`
- `src/lolcode/runtime.rkt`
- `src/lolcode/runtime/value.rkt`
- `src/lolcode/parser.rkt`
- `tests/spec/runtime-core-test.rkt`

## Executive Summary

First, things we should treat as settled from the text.

A BUKKIT has special slots parent, omgwtf, and izmakin. parent is the prototype link; omgwtf is the missing-slot hook; izmakin is the post-prototyping hook.

There are three distinct surface forms and they are not interchangeable: ordinary call is I IZ <function> ... MKAY; slot access is <object>'Z <slot>; slot-call is <object> IZ <slot> ... MKAY. Dynamic slot names use SRS, and the spec’s own example computes a method name with SMOOSH and then calls it with IZ SRS ... MKAY.

Bare function names in expression position denote the function value; they do not perform a nullary call. The text explicitly stores a function in a slot with <object> HAS A blogin ITZ blogin, which only makes sense if bare blogin means the function object, not blogin().

Functions are fixed-arity. Arguments are evaluated before the call. There is no text support for user-defined variadic functions; only variadic operators like SMOOSH and VISIBLE are variadic.

In object-called functions, lookup changes. The stated order is: function namespace, then calling object namespace, then “global” namespace; ME names the calling object and throws if there is no calling object; ME HAS A and ME'Z ... are the explicit ways to create/use receiver slots from inside the function.

In an O HAI IM <object> ... KTHX block, I refers to the object, and bare identifiers are looked up via slot-access first, then global scope, then error. So object-body code is not using ordinary local-variable lookup first.

Prototype inheritance via LIEK A creates a parent slot on the new object, and changing that slot later changes the object’s prototype. Parent-chain lookup continues until parent is NOOB or an already-searched parent is reached, so cycle detection is mandatory in parent-chain traversals.

Child assignment to an inherited name is copy-on-write shadowing, not direct parent mutation. If the name is found only up the inheritance chain, the spec says it is declared/created in the current object and set there. If it is found nowhere and was never previously assigned, that is a declaration error.

Inherited callable slots are receiver-dynamic. The text is explicit: “during a Slot-Access Function call, the Function obtains variables from the object it was accessed from,” and the prefix example shows the same inherited function producing parent output when called through the parent and child output when called through the child.

LIEK A and inheritance-SMOOSH are different mechanisms. LIEK A is prototype inheritance through parent. SMOOSH in the inheritance syntax is static mixin copying. Mixins are applied in reverse declaration order, and later donor changes do not propagate into the recipient. That means leftmost declared mixins win on conflicts among mixins.

Slot declarations inside bukkits may be repeated; repeating them just changes the referenced value. Ordinary variables/functions are different: the function example says I HAS A var ITZ 0 is an error if var is already taken by a function, and ordinary functions/variables share a namespace.

Variables are references to locations in memory. Primitive values are immutable, but variables themselves are references. That is enough to justify a shallow-reference model unless a feature explicitly says otherwise.

VISIBLE prints by casting arguments to YARN. The spec defines that unsafe casts cause errors for type-specific operators, and it does not define FUNKSHUN-to-YARN casting. So printing a function should be treated as an error, not given an invented printable representation.

The concrete slot syntax to implement is 'Z. The prose line that says the slot operator is - is editorial noise; every actual syntax example in the draft uses 'Z.

Second, these are implementation policies we chose to complete underspecification, not things the text says verbatim.

omgwtf should fire only after the entire parent-chain slot lookup fails, and it should fire once, on the original receiver. The text says omgwtf is called when slot access fails, and slot access itself includes climbing the parent chain with cycle stopping. So an early local miss is not yet “slot access fails”; it is only an intermediate lookup miss. This is the only completion that does not fight the inheritance lookup the text already defines.

The runtime default for omgwtf should be “throw,” because that is the only default behavior the text actually states. A user override may return a value that the runtime then installs into the missing slot, or it may throw. Because the text gives no missing-slot-name argument or implicit binding, user-defined omgwtf is inherently name-insensitive unless you add an extension.

Shallow copy is the right reading for slot copying / mixin copying. The text says variables are references and mixins copy slots; it never introduces recursive deep cloning. So if a copied slot points to another BUKKIT, aliasing that nested BUKKIT is the natural behavior. This is a strong textual inference, not an added feature.

ME'Z parent IZ bump MKAY is the natural “super-like” call form the language gives you, because there is no dedicated super keyword but parent is a real special slot and slot-call syntax accepts object expressions. This is a consequence of the general slot/special-slot syntax, not a separately stated feature.


Take that as advice as we walk through these purported issues:

## High-Severity Findings

### 1) Method/slot dual-namespace model is real and load-bearing

Evidence in code:
- Separate `slots` and `methods` maps in `lol-object%` (`src/lolcode/runtime/value.rkt`, lines 26-28).
- Method lookup is independent (`lookup-method`) from slot lookup (`lookup-slot-box`) (`src/lolcode/runtime/value.rkt`, lines 55-73).
- Object-method definitions install into method table (`src/lolcode/runtime.rkt`, lines 755-758 and 824).
- Method call dispatch tries method table first, then callable slot (`src/lolcode/runtime.rkt`, lines 425-437).

Observed consequences:
- A method name can be callable via `IZ` while `obj'Z name` is missing.
- Slot assignment cannot rebind method dispatch behavior in the same name as expected for single-slot semantics.

Repro outcomes:
- `HOW IZ I f ...` then `o'Z f R 7` -> `unknown slot: f`.
- `o HAS A f ITZ "S"` after method def -> `o IZ f MKAY` returns method result, `o'Z f` reads slot value.

Assessment:
- This is the core semantic fork behind checklist `B7/H1`.

### 2) `omgwtf` slot hook invocation has calling-convention bug

Evidence in code:
- `call-omgwtf!` invokes slot hook as `(maybe-hook this (list name) ctx)` (`src/lolcode/runtime/value.rkt`, line 95).
- Global/function values are compiled as env-first callables (`src/lolcode/runtime.rkt`, lines 686-713).

Observed consequence:
- Slot-assigning `omgwtf` to a normal function can crash with internal contract error (`env-table: expected env? given object`).

Assessment:
- Implementation defect (not policy choice), and can be misread as semantic behavior if not isolated.

### 3) Method-call miss does not trigger `omgwtf` unless slot was prewarmed through `'Z`

Evidence in tests and code:
- Explicit policy test: `method-call-does-not-trigger-omgwtf` (`tests/spec/runtime-core-test.rkt`, lines 889-897).
- Prewarming test: slot access via `'Z` materializes callable then `IZ` succeeds (`tests/spec/runtime-core-test.rkt`, lines 899-905).
- Dispatch path bypasses missing-slot `get-slot` and uses method lookup/fallback flow (`src/lolcode/runtime.rkt`, lines 425-441).

Assessment:
- Coherent as a chosen policy, but likely under-examined against "slot access fails" wording in spec.
- Pass1 correctly leaves related items OPEN.

### 4) Special-slot inheritance is inconsistent between method-defined and slot-assigned hooks

Evidence in code:
- Every object eagerly gets default `omgwtf`/`izmakin` slots (`src/lolcode/runtime/value.rkt`, lines 37-43).
- Inherited method hooks can still resolve through method chain.
- Slot-assigned parent hook can be masked by child default slot presence.

Observed consequence:
- Parent slot-assigned `izmakin` (`izmakin R boot`) does not run for child prototype.
- Parent method-defined `izmakin` (`HOW IZ I izmakin`) does run for child prototype.

Assessment:
- Semantic asymmetry not yet resolved in policy/docs (`E7/H10`).

### 5) Synthetic receiver-name fallback remains an explicit extension

Evidence in code:
- Identifier receiver path synthesizes `"<receiver>'Z <method>"` fallback when receiver binding is missing (`src/lolcode/runtime.rkt`, lines 451-456).
- Parser comment admits namespace-style fallback (`src/lolcode/parser.rkt`, lines 232-234).

Assessment:
- Direct conflict with strict-no-extension intent and pass1 `B8/H2` disposition.

## Medium-Severity / Important OPEN Questions

### 6) `IT` contradiction still leaks surprising default method return behavior

Evidence in code:
- Method call env aliases `IT` to runtime-global box (`src/lolcode/runtime.rkt`, lines 132-138 and method call sites 732/805).

Observed consequence:
- Method with no bare expression can return whatever global `IT` already holds (example run produced `<BUKKIT>`).

Assessment:
- This is exactly the `C2/C3` contradiction pressure point; currently policy-pinned but semantically unstable for users.

### 7) Pass1 `MATCH` wording is too strong for some `U/C` regions

Examples:
- `F3` (mixin own-only vs own+inherited) is textually contradictory in 1.3 examples; implementation picks own-only policy.
- `G1/G3` evaluation order and side effects are policy pins, not textually compelled semantics.

Assessment:
- Valid project policies, but should remain visibly policy-level rather than "spec settled."

## Cross-Doc Consistency Gaps

1. `spec/traceability/ITEM_BY_ITEM_RESOLUTION_MAP.md` uses many `implemented` statuses that now overlap with pass1 `DIVERGENCE/OPEN` hotspots (notably method/slot and special-slot areas). Add an expert-pass override marker for impacted IDs.
2. `spec/traceability/ORDERED_NOTES_ADJUDICATION_CHECKLIST.md` marks `N84` ("method-call does not trigger omgwtf") as implemented, while pass1 treats broader dispatch semantics as OPEN/possibly divergent under strict exegesis.
3. `spec/traceability/lolcode_1_3_expert_review_adjudication_pass1.md` has trailing section `L` prompt text ("What about all the printing?") that is not adjudicated yet. Move it into explicit OPEN items or remove it.

## Recommended Next Tranche (Audit-Driven)

1. Semantics-first dispatch normalization:
   - Remove synthetic fallback (`src/lolcode/runtime.rkt`, identifier receiver fallback branch).
   - Collapse method/slot dispatch toward single callable-slot model, or explicitly mark and reject split as non-spec extension.

2. Hook model cleanup:
   - Fix `omgwtf` slot-hook calling convention defect.
   - Add explicit tests for inherited slot-assigned `omgwtf/izmakin` behavior to force policy choice.

3. Policy-to-test closure for OPENs:
   - Add dedicated tests for pass1 gaps: `J6`, `J7`, `J14`, `J15`, `J17`, `J18`.

4. Docs alignment pass:
   - Update resolution-map statuses for expert-pass divergences.
   - Convert pass1 section `L` into explicit `G/C` tracked items with test links.

## Validation Run

- `raco test tests/spec/runtime-core-test.rkt tests/spec/spec-audit/known-gaps-failing-test.rkt`
- Result: `486 tests passed`.

Passing tests here means current behavior is stable under current tests, not that unresolved semantics are fully adjudicated.


### Outstanding, so don't go "fix"


IT is still the big one. We have not yet settled IT, local scope after a bare expression, and IT always looked up from global namespace in bukkit-called functions, vs no global scope. This should be resolvable by figuring out the plain reading of a couple of sections, but we just haven't settled and explained it yet.

We have not settled whether inherited izmakin counts, whether each fresh object gets a default own izmakin slot that masks an inherited one, or exactly how mixin-copied izmakin should interact with construction timing. The text says when izmakin runs, but not enough about precedence/timing in those combinations.

We have not settled whether mixin copying includes only slots defined directly on the mixin object or also inherited slots. The text says “all slots defined on the mixin”, suggesting own slots, but a later worked example about copying cheeze mentions “its parent slots” too.

We have not settled the exact coherent rescue reading of global / global scope / global namespace in the object sections. That is tied to the IT problem and should stay marked unresolved for now.

## Remediation Update (2026-03-07)

Completed in this tranche:

1. Method/slot split removed from execution semantics.
   - `lol-object%` now has a single slot table (no separate method map).
   - `HOW IZ I` inside object context and `HOW IZ <object> <slot>` both install callable values into slots.
   - `<object> IZ <slot> ... MKAY` dispatches only through slot values.
   - Evidence:
     - `src/lolcode/runtime/value.rkt` (single slot model)
     - `src/lolcode/runtime.rkt` (`expr-method-call`, `make-callable-fn`, method definition compilers)
     - Regression test: `method-defs-are-slot-callables` in `tests/spec/runtime-core-test.rkt`.

2. `omgwtf` env-table contract crash fixed.
   - Missing-slot resolution now invokes `omgwtf` through the same receiver-projected slot-call path as other slot calls.
   - This enforces env-first callable convention and removes the internal object-vs-env mismatch.
   - Evidence:
     - `src/lolcode/runtime.rkt` (`invoke-slot-callable`, `read-slot-value`)
     - `src/lolcode/runtime/value.rkt` (`resolve-missing-slot!`)
     - Regression test: `omgwtf-slot-function-call-convention` in `tests/spec/runtime-core-test.rkt`.

3. Synthetic identifier receiver fallback removed.
   - No runtime synthesis of `"<receiver>'Z <method>"` in plain method-call syntax.
   - Unbound receiver identifiers now raise `unknown identifier`.
   - Evidence: `src/lolcode/runtime.rkt` (`expr-method-call`).

4. Special hooks remain callable under the single-slot model.
   - `omgwtf` and `izmakin` now use explicit special-slot procedure lookup across parent chain.
   - Preserves inherited hook behavior for method-defined hooks while keeping default strict behavior when no hook is provided.
   - Evidence:
     - `src/lolcode/runtime/value.rkt` (`lookup-special-procedure-slot`)
     - `src/lolcode/runtime.rkt` (`run-izmakin-hook!`, `read-slot-value`).

Validation:

- `raco test tests/spec/runtime-core-test.rkt`
- `raco test tests/spec/spec-audit/known-gaps-failing-test.rkt tests/spec/spec-audit/traceability-test.rkt`
- `./scripts/test_racket.sh`
- Result: all passing (`976` suite total in full script run).

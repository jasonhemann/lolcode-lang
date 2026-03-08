
# LOLCODE 1.3 Textual-Recovery Review Checklist
## Objects, slot calls, SMOOSH mixins, inheritance, special slots, and extension-risk behaviors

Purpose: review only what can be recovered from the text of the 1.3 spec and avoid blessing implementation artifacts as semantics.

## Classification buckets

Use exactly one primary classification per item.

- **T — Textually compelled**: directly stated in normative prose or worked example.
- **I — Strong textual inference**: not said in one sentence, but follows naturally from multiple explicit rules.
- **U — Underspecified / arbitrary choice**: the text mentions the area but leaves a crucial step or tie-break undefined.
- **X — Likely implementation artifact / unwanted extension**: cannot be justified from the text; probably should not be treated as language semantics.
- **C — Textual contradiction / editorial defect**: spec says two incompatible things; conservative policy needed.

## Expert instructions

For each item:
1. identify the exact spec text or example that supports it;
2. decide T / I / U / X / C;
3. if U or C, decide whether the implementation should reject, error, or adopt a narrow conservative policy;
4. explicitly record whether we are *forbidding* any tempting extension.

---

## A. Parsing / AST distinctions that must be kept separate

### A1. Ordinary function definition vs slot-function definition
- **Text**: `HOW IZ I <function name>` versus `HOW IZ <object> <slot>`.
- **Why it matters**: these are not just the same syntax with a missing argument; they produce different lookup and receiver behavior.
- **Initial assessment**: **T** that both syntactic forms exist; **I** that they should be represented distinctly in the AST.
- **Decision needed**: confirm that the implementation does not collapse these too early.

### A2. Ordinary call vs slot-access function call
- **Text**: `I IZ <function name> ... MKAY` versus `<object> IZ <slotname> ... MKAY`.
- **Why it matters**: slot-call establishes receiver-sensitive lookup and enables `ME`.
- **Initial assessment**: **T**.
- **Decision needed**: confirm that these are separate parse/eval forms, not one call form with ad hoc runtime branching.

### A3. Ordinary `SMOOSH` concatenation vs mixin/inheritance `SMOOSH`
- **Text**: `SMOOSH ... MKAY` as string concatenation; `IM LIEK <parent> SMOOSH <mixin> ...` as mixin inheritance.
- **Why it matters**: same surface word, different grammatical category and semantics.
- **Initial assessment**: **T** that both uses exist; **I** that they need distinct AST nodes.
- **Decision needed**: confirm parser separation and prevent precedence bleed-through.

### A4. Slot access vs slot call vs ordinary identifier lookup
- **Text**: `<object> 'Z <slotname>`, `<object> IZ <slotname> ... MKAY`, and ordinary identifiers.
- **Why it matters**: lookup, type-checking, and fallback rules differ.
- **Initial assessment**: **T**.
- **Decision needed**: confirm these are separate evaluator paths.

### A5. `SRS` as dynamic slot name, not generic receiver reinterpretation
- **Text**: `<object> 'Z SRS <expression>` and `<object> IZ SRS funcName MKAY`.
- **Why it matters**: the spec gives `SRS` for dynamic slot naming/calling, not for converting arbitrary strings into receiver identifiers.
- **Initial assessment**: **T** for dynamic slot names; **X** for any extra “receiver-name fallback” semantics not grounded in the text.
- **Decision needed**: forbid non-textual reinterpretation of `SRS` results as namespace lookups.

### A6. `O HAI IM` contextual rewrite of `I`
- **Text**: “Anything `I` inside the codeblock actually refers to `<object>`.”
- **Why it matters**: this is a context-sensitive rewrite rule, not ordinary lexical scoping.
- **Initial assessment**: **T**, but operational details are partly **U**.
- **Decision needed**: specify whether this is parser desugaring or runtime contextual evaluation.

### A7. `O HAI IM` identifier lookup regime
- **Text**: identifiers within the block are looked up via slot-access first, then global scope, else error.
- **Why it matters**: this is a different lookup regime from ordinary local scope.
- **Initial assessment**: **T**.
- **Decision needed**: confirm whether this applies to all identifiers in the block, including references inside nested function definitions.

### A8. Slot operator typo: prose says `-`, examples use `'Z`
- **Text**: “slot operator `-`” immediately followed by syntax `<object> 'Z <slotname>`.
- **Why it matters**: lexer/parser must choose one actual token.
- **Initial assessment**: **T** for equivalence under explicit syntax prose.
- **Resolution (N06)**: accept both `-` and `'Z` as equivalent slot-access syntax, including dynamic `SRS` slot-name forms. This is treated as a textual equivalence, not a permissive extension.

---

## B. Receiver, lookup, and method-call mechanics

### B1. Receiver-dynamic slot-function calls
- **Text**: “No matter where a FUNKSHUN is stored in a slot, during a Slot-Access Function call, the Function obtains variables from the object it was accessed from,” plus the `parentClass` / `testClass` example.
- **Why it matters**: this is the central object-method semantics.
- **Initial assessment**: **T**.
- **Decision needed**: lock this in as canonical.

### B2. Function namespace -> calling object namespace -> “global” namespace
- **Text**: explicit three-step lookup order in the bukkit function scope section.
- **Why it matters**: determines shadowing and accidental capture behavior.
- **Initial assessment**: **T**.
- **Decision needed**: define what “global” means, given other parts of the spec deny global scope.

### B3. `ME` exists only when there is a calling object
- **Text**: explicit statement that `ME` throws if there is no calling object.
- **Why it matters**: the same function can succeed as a slot-call and fail as a plain call.
- **Initial assessment**: **T**.
- **Decision needed**: confirm this is a runtime error, not parse-time rejection.

### B4. `ME HAS A` and `ME'Z` target receiver slots
- **Text**: examples for declaration and assignment on the calling object.
- **Why it matters**: receiver slots and function-local variables are distinct namespaces.
- **Initial assessment**: **T**.
- **Decision needed**: confirm whether `ME HAS A` always creates/shadows locally on the receiver.

### B5. Parameter / local shadowing of receiver slots
- **Text**: function namespace is searched before calling object namespace; `ME'Z` is the explicit escape hatch.
- **Why it matters**: methods can accidentally read parameters instead of slots.
- **Initial assessment**: **I**.
- **Decision needed**: lock in test cases proving local/param shadowing and explicit `ME'Z` access.

### B6. Slot-call on a non-function slot
- **Text**: spec defines slot-call syntax but does not explicitly say what happens when the resolved slot is not a FUNKSHUN.
- **Why it matters**: this is a major type-error boundary.
- **Initial assessment**: **U**.
- **Decision needed**: conservative policy should probably be runtime type error, not fallback or coercion.

### B7. Distinct “method namespace” beating callable slot values
- **Observed in implementation**: “method wins over same-named slot callable on `obj IZ name MKAY`.”
- **Why it matters**: the spec treats methods as functions in slots, not as a separate namespace.
- **Initial assessment**: **X** unless a textual basis is found.
- **Decision needed**: likely forbid as an extension.

### B8. Synthetic namespaced fallback for `I IZ ghost'Z hi MKAY`
- **Observed in implementation**: fallback works only when receiver is a bare unbound identifier.
- **Why it matters**: this invents semantics for a surface form not clearly licensed by the grammar.
- **Initial assessment**: **X**.
- **Decision needed**: likely remove / reject.

### B9. No equivalent fallback for `SRS` receiver paths
- **Observed in implementation**: `SRS recv IZ hi MKAY` errors on non-BUKKIT string instead of using namespaced fallback.
- **Why it matters**: asymmetry suggests the fallback is not real language semantics.
- **Initial assessment**: fallback itself looks **X**; this asymmetry is evidence of that.
- **Decision needed**: remove the fallback rather than extend `SRS` to match it.

---

## C. Scope contradictions and `IT`

### C1. “No global scope” vs bukkit-scope lookup into “global”
- **Text**: early scope section says there is no global scope; bukkit function scope later says lookup ends in the “global” namespace.
- **Why it matters**: this affects name resolution everywhere in methods.
- **Initial assessment**: **C**.
- **Resolution (`C1/C2/C3`)**: “global” is interpreted as non-receiver ordinary lookup plane, not a process-global override of activation-local function temporaries.

### C2. `IT` is local after bare expressions vs `IT` is always looked up from global namespace
- **Text**: expression-statement section says `IT` remains in local scope; bukkit function scope says `IT` is always global.
- **Why it matters**: default function return and control-flow constructs depend on `IT`.
- **Initial assessment**: **C**.
- **Resolution (`N12`/`N60`/`N74`)**: method-context `IT` is activation-local and never resolved through receiver slot lookup; regressions pin local IT behavior and method fallthrough.

### C3. Default method return via `IT`
- **Text**: functions return `IT` if they reach `IF U SAY SO` without `FOUND YR`; bukkit scope section destabilizes where `IT` comes from.
- **Why it matters**: methods without explicit return are currently semantically unstable.
- **Initial assessment**: **C**.
- **Resolution (`C1/C2/C3`)**: method fallthrough returns the method activation-local `IT` cell (initialized to `NOOB`).

---

## D. Prototyping, parent chains, and mutation

### D1. `parent` slot auto-created by inheritance / prototyping
- **Text**: inheritance automatically creates a `parent` slot on the new object.
- **Why it matters**: required for all inheritance lookups.
- **Initial assessment**: **T**.
- **Decision needed**: confirm exact timing of creation.

### D2. Parent mutation is allowed
- **Text**: a bukkit may change its prototype by changing its `parent` slot.
- **Why it matters**: lookup is dynamic and can be changed after construction.
- **Initial assessment**: **T**.
- **Decision needed**: add explicit tests for parent mutation effects.

### D3. Cycle detection on parent-chain lookup
- **Text**: lookup stops when it reaches a parent object it has already searched before.
- **Why it matters**: prevents nontermination on cyclic parent graphs.
- **Initial assessment**: **T**.
- **Decision needed**: confirm that every parent-chain walk uses the same visited-set rule.

### D4. Cycle detection also on assignment’s existence search
- **Text**: assignment searches the current object, then parents, and if found only in an ancestor creates a new slot in the current object.
- **Why it matters**: this search is distinct from simple lookup, but must also be cycle-safe.
- **Initial assessment**: **I**.
- **Decision needed**: explicitly apply cycle handling here too.

### D5. Assignment to inherited name creates/shadows locally
- **Text**: if the variable name is found up the inheritance chain, then that variable is declared and created within the current object and set there.
- **Why it matters**: this is copy-on-write shadowing, not parent mutation.
- **Initial assessment**: **T**.
- **Decision needed**: lock in with tests.

### D6. Declaration error when assignment finds no such name
- **Text**: if the variable search fails and the variable was never previously assigned, then it is a declaration error.
- **Why it matters**: this is a sharp error boundary inside object assignment.
- **Initial assessment**: **T**.
- **Decision needed**: add explicit failure tests.

### D7. Shallow aliasing of nested BUKKITs across parent/child
- **Observed / inferred**: top-level inherited slot assignment shadows locally, but nested mutable BUKKIT values may still alias.
- **Why it matters**: child mutation of `cfg'Z count` may leak to parent if `cfg` itself was inherited by reference.
- **Initial assessment**: probably **I** or **U** depending on how literally “variables are references” is applied to slot-copy / prototype state.
- **Decision needed**: determine whether this can actually be recovered from text, or whether it is a policy choice.

---

## E. Special slots: `omgwtf` and `izmakin`

### E1. Every bukkit contains `parent`, `omgwtf`, and `izmakin`
- **Text**: explicit list of special slots every bukkit contains.
- **Why it matters**: affects inheritance and whether defaults exist on each object.
- **Initial assessment**: **T**.
- **Decision needed**: determine whether “contains” means each new object gets fresh default slots that may shadow inherited ones.

### E2. `omgwtf` runs when slot access fails; returns value to install or throws
- **Text**: explicit prose.
- **Why it matters**: defines missing-slot behavior and memoization.
- **Initial assessment**: **T** at high level; operational details below remain open.
- **Decision needed**: lock in the exact trigger and receiver.

### E3. What counts as “slot access fails”?
- **Open issue from notes**: missing slot vs present-but-non-function during slot-call vs other error modes.
- **Why it matters**: determines whether `omgwtf` is a missing-name hook or a more general dispatch failure hook.
- **Initial assessment**: **U**.
- **Decision needed**: conservative reading suggests missing-slot only, not non-function call.

### E4. Does parent-chain search happen before `omgwtf`, or does each failed hop trigger it?
- **Historical open issue from notes**.
- **Why it matters**: side effects, memoization, and cycle behavior all change.
- **Resolution (N84)**: full parent-chain slot lookup happens first; `omgwtf` runs once only after total lookup failure, on the original receiver.

### E5. Which object’s `omgwtf` is used after total failure?
- **Historical open issue from notes**: original receiver vs most distant ancestor.
- **Why it matters**: determines receiver, mutation target, and behavior under cycles.
- **Resolution (N84)**: original receiver only.

### E6. Interaction of `omgwtf` with global fallback
- **Open issue from notes**: if global lookup would succeed, does missing slot still count as failure?
- **Why it matters**: slot access and ordinary identifier lookup are being conflated in some readings.
- **Initial assessment**: **U**, but likely resolved by keeping slot lookup separate from global variable lookup.
- **Decision needed**: do not let ordinary global identifiers satisfy slot access unless text explicitly requires it.

### E7. Special slots masked by per-object defaults
- **Observed in implementation**: parent `izmakin`/`omgwtf` masked because child gets default special slots.
- **Why it matters**: inherited constructor/hook behavior may silently disappear.
- **Initial assessment**: **U** or **X**, not clearly textually compelled.
- **Decision needed**: do not bless this unless the expert finds direct textual support.

### E8. `izmakin` timing and inheritance
- **Text**: runs after a bukkit is fully prototyped but before the prototyping method returns.
- **Why it matters**: unclear whether inherited `izmakin` runs, and on what receiver.
- **Resolution (N19 + N23)**: high-level existence is **T** and inheritance/dispatch is policy-pinned: effective `izmakin` follows special-slot precedence (child own > copied mixin > inherited parent > default), and runs after prototype/mixin/parent restoration on the constructed receiver.

### E9. What state is visible to `izmakin`?
- **Text**: “fully prototyped” suggests parent/mixin state exists, but the ordering against body execution and mixins is not fully spelled out.
- **Why it matters**: constructor side effects and invariants depend on it.
- **Resolution (N19)**: visible state is post-prototype build with mixin copy and parent slot finalized; this ordering is test-pinned.

---

## F. Mixins and `SMOOSH` inheritance

### F1. Reverse order of mixin application
- **Text**: mixin slots are copied in reverse order of declaration; example says `ZipStuffz` then `FileStuffz`.
- **Why it matters**: leftmost written mixin wins in conflicts.
- **Initial assessment**: **T**.
- **Decision needed**: lock in as canonical.

### F2. Mixin inheritance is static, not live
- **Text**: object does not see later changes to mixin objects.
- **Why it matters**: copied slots are not dynamically linked.
- **Initial assessment**: **T**.
- **Decision needed**: lock in as canonical.

### F3. What exactly gets copied: own slots only, or inherited slots too?
- **Text**: prose says “all slots defined on the mixin”; later example comment says “all of cheeze and its parent slots are copied into slice.”
- **Why it matters**: these are not the same semantics.
- **Resolution (N24)**: policy-pinned to donor effective-visible source set (own + inherited-visible slots/methods), copied in reverse mixin order.

### F4. Shallow copy vs deep copy for copied slot values
- **Text**: not stated.
- **Why it matters**: nested mutable BUKKITs may alias across donor and recipient.
- **Resolution (N81)**: policy-pinned shallow/call-by-sharing copy for mutable slot values.

### F5. Receiver behavior of functions copied via mixins
- **Text**: slot-access function call rule says receiver is the object the function was accessed from, regardless of where the function is stored.
- **Why it matters**: copied functions should likely still be receiver-dynamic when slot-called on the recipient.
- **Resolution (N69)**: receiver-dynamic behavior is implemented and pinned for mixin-copied functions.

### F6. Mixing parent and child objects together
- **Historical open issue from notes**.
- **Why it matters**: with reverse copy order and possible inherited-slot copying, parent/child mixin combinations can duplicate or overwrite unexpectedly.
- **Resolution (N24 + N69 + N81)**: behavior is now policy-pinned with parent/child mixin interaction regressions.

### F7. Post-construction “manual mixin” example
- **Text**: example creates `slice` with `A bukkit SMOOSH cheeze`, then rewires `parent`.
- **Why it matters**: spec itself demonstrates manual prototype surgery after static mixin copying.
- **Initial assessment**: **T** that this pattern is intended to be legal.
- **Decision needed**: confirm exact consequences and test them.

---

## G. Evaluation order and side effects

### G1. Are `SMOOSH` arguments eagerly evaluated?
- **Text**: `SMOOSH` implicitly casts all input values to YARNs, but evaluation order and strictness are not explicitly formalized here.
- **Why it matters**: side effects, errors, and missing-slot hooks become observable.
- **Initial assessment**: probably **I** that arguments are evaluated, but exact order is **U**.
- **Resolution (policy-pinned)**: evaluate left-to-right and eagerly; side effects from earlier operands are preserved even if a later operand errors.

### G2. Two independent missing-slot accesses inside one `SMOOSH`
- **Observed**: `SMOOSH box'Z a AN box'Z b MKAY` fired `omgwtf` twice.
- **Why it matters**: this may be perfectly consistent if each operand is evaluated independently.
- **Initial assessment**: likely **I/U**, not necessarily a bug.
- **Resolution (policy-pinned)**: independent operands are evaluated independently in order; distinct misses trigger independent lookup/hook behavior.

### G3. Side effects before later operand error
- **Text**: not settled for variadics in general.
- **Why it matters**: whether printing/mutation from earlier operands survives if a later operand errors.
- **Initial assessment**: **U**.
- **Resolution (policy-pinned)**: side effects from already-evaluated operands are kept; later operand errors do not roll them back.

### G4. Slot-call after `omgwtf` synthesizes a non-function
- **Text**: `omgwtf` returns a value to place in the unknown slot, but slot-call type-check behavior is not specified.
- **Why it matters**: `<object> IZ missing MKAY` may synthesize a non-function.
- **Initial assessment**: **U**.
- **Decision needed**: likely runtime type error after synthesis.

---

## H. User-supplied implementation observations to classify

Use this section as a triage queue. The “initial read” is only a provisional judgment from the text.

### H1. `obj IZ name MKAY` prefers a method over a same-named callable slot
- **Initial read**: probably **X**.
- **Reason**: the spec presents methods as functions in slots, not a parallel namespace.

### H2. `I IZ ghost'Z hi MKAY` can resolve a synthetic function name when `ghost` is unbound
- **Initial read**: probably **X**.
- **Reason**: not recoverable from ordinary-call grammar or slot-call grammar.

### H3. The same fallback is blocked when `ghost` is bound to a non-BUKKIT
- **Initial read**: symptom of H2 rather than standalone semantics.

### H4. `SRS` receiver path does not get the same fallback
- **Initial read**: more evidence that H2 is an artifact.

### H5. Inherited slot function calls are receiver-dynamic
- **Initial read**: **T**.

### H6. Copy-on-write is shallow, so nested objects alias across parent/child
- **Initial read**: **I/U**.

### H7. `SMOOSH` is eager, so all operand side effects run
- **Initial read**: **I/U**.

### H8. Missing-slot `omgwtf` side effects fire once per operand access in `SMOOSH`
- **Initial read**: probably fine for distinct operands; needs same-name repeat test.

### H9. Mixin order is reverse-applied; leftmost declared mixin wins
- **Initial read**: **T**.

### H10. Child defaults mask inherited parent `omgwtf` / `izmakin`
- **Initial read**: **U/X**.
- **Reason**: “every bukkit contains” is not enough by itself to justify eager per-object shadowing.

---

## I. High-priority “do not accidentally extend the language” rules

These should be treated as default prohibitions unless the expert finds direct textual support.

1. Do **not** invent a separate method namespace that outranks callable slot values.
2. Do **not** invent synthetic namespaced fallback for `I IZ ghost'Z hi MKAY`.
3. Do **not** reinterpret `SRS` receiver results as namespace names or implicit variable lookups.
4. Do **not** silently treat slot-call on a non-function as ordinary slot access.
5. Do **not** call `omgwtf` once per ancestor unless the text clearly requires it.
6. Do **not** assume inherited `omgwtf` / `izmakin` are masked by per-object defaults unless the text compels it.
7. Do **not** introduce deep-copy mixin semantics without textual support.
8. Do **not** switch to parent-locked or definition-site-locked method closure semantics; the spec examples point toward receiver-dynamic lookup.
9. Do **not** resolve the `IT` contradiction by adding new invisible scopes or dynamic variables unless the expert explicitly approves that as the narrowest repair.

---

## J. Recommended concrete tests for the expert to request

1. Parent/child receiver-dynamic method call (`prefix` example from the spec).
2. Assignment to inherited slot creates child-local shadow, not parent mutation.
3. Assignment to missing slot in object hierarchy produces declaration error.
4. Parent-cycle lookup terminates.
5. Parent-cycle assignment existence search also terminates.
6. Missing slot with parent chain + `omgwtf`: original receiver vs ancestor hook.
7. Missing slot where resolved synthesized value is non-function, then called.
8. Inherited `izmakin`: runs or not?
9. Child with no explicit `omgwtf` / `izmakin`: inherited hook visible or masked?
10. Mixins `m1 AN m2`: leftmost wins.
11. Mixin donor later mutation does not affect recipient.
12. Mixin copies own slots only vs own+inherited slots.
13. Nested mutable slot copied by mixin: alias or copy?
14. `SMOOSH` with two missing slot operands: hook count and order.
15. `SMOOSH` with one side effecting operand and one erroring operand: ordering.
16. Slot-call on non-function slot: exact runtime error.
17. `ME` in plain function call: error.
18. `ME'Z` versus parameter shadowing in slot-called method.
19. `IT` inside ordinary function vs method default return.
20. `O HAI IM` name lookup inside block, including nested `HOW IZ I`.

---

## K. Minimal spec anchors the expert should keep open while reviewing

- Variables / scope / no global scope
- Expression statements and local `IT`
- Functions and default return
- Bukkit function scope and receiver lookup
- `ME`, `ME HAS A`, `ME'Z`
- `O HAI IM` and its lookup rule
- Slot access and `SRS`
- Special slots `parent`, `omgwtf`, `izmakin`
- Inheritance of slots
- Functions and inheritance
- Mixin inheritance and its worked examples

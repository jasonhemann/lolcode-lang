# LOLCODE 1.3 archival interpretation memo
Date: 2026-03-10

Purpose: preserve the project’s major hard-call interpretations in a form that is usable as:
1. an implementation guide,
2. a regression-test guide,
3. an archival justification memo for future implementers and reviewers.

This memo is written under the project’s adopted interpretive posture: the 1.3 spec is to be saved if at all possible, not rewritten casually. Broad umbrella prose yields to later, more specific object-language clauses where needed, and we avoid adding invisible machinery or permissive extensions unless the text forces them.

## Interpretive baseline

Use these principles first.

- The spec itself says 1.3 is trying to add features that make LOLCODE more like what programmers expect from modern languages (`lolcode-spec-v1.3.md` lines 1-5).
- The project policy says to avoid silent extensions and ad hoc convenience behavior; when a unique reading is not directly recoverable, pin the narrowest coherent policy rather than widening the language (`SPEC_ADJUDICATION_POLICY.md` lines 9, 24, 39, 54-64).

That means:
- do not invent extra namespaces or fallback forms;
- do not normalize away distinct syntax when the text can be saved as written;
- do not “repair” the language by adding hidden runtime mechanisms if a narrower reading keeps the clauses coherent.

---

## Holding 1: `I IZ ...` and `<object> IZ ...` are distinct semantic forms

### Text
- Ordinary function calls evaluate argument expressions before the call (`lolcode-spec-v1.3.md` lines 602-604).
- Bukkit call syntax is separately introduced as `<object> IZ <slotname> ... MKAY` (`lolcode-spec-v1.3.md` lines 741-756).
- The adjudication ledger records this as `N02`: distinct AST/runtime call paths for `I IZ` vs `<object> IZ` (`NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md` line 18).

### Holding
Treat ordinary call and slot-call as separate parse/eval forms.

### Why
The slot-call form is what makes receiver-sensitive lookup and `ME` meaningful. Collapsing them early forces ad hoc runtime branching and invites non-textual extensions.

### Minimal tests
- `ordinary-call-does-not-enable-me`
- `slot-call-enables-me`
- `parser-distinguishes-I-IZ-vs-object-IZ`

---

## Holding 2: methods are slot values, not a separate method namespace

### Text
- BUKKIT slots may hold functions; the spec explicitly stores a function value in a slot: `<object> HAS A blogin ITZ blogin` (`lolcode-spec-v1.3.md` lines 624-641).
- Slot-function definition syntax `HOW IZ <object> <slot>` is just another way to place a function in a slot (`lolcode-spec-v1.3.md` lines 642-660).
- The expert/TODO docs already rejected the old separate-method behavior as non-textual (`EXPERT_REVIEW_ACTION_TODO_2026-03-07.md` lines 7-18).

### Holding
A method is just a function value living in a slot. There is no parallel dispatch table outranking callable slot values.

### Why
A separate method namespace would allow results the text never licenses: callable by `IZ` while absent from `'Z`, or slot rebinding not affecting dispatch.

### Minimal tests
```lolcode
HAI 1.3
HOW IZ I f
  FOUND YR "ok"
IF U SAY SO
I HAS A o ITZ A BUKKIT
o HAS A f ITZ f
VISIBLE o IZ f MKAY
KTHXBYE
```

Expected: `ok`

---

## Holding 3: slot-call semantics are receiver-dynamic, not definition-site-locked

### Text
- The core sentence: “No matter where a FUNKSHUN is stored in a slot, during a Slot-Access Function call, the Function obtains variables from the object it was accessed from” (`lolcode-spec-v1.3.md` line 804).
- The parent/child `funkin` example immediately illustrates this (`lolcode-spec-v1.3.md` lines 804-825).
- The assessment file marks receiver-projected slot-function scope as implemented/tested (`NEXT-BOTTOM-UP-CONCERNS-ASSESSMENT-2026-03-05.md` line 51).

### Holding
If parent defines `f`, child inherits it, and child calls `f`, the body of `f` resolves receiver-sensitive names against the child.

### Why
This is the central object-method semantics the text actually gives. Java-like definition-site/parent-locked method closure would contradict the worked example.

### Minimal tests
```lolcode
HAI 1.3
HOW IZ I funkin YR shun
  FOUND YR SMOOSH prefix AN shun MKAY
IF U SAY SO

O HAI IM parentClass
  I HAS A prefix ITZ "parentClass-"
  I HAS A funkin ITZ funkin
KTHX

O HAI IM testClass IM LIEK parentClass
  I HAS A prefix ITZ "testClass-"
KTHX

VISIBLE parentClass IZ funkin YR "HAI" MKAY
VISIBLE testClass IZ funkin YR "HAI" MKAY
KTHXBYE
```

Expected:
```text
parentClass-HAI
testClass-HAI
```

---

## Holding 4: inside `O HAI IM`, `I HAS A` is object-slot creation/update, not outer-binding mutation

### Text
- “Anything `I` inside the codeblock actually refers to `<object>`” (`lolcode-spec-v1.3.md` line 714).
- “Identifiers within the O HAI block are looked up via slot-access first” (`lolcode-spec-v1.3.md` line 725).
- Bukkit slot declarations may be repeated; repeating them just changes the slot’s referenced value (`lolcode-spec-v1.3.md` lines 632-633).
- The assessment file pins object-body declarations as object-scoped and non-leaking (`NEXT-BOTTOM-UP-CONCERNS-ASSESSMENT-2026-03-05.md` line 64).

### Holding
Inside `O HAI IM`, `I HAS A name ...` always targets the current object frame:
- if the slot already exists on the current object, update it;
- otherwise create it on the current object;
- do not walk outward and mutate ordinary outer/global bindings.

### Why
`O HAI IM` is not ordinary lexical declaration scope; it is object-body syntax with slot-first lookup. Letting `I HAS A` leak outward would defeat the whole point of the block form.

### Minimal tests
```lolcode
HAI 1.3
I HAS A name ITZ "outer"
O HAI IM o
  I HAS A name ITZ "inner"
KTHX
VISIBLE name
VISIBLE o'Z name
KTHXBYE
```

Expected:
```text
outer
inner
```

And:
```lolcode
HAI 1.3
O HAI IM o
  I HAS A x ITZ 1
  I HAS A x ITZ 2
KTHX
VISIBLE o'Z x
KTHXBYE
```

Expected: `2`

---

## Holding 5: bare method `IT` is distinct from receiver slot `IT`

### Text
- In ordinary statements, bare expressions place their value in the temporary variable `IT`, and `IT` remains in local scope (`lolcode-spec-v1.3.md` line 407).
- `O RLY?` branches on `IT` (`lolcode-spec-v1.3.md` line 433).
- Function fallthrough return returns the value in `IT` (`lolcode-spec-v1.3.md` lines 588-592).
- In object-called functions, lookup order is function namespace, calling object namespace, then “global” namespace, and `IT` is singled out: “IT is always looked up from global namespace” (`lolcode-spec-v1.3.md` lines 664-672).
- `ME` / `ME'Z` are the explicit receiver-side escape hatch (`lolcode-spec-v1.3.md` lines 674-700).
- The adjudication ledger records this as `N12`: `IT` local in ordinary scopes; method-context `IT` follows the special object-function rule (`NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md` line 22).

### Holding
In method context:
- bare `IT` is the language temporary, not a receiver slot;
- `ME'Z IT` is the receiver slot named `IT`;
- those two must stay distinct.

### Why
This is the narrowest reading that keeps the ordinary `IT` machinery (`O RLY?`, fallthrough return, expression statements) intact while giving the bukkit-function scope paragraph real work: `IT` bypasses receiver-slot lookup.

### Minimal tests
Direct distinction:
```lolcode
HAI 1.3
O HAI IM o
  I HAS A IT ITZ "slot-it"
  HOW IZ I f
    7
  IF U SAY SO
KTHX

VISIBLE o IZ f MKAY
VISIBLE o'Z IT
KTHXBYE
```

Expected:
```text
7
slot-it
```

Explicit receiver access:
```lolcode
HAI 1.3
O HAI IM o
  I HAS A IT ITZ "slot-it"
  HOW IZ I f
    FOUND YR ME'Z IT
  IF U SAY SO
KTHX
VISIBLE o IZ f MKAY
KTHXBYE
```

Expected: `slot-it`

Control-flow distinction:
```lolcode
HAI 1.3
O HAI IM o
  I HAS A IT ITZ FAIL
  HOW IZ I f
    WIN
    O RLY?
      YA RLY
        FOUND YR "expr-it"
      NO WAI
        FOUND YR "slot-it"
    OIC
  IF U SAY SO
KTHX
VISIBLE o IZ f MKAY
KTHXBYE
```

Expected: `expr-it`

---

## Holding 6: plain `BUKKIT` starts with `parent = NOOB`

### Text
- Empty-object creation is `I HAS A <object> ITZ A BUKKIT`; it gets “the default behavior of all bukkits” (`lolcode-spec-v1.3.md` lines 616-622).
- Every bukkit contains special slots including `parent` (`lolcode-spec-v1.3.md` lines 760-766).
- Parent-chain lookup stops when the parent slot is `NOOB` (`lolcode-spec-v1.3.md` line 796).

### Holding
A plain `BUKKIT` has a `parent` slot whose default value is `NOOB`.

### Why
That is the only clean way to satisfy all three clauses at once.

### Minimal test
```lolcode
HAI 1.3
I HAS A o ITZ A BUKKIT
VISIBLE BOTH SAEM o'Z parent AN NOOB
KTHXBYE
```

Expected: `WIN`

---

## Holding 7: parent-chain lookup is cycle-safe, and child assignment to inherited names is copy-on-write shadowing

### Text
- Parent lookup continues until `parent` is `NOOB` or an already-searched parent is reached (`lolcode-spec-v1.3.md` line 796).
- Assignment inside an object searches current object, then parent chain; if found in an ancestor, the variable is created in the current object and set there; if not found anywhere, it is a declaration error (`lolcode-spec-v1.3.md` line 798).
- The adjudication ledger records cycle-safe traversal (`N21`) and inherited assignment copy-on-write (`N22`) (`NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md` lines 31-32).

### Holding
- Every parent-chain walk must be cycle-safe.
- Assigning to an inherited name creates/shadows that name locally on the child; it does not mutate the ancestor slot.

### Minimal tests
Copy-on-write:
```lolcode
HAI 1.3
O HAI IM p
  I HAS A n ITZ 0
KTHX
O HAI IM c IM LIEK p
KTHX
c'Z n R 1
VISIBLE p'Z n
VISIBLE c'Z n
KTHXBYE
```

Expected:
```text
0
1
```

Missing-name declaration error:
```lolcode
HAI 1.3
O HAI IM p
KTHX
O HAI IM c IM LIEK p
KTHX
c'Z missing R 1
KTHXBYE
```

Expected: runtime declaration error

---

## Holding 8: declaration/prototype grammar is saveable as written

### Text
- Variable default declaration form: `I HAS A <variable> ITZ A <type>` (`lolcode-spec-v1.3.md` line 126).
- Empty object: `I HAS A <object> ITZ A BUKKIT` (`lolcode-spec-v1.3.md` line 619).
- Plain prototype: `I HAS A <object> ITZ LIEK A <parent>` (`lolcode-spec-v1.3.md` line 777).
- Mixin prototype: `I HAS A <object> ITZ A <parent> SMOOSH <mixin> (AN <mixin>)*` (`lolcode-spec-v1.3.md` line 838).

### Holding
Do not rewrite the grammar. Preserve all four forms:
1. `ITZ A <built-in-type>`
2. `ITZ A BUKKIT`
3. `ITZ LIEK A <parent>`
4. `ITZ A <parent> SMOOSH ...`

### Why
The spec repeats and operationally explains the mixin form exactly as written. It is saveable without emendation.

### Minimal tests
Accepted:
- `I HAS A s ITZ A YARN`
- `I HAS A o ITZ A BUKKIT`
- `I HAS A c ITZ LIEK A p`
- `I HAS A z ITZ A River SMOOSH FileStuffz AN ZipStuffz`

Rejected:
- `I HAS A bad ITZ A River` (unless `River` is one of the recognized built-in type words)

---

## Holding 9: mixins copy the donor’s effective visible interface, including inherited-visible members; mixin application is reverse-order and static

### Text
- Formal mixin rule: “All slots defined on the mixin are copied” in reverse order (`lolcode-spec-v1.3.md` line 849).
- Worked example: copy `ZipStuffz`, then `FileStuffz`, then replace `parent` with `River` (`lolcode-spec-v1.3.md` line 855).
- Staticity: later donor changes do not affect the recipient (`lolcode-spec-v1.3.md` line 857).
- Later worked example: “all of cheeze and its parent slots are copied into slice” (`lolcode-spec-v1.3.md` line 871).
- The adjudication ledger pins the source set as donor effective-visible slots/methods, including inherited-visible members (`NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md` lines 120-127).

### Holding
- A mixin contributes its effective visible slot/method interface, not just syntactically local members.
- Donor-own members override donor-parent-visible members.
- Mixins are applied in reverse declaration order, so the leftmost written mixin wins.
- Mixins are static: later donor mutation does not propagate.

### Why
This is the only reading that saves both the formal prose and the `cheeze` comment without inventing a second hidden mechanism.

### Minimal tests
Inherited-visible donor member copied:
```lolcode
HAI 1.3
O HAI IM A
  I HAS A a ITZ "A"
KTHX
O HAI IM B IM LIEK A
  I HAS A b ITZ "B"
KTHX
I HAS A X ITZ A BUKKIT SMOOSH B
VISIBLE X'Z a
VISIBLE X'Z b
KTHXBYE
```

Expected:
```text
A
B
```

Reverse-order / leftmost-wins:
```lolcode
HAI 1.3
O HAI IM M1
  I HAS A tag ITZ "m1"
KTHX
O HAI IM M2
  I HAS A tag ITZ "m2"
KTHX
I HAS A X ITZ A BUKKIT SMOOSH M1 AN M2
VISIBLE X'Z tag
KTHXBYE
```

Expected: `m1`

Staticity:
- mutate donor after recipient creation;
- recipient must not change.

---

## Holding 10: special slots are copied through mixins too; only `parent` is then forcibly replaced by the declared parent

### Text
- Every bukkit contains `parent`, `omgwtf`, and `izmakin` (`lolcode-spec-v1.3.md` lines 760-770).
- Mixins copy “all slots” from the donor (`lolcode-spec-v1.3.md` line 849).
- The `ZipFileRiver` example explicitly calls out only one post-copy overwrite: replace `parent` with `River` (`lolcode-spec-v1.3.md` line 855).
- Project policy table `N23` records:
  - `parent`: copied from mixin effective visible slots, then replaced by declared parent;
  - `omgwtf`: copied via mixins and then participates in normal precedence;
  - `izmakin`: copied via mixins and then participates in normal precedence (`NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md` lines 112-118).

### Holding
- Mixins copy special slots too.
- After mixin copy, the new object’s `parent` is forcibly set to the declared parent object.
- No analogous reset is applied to `omgwtf` or `izmakin`.

### Why
The text explicitly singles out the `parent` rewrite and says nothing similar about the other special slots.

### Minimal tests
Copied `omgwtf` survives:
```lolcode
HAI 1.3
HOW IZ I fallback
  FOUND YR "from-mixin"
IF U SAY SO

O HAI IM M
  I HAS A omgwtf ITZ fallback
KTHX

I HAS A X ITZ A BUKKIT SMOOSH M
VISIBLE X'Z missing
KTHXBYE
```

Expected: `from-mixin`

Copied `izmakin` survives and runs:
```lolcode
HAI 1.3
HOW IZ I boot
  ME HAS A made ITZ WIN
IF U SAY SO

O HAI IM M
  I HAS A izmakin ITZ boot
KTHX

I HAS A X ITZ A BUKKIT SMOOSH M
VISIBLE X'Z made
KTHXBYE
```

Expected: `WIN`

---

## Holding 11: `omgwtf` is a zero-arity, name-insensitive, one-shot missing-slot hook; synthesis is memoized

### Text
- `omgwtf` is called when slot access fails, should return a value to place in the unknown slot or throw; default behavior throws (`lolcode-spec-v1.3.md` line 768).
- The spec supplies no missing-slot-name argument.
- The adjudication ledger pins:
  - zero-arity hook invocation because the spec does not define parameters (`NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md` lines 26, 112-118),
  - memoization of the synthesized value into the missing slot (`NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md` lines 26, 116-117).

### Holding
- `omgwtf` takes zero arguments.
- It is inherently name-insensitive unless the language is extended.
- It fires after full slot-access failure, not on each ancestor hop.
- Its returned value is memoized into the resolved missing slot.
- The default `omgwtf` behavior is throw.

### Why
Adding an implicit missing-name argument or multi-hop firing would introduce machinery the text does not license. The plain words “when slot access fails” fit full-chain failure best.

### Minimal tests
Distinct misses are independent:
```lolcode
SMOOSH box'Z a AN box'Z b MKAY
```
Expected: two misses / two hooks

Same missing slot repeated is memoization-sensitive:
```lolcode
SMOOSH box'Z a AN box'Z a MKAY
```
Expected: first access may synthesize; second access sees memoized value

User hook is name-insensitive:
- no hook parameters are passed

Default hook:
- missing slot on plain object throws

---

## Holding 12: slot-call after `omgwtf` synthesizes a non-function is a runtime callable/type error

### Text
- The spec distinguishes slot access (`'Z`) from slot-call (`IZ`) (`lolcode-spec-v1.3.md` lines 731-756).
- `omgwtf` may synthesize any value to install into the unknown slot (`lolcode-spec-v1.3.md` line 768).
- The checklist’s conservative reading is: do not silently degrade slot-call on a non-function into ordinary slot access (`lolcode_1_3_expert_review_checklist.md`, section I.4 / G4).

### Holding
If `omgwtf` synthesizes a non-function:
- plain slot access succeeds and returns the synthesized value;
- slot-call on that slot still fails with a callable/type error.

### Minimal test
```lolcode
HAI 1.3
HOW IZ I zero
  FOUND YR 0
IF U SAY SO

O HAI IM O
  I HAS A omgwtf ITZ zero
KTHX

VISIBLE O'Z missing
VISIBLE O IZ missing MKAY
KTHXBYE
```

Expected:
- first line prints `0`
- second line errors

---

## Holding 13: `izmakin` runs after the object is fully prototyped, with mixins applied and declared parent restored

### Text
- `izmakin` runs “after a bukkit is fully prototyped but before the prototyping method returns” (`lolcode-spec-v1.3.md` line 770).
- The assessment file says `izmakin` ordering is explicitly tested: the hook sees a fully prototyped post-mixin object with declared parent restoration applied (`NEXT-BOTTOM-UP-CONCERNS-ASSESSMENT-2026-03-05.md` lines 33-36).
- The adjudication ledger records `N19`: ordering pinned to post-prototype / mixin / parent-restored state (`NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md` line 50).

### Holding
The effective `izmakin` (after child/mixin/inherited precedence has been resolved) runs after:
1. mixin copying,
2. declared-parent restoration,
3. object assembly is otherwise complete.

### Why
That is exactly what “fully prototyped” has to mean in this object system.

### Minimal test
```lolcode
HAI 1.3
HOW IZ I boot
  FOUND YR ME'Z parent
IF U SAY SO

O HAI IM P
KTHX

O HAI IM M
  I HAS A izmakin ITZ boot
KTHX

I HAS A X ITZ A P SMOOSH M
VISIBLE BOTH SAEM X'Z parent AN P
KTHXBYE
```

Expected: `WIN`

---

## Holding 14: bare function identifiers denote function values; they do not perform nullary calls

### Text
- The function section says argument values are obtained before the function is called (`lolcode-spec-v1.3.md` lines 602-604).
- Slot assignment example stores a function directly: `<object> HAS A blogin ITZ blogin` (`lolcode-spec-v1.3.md` lines 624-641).

### Holding
A bare function identifier in expression position denotes the function value. Calls require `I IZ ... MKAY` or `<object> IZ ... MKAY`.

### Why
Otherwise the spec’s own function-in-slot example would make no sense.

### Minimal tests
```lolcode
HAI 1.3
HOW IZ I f
  FOUND YR 7
IF U SAY SO
I HAS A o ITZ A BUKKIT
o HAS A f ITZ f
VISIBLE o IZ f MKAY
KTHXBYE
```

Expected: `7`

And:
```lolcode
HAI 1.3
HOW IZ I f
  FOUND YR 7
IF U SAY SO
I HAS A g ITZ f
VISIBLE I IZ g MKAY
KTHXBYE
```

Expected if indirect-call syntax is supported through value binding; otherwise reject by parser/runtime policy. (Do not reinterpret bare `f` as a call.)

---

## Holding 15: there are no true lexical closures; closure-like behavior is object-backed, not definition-site capture

### Text
- Ordinary functions do not have access to the outer/calling code block’s variables (`lolcode-spec-v1.3.md` line 584).
- Object-called functions use function namespace -> calling object namespace -> non-object/global side (`lolcode-spec-v1.3.md` lines 664-700).

### Holding
LOLCODE 1.3 does not provide true lexical closures. What it does provide is movable function values and receiver-backed environment lookup when a function is invoked as a slot-call.

### Why
That matches the explicit “no outer locals” rule while preserving the receiver-dynamic object semantics.

### Minimal tests
No lexical capture:
- ordinary function cannot see a surrounding local unless passed explicitly

Closure-like receiver environment:
```lolcode
HAI 1.3
HOW IZ I constFromEnv YR x
  FOUND YR y
IF U SAY SO

O HAI IM env
  I HAS A y ITZ 7
  I HAS A constFromEnv ITZ constFromEnv
KTHX

VISIBLE env IZ constFromEnv YR SUM OF 2 AN 3 MKAY
KTHXBYE
```

Expected: `7`

If `env'Z y R 9`, a later call should return `9`, proving this is not lexical capture but receiver-time lookup.

---

## Holding 16: `SMOOSH` is strict/eager; project policy pins left-to-right evaluation and no rollback of earlier side effects

### Text
- `SMOOSH` implicitly casts all input values to YARNs (`lolcode-spec-v1.3.md` line 557).
- Ordinary function argument expressions are obtained before the call (`lolcode-spec-v1.3.md` lines 602-604).
- The project assessment pins call-argument ordering left-to-right and notes explicit `omgwtf` memoization/side-effect coverage (`NEXT-BOTTOM-UP-CONCERNS-ASSESSMENT-2026-03-05.md` lines 51-55, 67-68).

### Holding
Project policy: `SMOOSH` evaluates operands eagerly, left-to-right, with no rollback of earlier side effects if a later operand errors.

### Why
This is the narrowest non-fancy operational discipline once strict/eager evaluation is accepted.

### Minimal tests
Earlier side effect survives later error:
```lolcode
HAI 1.3
I HAS A x ITZ 0
VISIBLE SMOOSH (x R 1) AN missingVar MKAY
KTHXBYE
```
(Adapt into legal LOLCODE expression/side-effect form available in the implementation.)
Expected:
- side effect from operand 1 remains
- later operand error is still raised

Distinct missing accesses:
- `SMOOSH box'Z a AN box'Z b MKAY` => two misses

Same missing access repeated:
- `SMOOSH box'Z a AN box'Z a MKAY` => second sees memoized value

---

## Holdings expressly rejecting extensions

These are not optional conveniences. They are forbidden unless future archival evidence compels them.

1. No separate method namespace outranking callable slot values.
2. No synthetic fallback like `I IZ ghost'Z hi MKAY`.
3. No reinterpretation of `SRS` receiver results into namespace names.
4. No silent coercion from slot-call on a non-function into plain slot access.
5. No inherited `omgwtf`/`izmakin` masking by fresh per-object defaults unless the text forces it.
6. No deep-copy mixin semantics without textual support.
7. No parent-locked or definition-site-locked closure semantics for slot-called functions.
8. No new invisible dynamic/global `IT` store beyond the narrow ordinary-temporary reading.

---

## Remaining open items (if not already separately frozen)

As of this memo, the big issues are largely closed. The residual items are small and should be tracked separately from the settled holdings above:

1. Expression-level TYPE-word policy (only if the project has not already frozen it).
2. Any remaining documentation drift between TODO/checklist/map files.
3. Any missing direct regression for method fallthrough return vs receiver slot `IT`.

---

## Suggested archival note to future implementers

If a future reader thinks the spec “contradicts itself,” first try the narrower move:
- treat later, more specific object-language clauses as clarifying broad early prose;
- preserve distinct syntactic forms rather than normalizing them together;
- refuse extensions that add unseen machinery;
- ask what reading makes the most adjacent worked examples true at once.

That method resolved the major object-system hard calls in this project without rewriting the 1.3 text.

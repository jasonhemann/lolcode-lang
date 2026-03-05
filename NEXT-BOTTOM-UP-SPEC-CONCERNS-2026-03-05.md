# Next Bottom-Up Spec Concerns (LOLCODE 1.3)

Date: 2026-03-05  
Method: bottom-up reread of `spec/upstream/lolcode-spec-v1.3.md`, emphasizing OO/BUKKIT + control-flow intersections.

These are **risk candidates** (not all confirmed bugs).  
Each item is a concrete place where parser/runtime semantics can drift from the spec or where the English text is internally under-specified.

## A. BUKKIT / OO / Inheritance (bottom of spec upward)

1. **Mixin source-set ambiguity (own slots vs inherited slots)**  
   Spec refs: lines 849, 857, 871-873.  
   Risk: one clause says copy slots "defined on the mixin"; example says include mixin parent slots too.

2. **Mixin precedence and override order under parent + multiple mixins**  
   Spec refs: lines 849, 855.  
   Risk: reverse declaration order and parent replacement can produce conflicting precedence rules.

3. **Mixin copy depth (shallow vs deep)**  
   Spec refs: lines 849, 857.  
   Risk: static mixin wording does not specify whether copied slot values are aliased objects/functions or cloned values.

4. **`parent` slot mutation to non-BUKKIT values**  
   Spec refs: line 790, lines 796-799.  
   Risk: text allows changing `parent`; behavior if set to NUMBR/YARN/FAIL is unspecified.

5. **Cycle safety after dynamic reparenting**  
   Spec refs: lines 790, 796.  
   Risk: cycle-termination is mentioned for lookup but not for assignment/write traversal paths.

6. **Copy-on-write assignment target in ancestor chain**  
   Spec refs: line 798.  
   Risk: must copy into current object, not mutate ancestor; easy to get wrong with shared slot boxes.

7. **Copy-on-write for inherited function slots**  
   Spec refs: lines 798, 804.  
   Risk: assignment semantics for function-valued slots can accidentally preserve wrong receiver scope.

8. **`parent`/`omgwtf`/`izmakin` inheritance behavior**  
   Spec refs: lines 758-770, 790.  
   Risk: unclear whether child objects should inherit or shadow special-slot handlers before explicit declaration.

9. **Receiver-projected scope for slot-access function calls**  
   Spec refs: lines 804, 810.  
   Risk: callable pulled from parent/global slot must still resolve variables from access receiver.

10. **Dynamic method name call with `SRS`**  
    Spec refs: lines 738, 741-753.  
    Risk: parse/eval order bugs if method-name expression has side effects.

11. **Method-call argument grammar (`<variable>` vs `<expression>`) mismatch**  
    Spec refs: lines 744-745 vs function-call lines 599-602.  
    Risk: method calls may be over-restricted or over-permissive depending on parser choice.

12. **`omgwtf` semantics: cache-or-not on missing slot**  
    Spec refs: line 768.  
    Risk: text says return value is "placed in unknown slot"; many implementations forget memoization.

13. **`omgwtf` recursion hazard**  
    Spec refs: line 768.  
    Risk: if `omgwtf` itself accesses missing slot, recursion policy is unspecified.

14. **`izmakin` invocation phase ordering**  
    Spec refs: line 770, lines 774-790, 849-857.  
    Risk: unclear whether hook runs before/after mixin copy and parent-slot finalization.

15. **`izmakin` reentrancy/recursive prototyping behavior**  
    Spec refs: line 770.  
    Risk: hook can create/prototype bukkits; lifecycle and IT/scope interactions can diverge.

16. **`O HAI IM` lookup mode (slot-first then global) vs lexical locals**  
    Spec refs: line 725.  
    Risk: local declarations inside block can be bypassed by slot-first lookup.

17. **"Anything `I` inside codeblock refers to `<object>`" parsing collision**  
    Spec refs: line 714.  
    Risk: `I HAS A`, `I IZ`, and bare `I` forms can map to different AST categories.

18. **`ME` access in nested call contexts**  
    Spec refs: line 684.  
    Risk: behavior of `ME` inside helper functions invoked from methods is under-specified.

19. **Function-namespace composition in method context**  
    Spec refs: lines 666-674.  
    Risk: wording around "identifier `I`" in function namespace is unclear and easy to misread.

20. **`HOW IZ <object> <slot>` parse shape collisions**  
    Spec refs: lines 649-652.  
    Risk: disambiguation from `HOW IZ I <name>` and from SRS-named object references can fail.

21. **Slot-key domain conflict: identifier-only syntax vs numeric-index claim**  
    Spec refs: line 612 vs lines 629, 634, 738.  
    Risk: parser/runtime may accidentally forbid valid numeric slot indices.

22. **Top-level `I HAS A <obj> ITZ A BUKKIT` scope wording**  
    Spec refs: line 616 ("current object's scope").  
    Risk: top-level is not clearly an object context; implementation choice must be explicit.

## B. Functions / Flow / Labels / Mutation

23. **`GTFO` dual semantics precedence (break vs return NOOB)**  
    Spec refs: line 591 vs loops/switch sections (486, 552).  
    Risk: nested switch-in-function/loop-in-function can break wrong context.

24. **No-closure statement vs object/global fallback**  
    Spec refs: line 584 vs lines 666-670.  
    Risk: spec can be read as prohibiting outer captures but allowing global/object captures.

25. **Argument evaluation order and side effects**  
    Spec refs: line 602.  
    Risk: IT and mutation outcomes depend on left-to-right vs unspecified eval order.

26. **Loop updater order relative to `TIL`/`WILE` checks**  
    Spec refs: lines 559-564.  
    Risk: pre-check/post-check differences produce off-by-one loop behavior.

27. **Loop updater variable shadow/restore semantics**  
    Spec refs: line 564.  
    Risk: temporary loop variable can leak or overwrite outer binding on escapes.

28. **Label syntax constraints and dynamic labels**  
    Spec refs: lines 552, 559-562.  
    Risk: label is required but "unused"; whether `SRS`/computed labels are legal is unclear.

29. **Infinite-loop termination through nested constructs**  
    Spec refs: lines 552, 486.  
    Risk: `GTFO` inside nested `WTF?` should not accidentally exit outer loop/function.

30. **`WTF?` literal-uniqueness equality mode**  
    Spec refs: line 486.  
    Risk: duplicate detection can vary (string vs numeric equivalence, cast/no-cast).

31. **`WTF?` fallthrough to `OMGWTF` after a match**  
    Spec refs: line 486.  
    Risk: does `OMGWTF` run only on no-match, or can fallthrough reach it?

32. **`IT` locality clause vs method-global IT clause**  
    Spec refs: lines 407, 411 vs line 672.  
    Risk: IT behavior changes by context; easy to implement inconsistently.

## C. Operators / Types / Names / Parsing

33. **Optional `AN` causes keyword/identifier ambiguity**  
    Spec refs: lines 277-281, 170.  
    Risk: `AN` as identifier via `SRS` collides with separator token role.

34. **Implicit EOL closure for variadics in nested expressions**  
    Spec refs: lines 269, 286, 356, 383.  
    Risk: parser may close too early/late with comma and continuation interactions.

35. **`MAEK` target-type domain mismatch with BUKKIT language type set**  
    Spec refs: lines 365-368 vs line 612.  
    Risk: cast target set excludes BUKKIT explicitly; implementations often over-extend.

36. **Host-dependent numeric limits and precision policy**  
    Spec refs: lines 233, 235.  
    Risk: cross-implementation divergence if bounds/float format assumptions are implicit.

37. **String-to-number cast grammar edge cases**  
    Spec refs: line 237.  
    Risk: exponent forms, leading plus, whitespace, and multiple hyphens are unspecified.

38. **`SRS` "any identifier position" boundary**  
    Spec refs: line 170.  
    Risk: whether SRS is valid for labels, function args, type positions, and object names can drift.

39. **Comment + continuation + comma interactions in block comments**  
    Spec refs: lines 40, 65-83.  
    Risk: `OBTW/TLDR` same-line-with-comma behavior can desynchronize statement boundaries.

40. **Unicode normative-name escape compliance details**  
    Spec refs: line 255.  
    Risk: normalization/casing/version (4.1 names list) and alias handling are underspecified.

41. **Version handling policy gap in spec text**  
    Spec refs: line 89.  
    Risk: strict `HAI 1.3` policy is implementation-defined; corpus triage must distinguish policy vs divergence.

## D. "Same surface form, different AST" hotspots to keep watching

42. **`I HAS A` variable declaration vs slot declaration in `O HAI` context**  
    Spec refs: lines 117, 629, 714.

43. **`HOW IZ I` global function vs `HOW IZ <object> <slot>` method**  
    Spec refs: lines 574, 649.

44. **`I IZ` function call vs `<object> IZ` method call**  
    Spec refs: lines 599, 744.

45. **`<target> R <expr>` variable assignment vs slot assignment (`'Z` lvalue)**  
    Spec refs: line 205, lines 731-738.

46. **`SMOOSH` as string variadic op vs mixin-inheritance constructor form**  
    Spec refs: line 356 vs lines 838-845.

47. **`GTFO` in switch/loop/function bodies with different control meaning**  
    Spec refs: lines 486, 552, 591.

48. **`IT` as implicit temp vs explicit global-lookup behavior in methods**  
    Spec refs: lines 407, 411, 672.

1. You need separate AST nodes for ordinary function definition and method-in-slot definition. HOW IZ I <name> and HOW IZ <object> <slot> are not the same construct with a missing argument; they produce different lookup and receiver behavior. Do not desugar them together early. Also, the spec itself contains editorial drift (HOW DUZ I in one example, HOW IZ I in the real function section), so examples are not safe grammar sources.

2. You need separate AST nodes for ordinary call and slot-call. I IZ f MKAY and obj IZ f MKAY are semantically different because the second one establishes a receiver-sensitive lookup regime and enables ME. This is not surface sugar.

3. You need separate AST nodes for variable declaration, slot declaration, variable assignment, slot assignment, and recast assignment. I HAS A x, obj HAS A x, x R ..., ME'Z x R ..., and x IS NOW A T all have different namespace and mutation behavior. If you collapse them into one “assignment-ish” node, you will implement at least one of them wrong.

4. SRS is not just an ordinary expression operator. The spec says it may appear anywhere a regular identifier is expected. That means you need a distinct “dynamic-name” node for variable names, slot names, and maybe function names, not just a value expression node reused everywhere.

5. SMOOSH is overloaded across two different syntactic categories: a variadic YARN expression and a mixin/inheritance clause. Those should not share an AST class. One produces a string at runtime; the other changes object construction semantics. That is a classic novice-spec collision.

6. The slot-access operator is itself editorially unstable: the prose says the operator is -, while the grammar and examples use 'Z. Treat 'Z as the real token and mark the dash as a spec typo, otherwise your lexer or tests will drift.

7. The token I is doing three different jobs: part of I HAS A, part of HOW IZ I, and part of I IZ ... MKAY; then inside O HAI IM the prose says “Anything I inside the codeblock actually refers to <object>.” That is not one semantic thing. It is a family of unrelated syntactic markers plus one contextual rewrite rule.

8. The object layer introduces special identifiers and slots (ME, parent, omgwtf, izmakin, and effectively IT) without ever cleanly saying whether they are reserved, shadowable, or just conventional names. You need to decide that explicitly. Otherwise lookup will depend on ad hoc implementation order.

9. You need a preprocessing phase before parsing proper. Comma is a virtual newline, ... joins physical lines into one command, single-line comments terminate at newline and ignore trailing comma/ellipsis after BTW, and strings ignore both comma and ellipsis. If you do not normalize statement boundaries first, implicit MKAY closure, VISIBLE termination, and one-line HAI 1.3, KTHXBYE cases will all become parser bugs.

10. The scope model is internally contradictory. Early on, the spec says all variable scope is local to function or main block and that there is no global scope. Later, method lookup explicitly searches function namespace, calling object namespace, and “global” namespace. That is not a wording glitch; it is a semantic contradiction.

11. The function model is also contradictory. The ordinary function section says functions do not have access to the outer/calling code block’s variables. The bukkit section then gives methods receiver-sensitive access to the calling object’s namespace and a global namespace. That means “function” and “method” are semantically different entities even if both are stored as FUNKSHUN values.

12. IT is specified two different ways. Bare expression statements update a local IT that remains in local scope. But bukkit-method scope says IT is always looked up from global namespace. Those cannot both be true without a more elaborate dynamic-environment model than the spec ever states.

13. O HAI IM introduces a third lookup regime: identifiers inside the block are looked up by slot-access first, then global, then error. That bypasses the earlier ordinary local-scope story. So you now have at least three distinct lookup algorithms in one language: ordinary local lookup, method lookup with receiver, and object-body lookup. That should be formalized, not left as prose.

14. Function names and variable names share a namespace, and function values are rebindable like ordinary variables. But the example claiming duplicate declaration is an error is followed by code that reassigns the same name to 0, which reads like the spec is showing state after an earlier erroring line. This is exactly the kind of English-spec slippage that causes implementers to infer different rules.

15. There is a deep semantic fault line around “function value” versus “method call.” The spec says no matter where a FUNKSHUN is stored, a slot-access call makes it obtain variables from the object it was accessed from. That means the function’s free-name resolution is determined by call form, not by where the function was defined or stored. This is neither normal lexical closure nor normal prototype dispatch; it is a distinct third thing.

16. The spec never clearly says what happens when you extract a method-like function value and call it later without slot-call syntax. Does it lose receiver binding? Is there any such thing as a bound method object? The syntax suggests “no,” but the semantics are not stated. That gap will matter immediately for higher-order code.

17. BUKKIT is editorially split across versions. The type section still says arrays/BUKKIT are reserved for future expansion, while the later sections fully define BUKKITs as containers/objects with slots, methods, inheritance, mixins, and special slots. You need to pick one version of reality and treat the other as stale text.

18. LIEK A does not clearly say whether prototyping copies slots eagerly, installs only a parent pointer, or does some hybrid. The later inheritance-of-slots prose sounds like parent-chain lookup, but mixins explicitly copy slots statically. So there are two object-construction models in the same section, and their interaction is underspecified.

19. izmakin is constructor-like, but the trigger point is vague: “after a bukkit is fully prototyped but before the prototyping method returns.” You need to decide whether it fires for plain A BUKKIT, for LIEK A, for O HAI IM, for mixins, for parent mutation, and whether inherited izmakin runs with the child as receiver.

20. omgwtf is underdefined in exactly the dangerous place: missing-slot behavior. The prose says it runs when slot access fails and may synthesize a value into the unknown slot. It does not say whether failure is checked before or after parent lookup, whether non-callable slot invocation counts as slot-access failure, whether the hook runs once or per ancestor, or which object’s omgwtf is consulted.

21. Parent mutation means you must run cycle detection on every operation that follows parent links, not just ordinary lookup. The prose explicitly allows changing the parent slot and explicitly mentions stopping when a parent has already been searched. So access, assignment-existence checks, mixin-like copying from parents, and probably omgwtf fallback all need a visited-set.

22. Object assignment is copy-on-write shadowing, not ancestor mutation. If a name exists only in an ancestor, assignment from the child creates a new slot in the child and sets that. That is subtle, nonstandard, and very easy to get wrong if you implement slot assignment as ordinary parent-chain update.

23. You need explicit rules for whether special slots participate in inheritance, shadowing, and mixin copying. parent is special and mutable. omgwtf is special and behavior-bearing. izmakin is special and construction-bearing. The spec never cleanly says whether copying or overriding them is legal, ignored, or itself special-cased.

24. Mixin precedence is only half specified. Slots are copied in reverse order of declaration of mixins, but you still need rules for ties between: later mixin vs earlier mixin, mixin vs parent, local declarations inside O HAI IM, and special slots. Also the later example implies copying parent slots from a mixin object, which is stronger than the earlier “slots defined on the mixin” wording. That is an inconsistency, not just a missing example.

25. The slot-key model is unfinished. The prose says slots may be indexed by NUMBR or YARN, but the syntax only gives identifier slot names or SRS <expr>. So you need to decide whether SRS can evaluate to numeric keys, whether "3" and 3 are distinct keys, and whether bare identifiers are just sugar for YARN slot names.

26. Self-reference during object construction is not specified. In O HAI IM obj, is obj bound inside its own initializers before the object is fully built? Are earlier slots visible to later slot initializers? Can izmakin observe partially initialized state? That matters for recursive object graphs and method self-reference.

27. GTFO is overloaded across three control effects: loop break, switch break, and function return NOOB. The spec never states a general nearest-enclosing-target rule. Without that, nested loop/switch/function bodies are ambiguous.

28. Loop labels are required but “unused, except for marking the start and end of the loop.” That means you still need a matching rule, and probably an error for mismatched labels, nested duplicate labels, and malformed exits. The prose does not say any of that.

29. The timing of iteration-loop updates and tests is not actually nailed down. The spec says the operation is applied to the temporary loop variable and then explains TIL/WILE in prose, but it never cleanly says whether the step happens before the body, after the body, before the test, or after the test. With mutation, that is observable.

30. Allowing “any unary function” as the loop operation opens another hole. Does the loop accept only ordinary named functions, or slot-calls too? What if the function is not unary at runtime? What if it mutates globals or the receiver? What if it returns NOOB? The prose invites higher-order behavior but never specifies the contract.

31. WTF? uniqueness is underspecified. “Each literal must be unique” is clear enough, but the spec never says whether duplicate detection is a parse-time error, definition-time error, first-execution error, or simply undefined. Since YARN-with-interpolation is excluded from literals, you also need a real literal-normalization rule before checking uniqueness.

32. WTF? fallthrough plus errors needs a rule. The prose explains fallthrough when no GTFO occurs, but says nothing about what happens when a statement in an OMG block errors. Normal language design would stop execution, but the spec should say so because this is one of those places where informal prose lets people imagine “skip to next arm” behavior.

33. Blank case bodies are definitely intended, because the example has OMG "G" followed immediately by OMG "B". Your parser and AST need to represent empty blocks explicitly.

34. Variadic closure is statement-boundary-sensitive, not line-sensitive. MKAY may be omitted at end of line/statement, VISIBLE is terminated by line end or comma, comma is a virtual newline, and ... destroys the physical newline as a statement boundary. So your implicit-closure algorithm must operate over logical statements after preprocessing, not over raw lines.

35. The spec’s GC language is not really implementable as a normative requirement. “Will be garbage collected in the future” is not something a conformance suite can observe portably. Treat that as a memory-model note, not semantics.

36. Equality for BUKKITs and FUNKSHUNs is missing. BOTH SAEM only gives numeric special cases and says otherwise there is no automatic casting. It never states whether object/function equality is pointer identity, structural equality, or simply unsupported. That will surface immediately in WTF?, BOTH SAEM, and duplicate-literal checking if TYPE values or object-like literals ever expand.

37. The TYPE/NOOB story is unstable. TYPE is “under current review,” NOOB is both a value and also named as a TYPE literal, and the boolean-casting prose plus NOOB-casting prose invites confusion between the value NOOB and the TYPE literal NOOB. That needs a formal value/type distinction, not just English sentences.

38. The optional article A should be treated narrowly, not generalized. The spec only explicitly relaxes it in the I HAS A SRS name ... declaration context, while A also appears in ITZ A, MAEK ... A <type>, IS NOW A, and LIEK A. If you implement “article optional everywhere,” you will invent grammar the spec does not actually state.

39. Functions are described as first-class values, but the language does not define a general call-on-expression form. That means you can store a function in a variable or slot, but the only call syntaxes are name-based and slot-name-based. That gap is not cosmetic; it determines whether higher-order programming actually exists.

40. Argument evaluation order is only partly specified. The spec says argument expressions are evaluated before the call, but not whether evaluation is left-to-right. Once you admit mutation, GIMMEH, dynamic slot names, or method calls with side effects, that order matters.

The shortest way to say the whole thing is this: the spec needs three formally separate semantic relations and it currently blurs them together. You need one for ordinary name lookup, one for slot lookup, and one for slot-call evaluation with receiver binding. Most of the nastiest bugs you are worried about are just consequences of failing to keep those three apart.

If I were prioritizing, I would settle these first: 2, 10–15, 20–24, 27, and 34. Those are the ones that will poison the AST, the evaluator, and the test suite all at once.


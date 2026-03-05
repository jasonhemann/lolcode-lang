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

---

If we want, this can be converted directly into a new ordered adjudication checklist (like the prior 42-item pass), with one spec-anchored positive/negative test target per item.

# Next Bottom-Up Spec Concerns (Integrated + Renumbered)

Date: 2026-03-06
Sources:
- Original bottom-up concern list
- Prior normalized concern pass
- `third-tier-of-40-issues.md` (newly integrated)
- `fourth-tier-of-40-issues.md` (newly integrated)

Target: strict LOLCODE 1.3 only.

Policy reference: `spec/traceability/ADJUDICATION_POLICY.md`.

## Adjudication Order (Restart Pass 2)

Primary tranche (carry-forward priority + new parser/IT control additions):

1. `N02`
2. `N10`-`N15`
3. `N20`-`N24`
4. `N27`
5. `N34`
6. `N44`, `N51`, `N53`, `N54`, `N56`, `N60`, `N61`

Secondary tranche:

- `N01`, `N03`-`N09`, `N16`-`N19`, `N38`, `N42`, `N43`, `N45`-`N50`, `N52`, `N55`, `N57`-`N59`, `N63`, `N64`, `N67`, `N68`

Tertiary tranche:

- `N25`, `N26`, `N28`-`N33`, `N35`-`N37`, `N39`-`N41`, `N62`, `N65`, `N66`, `N69`

Quaternary tranche (low-priority additions from fourth-tier sweep):

- `N70`-`N85`

## Unified Concern List

1. `N01` Method-definition AST split (`HOW IZ I` vs `HOW IZ <object> <slot>`).
2. `N02` Call-form AST split (`I IZ` vs `<object> IZ`) and receiver semantics.
3. `N03` Separate declaration/assignment/recast/slot-assignment nodes.
4. `N04` `SRS` as dynamic identifier node (not only ordinary expression).
5. `N05` `SMOOSH` expression vs mixin/inheritance `SMOOSH` constructor disambiguation.
6. `N06` Slot-access token mismatch in prose (`-`) vs grammar/examples (`'Z`).
7. `N07` Multi-role `I` token: declaration marker, call marker, and object-body contextual rewrite.
8. `N08` Special identifiers/slots reservation and shadowing policy (`ME`, `parent`, `omgwtf`, `izmakin`, `IT`).
9. `N09` Pre-parse statement boundary normalization (comma, continuation, comment interaction).
10. `N10` Scope contradiction: early "no global scope" text vs object-method global lookup prose.
11. `N11` Function model contradiction: "no outer capture" vs object/global fallback semantics.
12. `N12` `IT` contradiction: local temporary vs "always global" in method context.
13. `N13` `O HAI IM` lookup regime (slot-first then global) and interaction with lexical locals.
14. `N14` Shared namespace of function and variable bindings; redeclaration narrative inconsistency.
15. `N15` Function-value semantics under slot-call receiver projection.
16. `N16` Extracted method/function value behavior when called without slot-call syntax.
17. `N17` Stale "BUKKIT reserved" text vs later full BUKKIT object model.
18. `N18` `LIEK A` object construction model (prototype-chain vs eager copy implications).
19. `N19` `izmakin` trigger ordering relative to prototyping/mixin/parent finalization.
20. `N20` `omgwtf` missing-slot behavior boundaries and memoization semantics.
21. `N21` Parent mutation cycle safety across all parent-chain operations.
22. `N22` Copy-on-write inherited assignment target semantics.
23. `N23` Special slot inheritance/shadow/mixin behavior (`parent`, `omgwtf`, `izmakin`).
24. `N24` Mixin precedence/source-set ambiguity (own-only vs inherited slots on mixin source).
25. `N25` Slot-key domain: identifier syntax vs NUMBR/YARN indexing claims.
26. `N26` Self-reference and visibility during object construction.
27. `N27` `GTFO` nearest-target rule across loop/switch/function nesting.
28. `N28` Loop label matching/uniqueness/error policy.
29. `N29` Loop updater timing relative to condition checks/body execution.
30. `N30` Updater contract for "any unary function" and side-effect boundaries.
31. `N31` `WTF?` duplicate-literal uniqueness stage and equality mode.
32. `N32` `WTF?` error propagation and `OMGWTF` interaction.
33. `N33` Blank `OMG` case bodies as first-class parse/runtime cases.
34. `N34` Variadic closure over logical statement boundaries (`MKAY` omission, comma, continuation).
35. `N35` GC prose as non-portable note vs normative requirement.
36. `N36` Equality semantics for `BUKKIT` and `FUNKSHUN` values (identity vs structural vs unsupported).
37. `N37` `TYPE` and `NOOB` value/type distinction stability.
38. `N38` Optional article `A` scope of applicability (narrow grammar-site handling).
39. `N39` Higher-order callability gap (function values are storable but call syntax is name/slot-shaped).
40. `N40` Argument evaluation order determinism under side effects.
41. `N41` Dynamic labels (`SRS`) admissibility and parse/runtime constraints.
42. `N42` Method argument grammar mismatch (`<variable>` wording vs expression-friendly call prose).
43. `N43` Keyword case-sensitivity policy (keywords vs identifiers).
44. `N44` Fixed preprocessing pipeline order (newline normalization, comments, continuation, comma, shielding).
45. `N45` Continuation marker normalization (`...` and `…`) including trailing-whitespace boundary policy.
46. `N46` Inline block-comment permissiveness and `TLDR` immediate handoff behavior.
47. `N47` NUMBAR lexical edge grammar (`.5`, `2.`, `-.5`, `-0.`) strictness policy.
48. `N48` String-to-number cast grammar strictness for sign/dot placement multiplicity.
49. `N49` Malformed escape failure semantics (hex, Unicode normative name, surrogate, out-of-range).
50. `N50` Interpolation scanner precedence (`::` escape before `:{...}` placeholder start).
51. `N51` Longest-match tokenization for multiword/punctuated keywords.
52. `N52` Assignment grammar normalization (`<variable> R <expression>` canonical form).
53. `N53` `O RLY?` predecessor-`IT` binding and comma/newline delimitation boundaries.
54. `N54` `MEBBE` truthiness semantics (`WIN` literal test vs TROOF-cast semantics).
55. `N55` Rejection behavior for orphan `MEBBE` / `NO WAI` forms.
56. `N56` `WTF?` predecessor-`IT` binding and delimitation boundaries.
57. `N57` Loop-label case-sensitivity and duplicate-label policy.
58. `N58` `HOW DUZ I` vs `HOW IZ I` canonical grammar policy.
59. `N59` Undefined phrase `SRS BIZNUS cast` mapped to concrete parser/runtime behavior.
60. `N60` Closed list of syntactic forms that update `IT`.
61. `N61` `VISIBLE` as statement-special variadic (delimiter closure + suffix `!` behavior).
62. `N62` `GIMMEH` undeclared-target policy (implicit declaration vs declaration-required).
63. `N63` TYPE-word dual role (TYPE literal values vs type designators).
64. `N64` Context-sensitive parsing of type designators in `MAEK` and `IS NOW A`.
65. `N65` Equality policy for non-numeric complex values (`BUKKIT`, `FUNKSHUN`, `TYPE`).
66. `N66` Built-in immutability statement vs observable object identity policy.
67. `N67` `ME` parse acceptance and runtime-only failure when no receiver exists.
68. `N68` `HOW IZ <object> <slot>` receiver existence/type check stage (parse, definition time, call time).
69. `N69` Receiver late-binding invariant for mixin-copied function values.
70. `N70` Reserved-word/literal/special-name collision policy in identifier positions.
71. `N71` Version token acceptance policy (`HAI <version>`) under spec-declared nonstandard handling.
72. `N72` Truthiness semantics for empty BUKKIT/array wording conflict.
73. `N73` Numeric portability policy for overflow/underflow/Inf/NaN/division-by-zero behavior.
74. `N74` Statement value-status policy for IT-sensitive default returns (`VISIBLE`, `GIMMEH`, others).
75. `N75` Assignment/declaration RHS sequencing relative to target binding visibility.
76. `N76` Forward-reference policy for function calls before function-definition statements.
77. `N77` Duplicate function-parameter-name policy.
78. `N78` Function-definition placement semantics (declaration/executable/conditional/loop nesting policy).
79. `N79` `ME HAS A` receiver-slot declaration shadow/overwrite behavior against inherited slots.
80. `N80` `ME'Z slot R expr` evaluation sequencing and same-slot read/write interaction.
81. `N81` Mixin copy depth semantics for mutable slot values (deep clone vs shallow alias).
82. `N82` Mutable-value aliasing policy (call-by-sharing) across function args and slot assignment.
83. `N83` Non-BUKKIT parent-slot mutation policy (`NOOB`/primitive parent values).
84. `N84` `omgwtf` method-call fallback when synthesized missing-slot value is non-callable.
85. `N85` `izmakin` failure atomicity (binding visibility on constructor failure).

## Third-Tier Crosswalk

Integrated from `third-tier-of-40-issues.md`:

- New IDs: `N43`-`N69`.
- Mapped to existing IDs (not renumbered as new): `N06`, `N07`, `N09`, `N12`, `N35`, `N38`, `N41`.

## Fourth-Tier Crosswalk

Integrated from `fourth-tier-of-40-issues.md`:

- New IDs: `N70`-`N85`.
- Mapped to existing IDs (not renumbered as new): `N01`, `N06`, `N07`, `N09`, `N10`, `N11`, `N12`, `N17`, `N18`, `N19`, `N20`, `N21`, `N23`, `N24`, `N25`, `N27`, `N34`, `N40`, `N44`, `N45`, `N46`, `N47`, `N48`, `N49`, `N51`, `N58`, `N60`, `N61`, `N62`, `N63`, `N64`, `N65`, `N69`.

## Status Keys

- `pending`: not yet adjudicated under policy.
- `adjudicated`: policy decision made, implementation aligned.
- `needs-change`: policy decision made, implementation not yet aligned.
- `spec-underdetermined`: no single implied behavior; explicit project policy required.

## Tracking

Restart-pass adjudication tracking is in `spec/traceability/ADJUDICATION_LEDGER.md`.

# Next Bottom-Up Spec Concerns (Normalized)

Date: 2026-03-06
Source: consolidated and deduplicated from the original bottom-up list and the appended follow-up notes.
Target: strict LOLCODE 1.3 only.

Policy reference: `spec/traceability/SPEC_ADJUDICATION_POLICY.md`.

## Adjudication Order

The user-prioritized order is preserved first:

1. `N02`
2. `N10`-`N15`
3. `N20`-`N24`
4. `N27`
5. `N34`

Then continue by tranche:

- Tranche 2: `N01`, `N03`-`N09`, `N16`-`N19`
- Tranche 3: `N25`, `N26`, `N28`-`N33`, `N35`-`N42`

## Normalized Concern List

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

## Status Keys

- `pending`: not yet adjudicated under policy.
- `adjudicated`: policy decision made, implementation aligned.
- `needs-change`: policy decision made, implementation not yet aligned.
- `spec-underdetermined`: no single implied behavior; explicit project policy required.

## Kickoff Tracking

Initial execution starts with tranche 1 in `spec/traceability/NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md`.

# Tranche 1 Adjudication (Restart Pass 2)

Date: 2026-03-06
Source list:
- `NEXT-BOTTOM-UP-SPEC-CONCERNS-2026-03-05.md`
- `third-tier-of-40-issues.md`
- `fourth-tier-of-40-issues.md`

Policy: `spec/traceability/SPEC_ADJUDICATION_POLICY.md`

Pass-2 tranche-1 targets:
- Carry-forward: `N02`, `N10`-`N15`, `N20`-`N24`, `N27`, `N34`
- Added from third-tier integration: `N44`, `N51`, `N53`, `N54`, `N56`, `N60`, `N61`

## Carry-Forward Results

| ID | Status | Summary |
| --- | --- | --- |
| `N02` | adjudicated | Distinct AST/runtime call paths for `I IZ` vs `<object> IZ`. |
| `N10` | adjudicated | Object-function lookup clauses interpreted as specific override to broad scope prose. |
| `N11` | adjudicated | Ordinary functions do not capture lexical outer locals; method/slot-call path is object-aware. |
| `N12` | adjudicated | `IT` local in ordinary scopes; method-context `IT` resolves through global lookup rule. |
| `N13` | adjudicated | `O HAI IM` body uses slot-first then global lookup (`object-block-slot-first-over-global-src`). |
| `N14` | adjudicated | Function and variable declarations share one namespace with duplicate declaration rejection. |
| `N15` | adjudicated | Slot-call receiver projection controls callable name lookup scope. |
| `N20` | adjudicated | `omgwtf` missing-slot path memoizes synthesized value to the missing slot. |
| `N21` | adjudicated | Parent-chain traversal is cycle-safe across lookup/assignment/method paths. |
| `N22` | adjudicated | Copy-on-write assignment for inherited slots; ancestor slot is not mutated by child assignment. |
| `N23` | adjudicated | Special-slot policy table fixed and tested (`parent`, `omgwtf`, `izmakin`). |
| `N24` | adjudicated | Mixin source-set fixed to own members only (inherited members not copied). |
| `N27` | adjudicated | `GTFO` uses nearest valid control target semantics. |
| `N34` | adjudicated | Variadic implicit closure runs over logical statements after formatting preprocess. |

## Pass-2 Additions Started

| ID | Status | Decision / Action |
| --- | --- | --- |
| `N44` | adjudicated | Deterministic preprocessing order is fixed and documented (`PREPROCESSING_AND_KEYWORD_POLICY.md`) with ordering-sensitive regressions (`inline-block-comment-tldr-handoff`, `preprocess-order-runtime-src`). |
| `N51` | adjudicated | Canonical longest-match keyword policy is fixed for punctuated and phrase tokens (`spaced-orly-question`, `spaced-wtf-question`, `split-im-outta-phrase`). |
| `N53` | adjudicated | `O RLY?` binds to current `IT`; statement delimiter behavior remains expression-driven (`stmt-if` uses `IT` directly). |
| `N54` | adjudicated | `MEBBE` uses TROOF-cast truthiness semantics; pinned by regression `orly-mebbe-truthy-cast-src`. |
| `N56` | adjudicated | `WTF?` binds to current `IT`; parser encodes `stmt-switch` with subject `(expr-ident \"IT\")`. |
| `N60` | adjudicated | IT update closed-list is documented (`IT_UPDATE_MATRIX.md`) and enforced by regression `it-update-matrix-src` plus supporting IT tests. |
| `N61` | adjudicated | `VISIBLE` remains statement-special variadic with delimiter closure and `!` suffix newline suppression. |
| `N43` | adjudicated | Keyword/literal/type recognition is strict-case in direct syntax positions; lowercase lookalikes remain identifiers (per identifier case-sensitivity text and strict extension policy). |
| `N42` | adjudicated | Method-call argument positions use expression semantics for coherence with call-expression section; parser/runtime tests now pin expression-argument method calls. |
| `N63` | adjudicated | TYPE-words are dual-role by context: expression-position words remain TYPE literals, while cast-target positions require strict cast target designators. |
| `N64` | adjudicated | Parser now enforces cast-target domain for both `MAEK <expr> [A] <type>` and `<lvalue> IS NOW A <type>` forms (`TROOF|YARN|NUMBR|NUMBAR|NOOB` only). |
| `N65` | adjudicated | Equality remains numeric-mode only for numeric pairs; non-numeric values use non-coercing host equality, with identity behavior pinned for BUKKIT/function values. |
| `N19` | adjudicated | `izmakin` ordering is pinned to post-prototype/mixin parent-restored state; reentrant prototype creation from `izmakin` is allowed and tested per-prototype execution. |
| `N81` | adjudicated | Mixin copy depth for mutable slot values is call-by-sharing (shallow object reference copy), pinned by `mixin-static-snapshot-mutable-alias-src`. |
| `N82` | adjudicated | Mutable-value aliasing policy is consistent across mixin copy and ordinary assignment paths: shared BUKKIT references remain shared unless explicitly re-bound. |
| `N20` | adjudicated (extended) | `omgwtf` missing-slot policy is pinned for stateful hooks: return-value memoization is authoritative for the resolved slot name even if intermediate same-slot mutation occurs inside `omgwtf`. |
| `N13` | adjudicated (edge policy) | `omgwtf` same-slot recursive re-entry is trapped as deterministic runtime error to avoid silent divergence in spec-underdetermined recursion scenarios. |
| `N70` | adjudicated | Reserved literal/special names are rejected at user binding sites (declarations, function/method/object names, parameter names) via runtime binder gate; added regressions for `WIN`/`ME` declarations and `FAIL`/`NOOB`/`TROOF` def-name/param/object collisions. |
| `N71` | adjudicated | Version acceptance remains strict `1.3`; unsupported versions and missing-version behavior are pinned by parse negatives (`unsupported-v12`, `unsupported-v14`, `missing-version`). |
| `N72` | adjudicated | BUKKIT values are truthy (no empty-container false special case), now explicitly pinned (`empty-bukkit-truthy-src`). |
| `N73` | adjudicated | Numeric portability follows host runtime: division by zero surfaces runtime error, and large NUMBR arithmetic remains exact (`quoshunt-division-by-zero-runtime-error-src`, `numbr-bignum-arithmetic-src`). |
| `N74` | adjudicated | IT-sensitive statement update policy remains the closed-list captured by `N60` and enforced by matrix regression (`it-update-matrix-src`). |
| `N75` | adjudicated | RHS sequencing is now pinned: declaration RHS cannot see the binding being created, assignment RHS reads prior binding value (`declaration-rhs-does-not-see-binding-being-declared-src`, `assignment-rhs-sees-prior-binding-value-src`). |
| `N76` | adjudicated | No forward-reference prebinding for functions; call-before-definition is runtime error (`function-forward-reference-runtime-error-src`). |
| `N77` | adjudicated | Duplicate function parameter names are rejected by same-scope binding rules at call frame construction (`function-duplicate-params-runtime-error-src`). |
| `N78` | adjudicated | Nested function definitions are rejected under strict 1.3 parser policy (`nested HOW IZ I definitions are not allowed in strict 1.3` parse negatives). |

## N23 Policy Table: Special Slots

| Special slot | Prototype inheritance path | Mixin-copy path | Override precedence | Effective policy |
| --- | --- | --- | --- | --- |
| `parent` | created on object/prototype and inherited by parent-chain lookup | may be copied from mixin own slots, but then replaced | declared `IM LIEK` parent wins after mixin application | force `child'Z parent` to the declared parent object at construction |
| `omgwtf` | inherited via parent-chain lookup like any slot/method behavior | copied when present as own mixin slot/method | child own definition > copied mixin > inherited parent > default throw | missing-slot lookup invokes effective `omgwtf`; synthesized value is memoized into missing slot |
| `izmakin` | inherited via parent-chain slot lookup | copied when present as own mixin slot/method | child own definition > copied mixin > inherited parent > default `NOOB` | run callable effective `izmakin` after prototype build and before constructor return |

## N24 Policy Table: Mixin Source Set

| Source member on mixin object | Copied to target? | Policy |
| --- | --- | --- |
| Own slot | yes | copied statically at mixin time |
| Own method | yes | copied statically at mixin time |
| Inherited slot from mixin parent | no | not part of mixin source-set |
| Inherited method from mixin parent | no | not part of mixin source-set |

## Immediate Next Steps

1. Completed: added `N54` regression (`orly-mebbe-truthy-cast-src`).
2. Completed: adjudicated and documented `N44` + `N51` with explicit parser/runtime regressions.
3. Completed: authored `IT_UPDATE_MATRIX.md` and adjudicated `N60`.
4. Carry out-of-tranche early result: `N62` now has regression coverage (`gimmeh-implicit-target-declare-src`) pinning implicit target declaration behavior.
5. Re-run tranche scripts after these pass-2 additions:
   - `./scripts/analyze_corpus_gaps.sh`
   - `./scripts/eval_tier2_corpus.sh`
   - `./scripts/test_external_evidence.sh`
6. Completed (2026-03-06): strict cast-target parser gate and runtime cast-domain cleanup for `N63`/`N64`, with new parse-negative regressions (`MAEK ... A BUKKIT`, `IS NOW A BUKKIT`).
7. Completed (2026-03-06): equality identity-mode regression added for `N65` (same-reference vs same-shape object/function values).
8. Completed (2026-03-06): `omgwtf` stateful memoization precedence and same-slot re-entry policy pinned with targeted runtime regressions.
9. Completed (2026-03-06): strict-case audit removed residual case-insensitive keyword/type/literal/comment handling extensions and added regressions for lowercase lookalike behavior.
10. Completed (2026-03-06): `izmakin` ordering/reentrancy and method-call argument expression policy (`N19`, `N42`) pinned with dedicated runtime regressions.
11. Completed (2026-03-06): quaternary-seed pass adjudicated/pinned `N70`-`N78` behavior for reserved-name collisions, truthiness/numeric policy edges, RHS sequencing, forward references, duplicate params, and nested function-definition strictness.

## Fourth-Tier Integration Note

- Fourth-tier sweep is integrated into the master numbered backlog.
- Net-new additions were assigned `N70`-`N85` and explicitly placed in the quaternary (low-priority) tranche.
- Overlap-heavy fourth-tier items were mapped to existing concerns and not renumbered as duplicates.

## Pass-2 Script Snapshot

Latest rerun (2026-03-05 local snapshot generation time):

- Tier2 totals unchanged: files `223`, likely programs `184`.
- Tier2 likely outcomes unchanged: parse-error `167`, ok `9`, lex-error `7`, runtime-error `1`.
- Strict in-scope 1.3 unchanged: parse-ok `10`, eval-ok `9`, parse-error `3`, runtime-error `1`.
- External evidence observed-status unchanged: ok `1`, parse-error `301`.

# Tranche 1 Adjudication (Restart Pass 2)

Date: 2026-03-06
Source list:
- `NEXT-BOTTOM-UP-SPEC-CONCERNS-2026-03-05.md`
- `third-tier-of-40-issues.md`

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
| `N44` | needs-change | Document exact preprocessing order as executable policy + add parser/lexer tests for ordering-sensitive cases. |
| `N51` | needs-change | Keep longest-match keyword tokenization policy; add explicit regressions for phrase collisions and punctuation suffix tokens. |
| `N53` | adjudicated | `O RLY?` binds to current `IT`; statement delimiter behavior remains expression-driven (`stmt-if` uses `IT` directly). |
| `N54` | adjudicated | `MEBBE` uses TROOF-cast truthiness semantics; pinned by regression `orly-mebbe-truthy-cast-src`. |
| `N56` | adjudicated | `WTF?` binds to current `IT`; parser encodes `stmt-switch` with subject `(expr-ident \"IT\")`. |
| `N60` | needs-change | Create closed list of `IT`-updating forms and verify no accidental updates from non-expression statements. |
| `N61` | adjudicated | `VISIBLE` remains statement-special variadic with delimiter closure and `!` suffix newline suppression. |

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
2. Add explicit regressions for `N51` (longest-match collisions) and `N44` (ordering-sensitive preprocessing).
3. Write and check in an `IT` mutation matrix for `N60`.
4. Carry out-of-tranche early result: `N62` now has regression coverage (`gimmeh-implicit-target-declare-src`) pinning implicit target declaration behavior.
5. Re-run tranche scripts after these pass-2 additions:
   - `./scripts/analyze_corpus_gaps.sh`
   - `./scripts/eval_tier2_corpus.sh`
   - `./scripts/test_external_evidence.sh`

## Pass-2 Script Snapshot

Latest rerun (2026-03-05 local snapshot generation time):

- Tier2 totals unchanged: files `223`, likely programs `184`.
- Tier2 likely outcomes unchanged: parse-error `167`, ok `9`, lex-error `7`, runtime-error `1`.
- Strict in-scope 1.3 unchanged: parse-ok `10`, eval-ok `9`, parse-error `3`, runtime-error `1`.
- External evidence observed-status unchanged: ok `1`, parse-error `301`.

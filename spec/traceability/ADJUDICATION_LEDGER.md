# Tranche 1 Adjudication (Restart Pass 2)

Date: 2026-03-06
Source list:
- `archive/legacy-inputs/NEXT-BOTTOM-UP-SPEC-CONCERNS-2026-03-05.md`
- `archive/legacy-inputs/third-tier-of-40-issues.md`
- `archive/legacy-inputs/fourth-tier-of-40-issues.md`

Policy: `spec/traceability/ADJUDICATION_POLICY.md`

Pass-2 tranche-1 targets:
- Carry-forward: `N02`, `N10`-`N15`, `N20`-`N24`, `N27`, `N34`
- Added from third-tier integration: `N44`, `N51`, `N53`, `N54`, `N56`, `N60`, `N61`

## Carry-Forward Results

| ID    | Status      | Summary                                                                                                                                                      |
|-------|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `N02` | adjudicated | Distinct AST/runtime call paths for `I IZ` vs `<object> IZ`.                                                                                                 |
| `N10` | adjudicated | Object-function lookup clauses interpreted as specific override to broad scope prose.                                                                        |
| `N11` | adjudicated | Ordinary functions do not capture lexical outer locals; method/slot-call path is object-aware.                                                               |
| `N12` | adjudicated | `IT` local in ordinary scopes; method-context bare `IT` is activation-local and bypasses receiver-slot lookup. Implemented/test-pinned and closed under `C1/C2/C3`. |
| `N13` | adjudicated | `O HAI IM` body uses slot-first then global lookup (`object-block-slot-first-over-global-src`).                                                              |
| `N14` | adjudicated | Function and variable declarations share one namespace with duplicate declaration rejection.                                                                 |
| `N15` | adjudicated | Slot-call receiver projection controls callable name lookup scope.                                                                                           |
| `N20` | adjudicated | `omgwtf` missing-slot path memoizes synthesized value to the missing slot, and hook invocation is strict zero-arity under spec silence on parameter passing. |
| `N21` | adjudicated | Parent-chain traversal is cycle-safe across lookup/assignment/method paths.                                                                                  |
| `N22` | adjudicated | Copy-on-write assignment for inherited slots; ancestor slot is not mutated by child assignment.                                                              |
| `N23` | adjudicated | Special-slot policy table fixed and tested (`parent`, `omgwtf`, `izmakin`).                                                                                  |
| `N24` | adjudicated | Mixin source-set is donor effective-visible slots/methods (including inherited-visible members), copied in reverse mixin declaration order.              |
| `N27` | adjudicated | `GTFO` uses nearest valid control target semantics.                                                                                                          |
| `N34` | adjudicated | Variadic implicit closure runs over logical statements after formatting preprocess.                                                                          |

## Pass-2 Additions Started

| ID    | Status                    | Decision / Action                                                                                                                                                                                                                                                                                                                                                                     |
|-------|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `N44` | adjudicated               | Deterministic preprocessing order is fixed and documented (`PREPROCESSING_AND_KEYWORD_POLICY.md`) with ordering-sensitive regressions (`inline-block-comment-tldr-handoff`, `preprocess-order-runtime-src`).                                                                                                                                                                          |
| `N51` | adjudicated               | Canonical longest-match keyword policy is fixed for punctuated and phrase tokens (`spaced-orly-question`, `spaced-wtf-question`, `split-im-outta-phrase`).                                                                                                                                                                                                                            |
| `N53` | adjudicated               | `O RLY?` binds to current `IT`; statement delimiter behavior remains expression-driven (`stmt-if` uses `IT` directly).                                                                                                                                                                                                                                                                |
| `N54` | adjudicated               | `MEBBE` uses TROOF-cast truthiness semantics; pinned by regression `orly-mebbe-truthy-cast-src`.                                                                                                                                                                                                                                                                                      |
| `N56` | adjudicated               | `WTF?` binds to current `IT`; parser encodes `stmt-switch` with subject `(expr-ident \"IT\")`.                                                                                                                                                                                                                                                                                        |
| `N60` | adjudicated               | IT update policy is narrowed to bare expression statements only; assignment-family and non-expression statements are non-mutating unless explicitly specified by text (`IT_UPDATE_MATRIX.md`, `it-update-matrix-src`, `visible-updates-it-src`).                                                                                                                                      |
| `N61` | adjudicated               | `VISIBLE` remains statement-special variadic with delimiter closure and `!` suffix newline suppression; implicit `MKAY` omission is rejected before `!` (explicit `MKAY` required).                                                                                                                                                                                                   |
| `N43` | adjudicated               | Keyword/literal/type recognition is strict-case in direct syntax positions; lowercase lookalikes remain identifiers. Direct keyword-shaped identifiers are rejected at binding sites, while `SRS` remains the dynamic escape hatch where identifier text is computed and then validated at identifier-expected sites (`reserved-keyword-mkay-name`, `reserved-keyword-mkay-arg`, `srs-keyword-name-in-function-arg-src`, `srs-keyword-slot-name-src`, `srs-keyword-function-name-src`, `srs-keyword-method-name-src`, `srs-keyword-object-name-src`, `srs-keyword-receiver-name-src`). Parameter binders remain direct-only (`YR <ident-token>`), so `YR SRS ...` is parse-rejected (`srs-parameter-binder-negative`). |
| `N42` | adjudicated               | Method-call argument positions use expression semantics for coherence with call-expression section; parser/runtime tests now pin expression-argument method calls.                                                                                                                                                                                                                    |
| `N63` | adjudicated               | TYPE-words are dual-role by context: expression-position words remain TYPE literals; declaration `ITZ A <...>` defaults are restricted to built-in types (`TROOF|YARN|NUMBR|NUMBAR|NOOB|BUKKIT`); prototyping remains `ITZ LIEK A <parent>` (plain) and `ITZ A <parent> SMOOSH ...` (mixin).                                                                                          |
| `N64` | adjudicated               | Parser now enforces cast-target domain for both `MAEK <expr> [A] <type>` and `<lvalue> IS NOW A <type>` forms (`TROOF|YARN|NUMBR|NUMBAR|NOOB` only).                                                                                                                                                                                                                                  |
| `N65` | adjudicated               | Equality remains numeric-mode only for numeric pairs; non-numeric values use non-coercing host equality, with identity behavior pinned for BUKKIT/function values.                                                                                                                                                                                                                    |
| `N19` | adjudicated               | `izmakin` ordering is pinned to post-prototype/mixin parent-restored state; reentrant prototype creation from `izmakin` is allowed and tested per-prototype execution.                                                                                                                                                                                                                |
| `N81` | adjudicated               | Mixin copy depth for mutable slot values is call-by-sharing (shallow object reference copy), pinned by `mixin-static-snapshot-mutable-alias-src`.                                                                                                                                                                                                                                     |
| `N82` | adjudicated               | Mutable-value aliasing policy is consistent across mixin copy and ordinary assignment paths: shared BUKKIT references remain shared unless explicitly re-bound.                                                                                                                                                                                                                       |
| `N79` | adjudicated               | `ME HAS A` writes receiver-owned slots: inherited names are shadowed on receiver, not mutated in ancestor (`me-has-a-shadows-inherited-slot-src`).                                                                                                                                                                                                                                    |
| `N80` | adjudicated               | `ME'Z slot R expr` follows ordinary assignment sequencing: RHS evaluates before slot write and reads prior slot value (`me-slot-assign-rhs-sees-prior-value-src`).                                                                                                                                                                                                                    |
| `N83` | adjudicated               | Non-BUKKIT `parent` values terminate inheritance traversal deterministically for both slot and method lookup (`parent-slot-nonobject-terminates-chain-src`, `parent-method-nonobject-terminates-chain-src`).                                                                                                                                                                          |
| `N84` | adjudicated               | Method call `<object> IZ <slot> MKAY` shares slot-access miss semantics: full parent-chain lookup first; if unresolved, invoke `omgwtf` once on the original receiver; cache synthesized slot value for later calls (`method-call-miss-omgwtf-after-full-chain-src`, `method-call-miss-omgwtf-on-original-receiver-src`).                                                                |
| `N85` | adjudicated               | `izmakin` failures surface during construction before declaration completion (`izmakin-failure-surfaced-before-binding-src`); binding atomicity follows declaration evaluation order (`compile-stmt-declare`: evaluate RHS then define binding).                                                                                                                                      |
| `N01` | adjudicated               | Parser preserves distinct definition-node split: `HOW IZ I` -> `stmt-function-def`, `HOW IZ <receiver> <name>` -> `stmt-method-def` (`ast-function-vs-method-def-shape-src`).                                                                                                                                                                                                         |
| `N03` | adjudicated               | Declaration, assignment, cast-assignment, and slot-set remain distinct statement constructors (`ast-stmt-node-split-src`).                                                                                                                                                                                                                                                            |
| `N04` | adjudicated               | `SRS` remains an explicit AST form in identifier-sensitive declaration/slot/call-name sites (`ast-srs-sites-shape-src`).                                                                                                                                                                                                                                                              |
| `N05` | adjudicated               | `SMOOSH` expression and prototype-mixin `SMOOSH` parse to different AST forms (`expr-variadic` vs `expr-prototype`) (`ast-smoosh-disambiguation-src`).                                                                                                                                                                                                                                |
| `N06` | adjudicated               | Slot-operator prose/display contradiction is harmonized by accepting both `-` and `'Z` spellings as equivalent slot access syntax, including dynamic `SRS` paths.                                                                                                                                                                                                                           |
| `N07` | adjudicated               | Multi-role `I` policy pinned: `I` remains reserved syntax token in declaration/call forms, and object-body `HOW IZ I`/`I HAS A` semantics are preserved (`i-token-role-shape-src`, parse negative `reserved-keyword-i-name`).                                                                                                                                                         |
| `N08` | adjudicated               | Special-name policy pinned: `ME` remains reserved at binding sites; `IT` is pre-bound (redeclaration rejected by same-scope duplicate gate); `parent/omgwtf/izmakin` are not globally reserved identifiers but retain slot-level special behavior (`special-names-global-vs-slot-policy-src`, `it-redeclare-runtime-error-src`).                                                      |
| `N09` | adjudicated               | Pre-parse boundary normalization remains deterministic and compositional across comma, continuation, line/block comments, and string shielding (`preprocess-confluence-n09-src`, plus existing preprocess-order regressions).                                                                                                                                                         |
| `N16` | adjudicated               | Function values extracted from slots are callable, but receiver-projected lookup applies only to slot-call invocation; direct `I IZ` on extracted value uses global call namespace (`extracted-slot-function-direct-call-namespace-src`).                                                                                                                                             |
| `N17` | adjudicated               | Stale “BUKKIT reserved” prose is treated as superseded by the normative object section; strict 1.3 fully supports BUKKIT declarations/slots/inheritance (for example `bukkit-slot-src`, `inherited-object-src`).                                                                                                                                                                      |
| `N18` | adjudicated               | `LIEK A` follows prototype-chain semantics with inherited lookup + copy-on-write assignment, not eager deep copy (`inherited-parent-mutation-visibility-src`, `inherited-method-slot-independence-src`, `parent-slot-reparenting-src`).                                                                                                                                               |
| `N25` | adjudicated               | Slot-key domain is surface-syntax constrained: direct slot syntax admits identifier or `SRS <expr>` only; dynamic `SRS` slot keys are typed (`NUMBR` or `YARN`) and do not coerce (`0` and `"0"` are distinct keys) (`bukkit-srs-numeric-slot-src`, `bukkit-slot-keys-typed-src`, parse negative `slot-set-direct-numeric-target`).                                                                                             |
| `N26` | adjudicated               | Object self-reference by object name inside `O HAI IM` body is not available during construction; binding is installed after body execution (`object-self-reference-during-construction-src`).                                                                                                                                                                                        |
| `N28` | adjudicated               | Loop label matching is enforced at runtime between `IM IN YR` and `IM OUTTA YR`; mismatch is runtime error and repeated names are allowed under structural pairing (`loop-label-mismatch`, `duplicate-loop-labels-n57-src`).                                                                                                                                                          |
| `N29` | adjudicated               | Loop condition is checked pre-body and updater runs post-body; updater variable names must resolve to already-declared bindings before loop entry (no implicit loop counter declaration/initialization) (`loop-order-matrix-src`, `loop-counter-requires-declared-updater`).                                                                                                                                              |
| `N30` | adjudicated               | Loop updater callable contract is unary and evaluated per iteration post-body; arity violations are runtime errors (`loop-unary-updater-src`, `loop-unary-updater-side-effects-src`, `loop-unary-updater-arity-error-src`).                                                                                                                                                           |
| `N31` | adjudicated               | `WTF?` duplicate literal uniqueness is enforced at parse time using numeric-mode equality for numeric literals (`duplicate-wtf-case-literal`, `duplicate-wtf-case-literal-numeric-mode`).                                                                                                                                                                                             |
| `N32` | adjudicated               | Runtime errors in matched `OMG` bodies halt execution and do not continue to `OMGWTF`/subsequent statements (`switch-runtime-error-propagates-src`).                                                                                                                                                                                                                                  |
| `N33` | adjudicated               | Empty `OMG` blocks are valid and participate in fallthrough semantics (`switch-empty-omg-fallthrough-src`).                                                                                                                                                                                                                                                                           |
| `N35` | adjudicated               | GC/deallocation prose is treated as non-normative runtime guidance; semantic behavior is pinned at binding/reference level (`r-noob-retains-binding-src`, `r-noob-does-not-invalidate-other-reference-src`).                                                                                                                                                                          |
| `N36` | adjudicated               | Non-numeric equality for complex values is identity/reference-sensitive under host equality with numeric-mode exception for numbers (`equality-complex-values-identity-src`).                                                                                                                                                                                                         |
| `N37` | adjudicated               | `TYPE` and `NOOB` remain distinct values/types under equality and cast behavior (`type-noob-distinction-stability-src`, `type-literal-domain-casts-src`).                                                                                                                                                                                                                             |
| `N39` | adjudicated               | Higher-order callability is shape-limited: function values are storable/extractable and callable via identifier/slot call forms, but no arbitrary expression-call form is introduced (`function-storage-src`, `extracted-slot-function-direct-call-namespace-src`).                                                                                                                   |
| `N40` | adjudicated               | Expression evaluation order is pinned as deterministic left-to-right: function/method call arguments are evaluated before body entry, and binary-operator operands are eager left-to-right (`function-call-arg-eval-order-src`, `method-call-arg-eval-order-src`, `logic-binary-left-to-right-src`, `logic-binary-eager-rhs-src`). |
| `N41` | adjudicated               | Dynamic loop labels via `SRS` are supported; label matching/errors still apply with dynamic names (`loop-dynamic-label-src`, `loop-dynamic-label-mismatch-src`).                                                                                                                                                                                                                      |
| `N66` | adjudicated               | Primitive-ops clause is read as non-mutating value semantics with canonical singleton sharpness only for `WIN`/`FAIL`/`NOOB`; numeric/YARN representation identity remains implementation-level and non-observable under strict equality semantics (`primitive-ops-immutable-src`, `equality-complex-values-identity-src`).                                                                                                                                       |
| `N69` | adjudicated               | Receiver late-binding invariant holds for mixin-copied function slots: slot-call dispatch projects receiver scope at call time, while extracted direct calls use global namespace (`mixin-copied-function-receiver-late-binding-src`).                                                                                                                                                |
| `N38` | adjudicated               | Optional article `A` remains grammar-site specific: declaration and `MAEK` may omit `A`, and if an article is present there it must be `A` (not `AN`); slot declaration and cast-assignment require strict forms; `ITZ <TYPE>` vs `ITZ A <TYPE>` remain distinct semantics (`optional-article-scope-n38-src`, parse negatives around declaration `AN`, `slot-set-without-article`, `cast-assignment-missing-a`).                                     |
| `N45` | adjudicated               | Continuation marker normalization supports both `...` and `…`; trailing horizontal whitespace before newline is accepted while non-whitespace trailing content is rejected (`continuation-trailing-space-tab-n45-src`, parse negatives `continuation-then-comma`, `continuation-with-trailing-comment`).                                                                              |
| `N46` | adjudicated               | Inline block-comment permissiveness and `TLDR` handoff are pinned, including immediate comma/newline handoff and strict delimiter enforcement (`tldr-handoff-space-comma-n46-src`, `inline-block-comment-tldr-handoff`, `block-comment-tldr-trailing-statement-without-comma`).                                                                                                       |
| `N47` | adjudicated               | Numeric lexical edge policy is strict: malformed forms (`.5`, `-.5`, `2.`, `-0.`, multi-dot) are rejected in direct numeric literal positions (`malformed-number-leading-dot`, `malformed-number-minus-leading-dot`, `malformed-number-trailing-dot`, `malformed-number-negative-trailing-dot`, `malformed-number-multi-dot`).                                                        |
| `N48` | adjudicated               | YARN-to-number casting uses strict grammar for sign/dot placement and multiplicity; malformed numeric YARNs raise runtime cast errors (`cast-invalid-yarn-dotdot-n48-src`, `cast-invalid-yarn-double-minus-n48-src`, `cast-invalid-yarn-leading-dot-n48-src`).                                                                                                                        |
| `N49` | adjudicated               | Malformed escape failure semantics are strict for invalid/out-of-range/surrogate code points and invalid normative names; `:[<name>]` requires uppercase names (lowercase/mixed-case rejected) and resolves against the spec-cited Unicode 4.1 table (newer names rejected) (`invalid-unicode-codepoint`, `invalid-unicode-surrogate-codepoint`, `lowercase-unicode-normative-name`, `mixed-case-unicode-normative-name`, `string-normative-escape-outside-41-src`).                                            |
| `N50` | adjudicated               | Interpolation scanner precedence is pinned: `::` escapes placeholder start before `:{...}` interpolation capture (`format-string-escaped-placeholder-src`, `escaped-interpolation-wtf-string-case`).                                                                                                                                                                                  |
| `N52` | adjudicated               | Assignment grammar is normalized to lvalue forms only; non-lvalue targets are parse errors and canonical variable/slot lvalue forms are accepted (`assignment-nonvariable-lhs`, `assignment-call-lhs`, `cast-assignment-nonvariable-lhs`, canonical assignment positives).                                                                                                            |
| `N55` | adjudicated               | Orphan conditional branches are rejected: `MEBBE`/`NO WAI` require valid `O RLY?` structure with `YA RLY` ordering (`orphan-mebbe-without-ya-rly`, `orphan-no-wai-without-orly`, `orly-mebbe-after-no-wai`).                                                                                                                                                                          |
| `N57` | adjudicated               | Loop labels are case-sensitive; duplicate names are permitted and matched structurally per loop statement pair (`loop-label-case-mismatch`, `duplicate-loop-labels-n57-src`).                                                                                                                                                                                                         |
| `N58` | adjudicated               | Definition-site verb synonyms are accepted: `HOW IZ` and `HOW DUZ` both parse for ordinary and receiver/object-block function definitions; call syntax remains `IZ`-only (`how-duz-i-form`, `how-duz-i-runtime-src`, `how-duz-receiver-runtime-src`, `how-duz-objectblock-runtime-src`, `how-duz-callform`).                                                                                                                   |
| `N59` | adjudicated               | “SRS BIZNUS” dynamic-name prose is concretized as explicit `expr-srs` handling across declaration/slot/function/method/receiver-name positions (`ast-srs-sites-shape-src`, dynamic `SRS` call/slot tests).                                                                                                                                                                            |
| `N62` | adjudicated               | `GIMMEH` target must already be a declared variable designator; undeclared targets are runtime errors and non-variable targets are parse errors (`gimmeh-undeclared-target-runtime-error-src`, `gimmeh-expression-target`).                                                                                                                                                           |
| `N67` | adjudicated               | `ME` is syntactically accepted but runtime-resolved only in method context; outside receiver context it raises runtime unknown-identifier error (`me-outside-method-src`, `me-does-not-leak-into-nested-function-from-method-src`).                                                                                                                                                   |
| `N68` | adjudicated               | `HOW IZ <receiver> <slot>` receiver checks occur at execution/definition time: parse accepts receiver expression shapes, then runtime enforces receiver existence and BUKKIT type (`method-def-receiver-missing-n68-src`, `method-def-receiver-nonbukkit-n68-src`).                                                                                                                   |
| `N20` | adjudicated (extended)    | `omgwtf` missing-slot policy is pinned for stateful hooks: return-value memoization is authoritative for the resolved slot name even if intermediate same-slot mutation occurs inside `omgwtf`; invocation arity is fixed at zero because the spec does not define hook arguments, and adding implicit missing-name arguments would introduce extra machinery not textually licensed. |
| `N13` | adjudicated (edge policy) | `omgwtf` same-slot recursive re-entry is trapped as deterministic runtime error to avoid silent divergence in spec-underdetermined recursion scenarios.                                                                                                                                                                                                                               |
| `N70` | adjudicated               | Directly written reserved literal/special names are rejected at user binding sites (declarations, function/method/object names, parameter names) via parser/runtime binder gates; this coexists with `N43`/`N88` dynamic-name policy (`SRS` may synthesize keyword-shaped names where grammar admits dynamic identifiers), while parameter binders remain direct-only. Added regressions for `WIN`/`ME` declarations and `FAIL`/`NOOB`/`TROOF` def-name/param/object collisions.                                                                                                                    |
| `N71` | adjudicated               | `HAI` header version must be a numeric token, and strict acceptance remains exactly `1.3`. Non-numeric version tokens are parse errors; numeric non-`1.3` versions are unsupported-version errors (`missing-version`, `version-token-must-be-number`, `version-string-literal-negative`, `unsupported-v12`, `unsupported-v14`).                                                                                                                                                                                                   |
| `N72` | adjudicated               | BUKKIT values are truthy (no empty-container false special case), now explicitly pinned (`empty-bukkit-truthy-src`).                                                                                                                                                                                                                                                                  |
| `N73` | adjudicated               | Numeric portability follows host runtime: division by zero surfaces runtime error, and large NUMBR arithmetic remains exact (`quoshunt-division-by-zero-runtime-error-src`, `numbr-bignum-arithmetic-src`).                                                                                                                                                                           |
| `N74` | adjudicated               | IT-sensitive statement behavior follows `N60`: only bare expression statements update `IT`; wrappers/assignment-family statements preserve current `IT` (`it-update-matrix-src`, `visible-updates-it-src`).                                                                                                                                                                            |
| `N75` | adjudicated               | RHS sequencing is pinned: declaration RHS cannot see the binding being created, assignment RHS reads prior binding value (`declaration-rhs-does-not-see-binding-being-declared-src`, `assignment-rhs-sees-prior-binding-value-src`).                                                                                                                                               |
| `N76` | adjudicated               | No forward-reference prebinding for functions; call-before-definition is runtime error (`function-forward-reference-runtime-error-src`).                                                                                                                                                                                                                                              |
| `N77` | adjudicated               | Duplicate function parameter names are rejected by same-scope binding rules at call frame construction (`function-duplicate-params-runtime-error-src`).                                                                                                                                                                                                                               |
| `N78` | adjudicated               | Nested function definitions are rejected under strict 1.3 parser policy (`nested HOW IZ I definitions are not allowed in strict 1.3` parse negatives).                                                                                                                                                                                                                                |
| `N86` | adjudicated               | Variadic optional-`AN` parsing is generalized to all argument positions for `SMOOSH`/`ALL OF`/`ANY OF` (not limited to raw-atom arguments), while leading `AN` remains invalid (`variadic-optional-an-general-expr`, `variadic-leading-an-negative`).                                                                                                                                |
| `N87` | adjudicated               | Implicit `MKAY` omission is statement-boundary scoped: omission is rejected before `!` and before `AN YR` continuation inside the same statement (`implicit-mkay-before-bang-negative`, `smoosh-explicit-mkay-before-bang-src`).                                                                                                                                                    |
| `N88` | adjudicated               | `SRS` at identifier-binding and lookup sites must produce identifier-shaped names at runtime; non-identifier results are runtime errors. Nested `SRS` is repeated identifier indirection (not source reparsing) (`srs-numeric-target-src`, `srs-nested-indirection-src`, `srs-generated-source-not-reparsed-src`).                                                                                                                                                                                                                             |
| `N90` | adjudicated               | `<object> HAS A <slot>` without `ITZ` is accepted as declaration shorthand and initializes the slot to `NOOB` (canonical explicit form remains `... ITZ <expr>`). This applies generally (including `ME`) rather than as a receiver-only exception (`slot-set-no-itz-shorthand-src`, `me-slot-no-itz-shorthand-src`, parse acceptance `slot-set-no-itz-shorthand`).                                                                                                                                                              |
| `N91` | adjudicated               | `OBTW` block comments are statement-boundary sensitive: recognized only at logical command start (line start or comma boundary), rejected mid-command (`obtw-mid-command-negative`, `block-comment-comma-boundary-src`).                                                                                                                                                             |
| `N92` | adjudicated               | Interpolation placeholder `:{...}` remains identifier-only (no whitespace/expression trimming), pinned with strict runtime errors (`format-string-whitespace-placeholder-src`).                                                                                                                                                                                                         |
| `N93` | adjudicated               | Unicode verbose-name escapes are frozen to the spec-cited Unicode 4.1.0 normative table with uppercase-name requirement (`string-normative-escape-src`, `string-normative-escape-outside-41-src`, `lowercase-unicode-normative-name`, `mixed-case-unicode-normative-name`).                                                                                                                                  |
| `N94` | adjudicated               | NUMBAR-to-YARN rendering policy is truncation to at most two decimals, no rounding, no forced zero padding (`numbar-visible-format-src`, `numbar-no-forced-padding-src`).                                                                                                                                                                                                             |
| `N95` | adjudicated               | Variadic logical operators short-circuit left-to-right (`ANY OF` stop on first `WIN`, `ALL OF` stop on first `FAIL`) with side-effect/error order pinned, and `SMOOSH` arity remains one-or-more (one-argument identity accepted; zero-argument form parse-rejected) (`logic-variadic-any-short-circuit-src`, `logic-variadic-any-short-circuit-avoids-error-src`, `logic-variadic-all-short-circuit-rhs-src`, `smoosh-one-arg-src`, parse negative `smoosh-zero-arg-negative`).                                                                                |
| `N96` | adjudicated               | Typed BUKKIT key-domain behavior is pinned: direct `<identifier>` slot access is YARN-keyed; dynamic `SRS` slot access uses evaluated `NUMBR`/`YARN` key values without identifier coercion (`bukkit-slot-keys-typed-src`).                                                                                                                                                         |
| `N97` | adjudicated               | `KTHXBYE` is a hard program terminator in strict mode: no same-line `BTW` tail is permitted, and no trailing non-whitespace lines are permitted after close (`kthxbye-inline-btw`, `one-line-minimal-inline-btw`, `trailing-btw-after-close`, `trailing-obtw-after-close`, `one-line-extra-after-close`).                                                                                                                                                        |
| `N98` | adjudicated               | Identifier-character domain is pinned to ASCII letters/digits/underscore with leading ASCII letter (`^[A-Za-z][A-Za-z0-9_]*$`): mixed-case and underscores are allowed; non-ASCII letters are rejected in strict mode as underdetermined by spec text (`valid-ident-mixed-case-underscore`, `invalid-ident-unicode-letter`, `invalid-ident-leading-underscore`, `invalid-ident-with-dash`, `invalid-ident-symbol-only`).                                                                                                                                                        |

## N43/N88 Binder-Site Rationale (No Dynamic Parameter Binders)

The project rejects `SRS`-generated parameter names in function/method definitions even though `SRS` is accepted at many dynamic reference/name sites.

Reason: parameter names are binders, not ordinary references. If parameter names were recomputed at call time, parameter binding would depend on ambient mutable state rather than on the fixed surface form of the function definition.

Consequences of allowing dynamic parameter binders:

1. Function interfaces would become unstable across calls.
2. Duplicate-parameter legality would become runtime-dependent rather than a stable property of the definition.
3. Recursive and mutually recursive calls could bind the same formal positions under different names as ambient state changes.
4. Call frames would need dynamically computed binder sets instead of the ordinary fixed binder layout defined by the function declaration.

Project wording pin:

“Stack frames do not become impossible, but they cease to have a fixed binder layout determined by the function definition; instead the frame’s binding set would have to be computed dynamically at each call.”

This behavior is pinned by parser negatives (`srs-parameter-binder-negative`, `function-dynamic-arg-name`, `method-dynamic-arg-name`) together with runtime duplicate-parameter guard behavior (`function-duplicate-params-runtime-error-src`).

## N90 Rationale (Generic `<object> HAS A <slot>` No-`ITZ` Shorthand)

`N90` intentionally adopts the general shorthand rule:

`<object> HAS A <slot>`

is accepted as declaration shorthand for:

`<object> HAS A <slot> ITZ NOOB`

Reasoning:

1. A `ME`-only shorthand carve-out requires extra special-case machinery that the spec does not introduce. `ME` is described as the calling-object identifier, not as a distinct grammar class that licenses unique declaration syntax.
2. The generic shorthand reading is structurally parallel to variable declaration shorthand (`I HAS A <var>` defaulting to `NOOB`), so it preserves the smallest coherent rule set across declaration forms.
3. Restricting shorthand to `ME` adds policy noise and makes the language less compositional with no textual requirement for that asymmetry.

Project ruling:

- If no `ITZ` initializer is present in `<object> HAS A <slot>`, strict mode defaults the new slot value to `NOOB` for any receiver object expression, not only `ME`.
- Explicit `... ITZ <expr>` remains canonical and equivalent where provided.

This behavior is pinned by `slot-set-no-itz-shorthand`, `slot-set-no-itz-shorthand-src`, and `me-slot-no-itz-shorthand-src`.

See also: `spec/traceability/archive/reports/N90_GENERIC_SLOT_SHORTHAND_RATIONALE_2026-03-12.md`.

## N71 Rationale (`HAI` Version Number Is Numeric Syntax)

Spec text basis (`spec/upstream/lolcode-spec-v1.3.md:89`):

- Programs must open with `HAI`.
- `HAI` should be followed by the current language version *number* (`1.3` in this spec).
- The spec notes no canonical cross-implementation policy for how version numbers are treated.

Strict holding:

1. The token immediately after `HAI` is header syntax, not an expression position.
2. Therefore it must lex/parse as a numeric token.
3. In this implementation, strict acceptance is only `1.3`; other numeric versions are rejected as unsupported.

Why this is the narrow reading:

- Accepting identifier/string tokens after `HAI` would contradict the explicit “version number” requirement and invent extra coercion behavior not stated by the text.
- Treating header version as runtime-castable data (`YARN`/`MAEK` style) would import expression semantics into a grammar header position where the spec gives a direct syntactic directive.

Pinned regressions:

- `missing-version`
- `version-token-must-be-number`
- `version-string-literal-negative`
- `unsupported-v12`
- `unsupported-v14`

## N97 Rationale (`KTHXBYE` Hard-Close Boundary)

Spec text basis (`spec/upstream/lolcode-spec-v1.3.md:91`):

- “A LOLCODE file is closed by the keyword `KTHXBYE` which closes the `HAI` code-block.”

Strict holding:

1. `KTHXBYE` closes the program body itself.
2. Therefore no additional code/comment material is accepted after `KTHXBYE` on the same line or later lines.
3. After `KTHXBYE`, only trailing whitespace is accepted.

Why this is the narrow reading:

- A permissive “inline `BTW` after `KTHXBYE`” rule introduces an extra carve-out not stated in the file-close clause.
- Under strict exegesis, once the file/code-block is declared closed, accepting additional lexical material is expansionary and should be rejected unless the text explicitly reopens that boundary.

Pinned regressions:

- `kthxbye-inline-btw`
- `one-line-minimal-inline-btw`
- `trailing-btw-after-close`
- `trailing-obtw-after-close`
- `one-line-extra-after-close`

## N98 Rationale (Identifier Character Domain)

Spec text basis (`spec/upstream/lolcode-spec-v1.3.md:111`):

- Identifiers “must begin with a letter” and continue with letters, numbers, underscores.
- The same sentence is case-sensitive and contains mixed historical wording (“small or lowercase letters”), without a formal Unicode character-class definition.

Strict holding:

1. Direct identifier syntax uses ASCII letter classes:
   `^[A-Za-z][A-Za-z0-9_]*$`.
2. Mixed-case identifiers and underscores are valid.
3. Non-ASCII letters in direct identifier syntax are rejected in strict mode.

Why this is the narrow reading:

- The spec gives no explicit Unicode identifier category/version/normalization model for identifiers (its Unicode 4.1 citation applies to `:[<char name>]` escapes, not identifier lexing).
- Accepting broad Unicode categories without a pinned profile introduces implementation-dependent drift; strict mode therefore selects the minimal deterministic character domain.

Pinned regressions:

- `valid-ident-mixed-case-underscore`
- `invalid-ident-unicode-letter`
- `invalid-ident-leading-underscore`
- `invalid-ident-with-dash`
- `invalid-ident-symbol-only`

## N66 Clarification (Primitive “New Objects” vs Canonical Singletons)

Spec text basis (`spec/upstream/lolcode-spec-v1.3.md:166`):

- Primitive types are immutable.
- Built-in operations return new objects.
- Explicit exceptions are `WIN`, `FAIL`, and `NOOB`, where references are canonicalized.

Project clarification:

1. The “new objects” clause is partly implementation-oriented language about immutable, non-mutating primitive operations.
2. It becomes semantically sharp only where the spec explicitly mandates canonical singleton instances (`WIN`/`FAIL`/`NOOB`).
3. For numbers and strings, the spec leaves representation/identity largely noncommittal.
4. Implementations are free not to exploit that latitude, as long as they do not expose semantics that require non-singleton or singleton identity for numeric/string values.

## N23 Policy Table: Special Slots

| Special slot | Prototype inheritance path                                       | Mixin-copy path                                       | Override precedence                                                     | Effective policy                                                                                                    |
|--------------|------------------------------------------------------------------|-------------------------------------------------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| `parent`     | created on object/prototype and inherited by parent-chain lookup | copied from mixin effective visible slots, then replaced | declared `IM LIEK` parent wins after mixin application                  | force `child'Z parent` to the declared parent object at construction                                                |
| `omgwtf`     | inherited via parent-chain lookup like any slot/method behavior  | copied from mixin effective visible slots               | child own definition > copied mixin > inherited parent > default throw  | missing-slot lookup invokes effective `omgwtf` with zero arguments; synthesized value is memoized into missing slot |
| `izmakin`    | inherited via parent-chain slot lookup                           | copied from mixin effective visible slots               | child own definition > copied mixin > inherited parent > default `NOOB` | run callable effective `izmakin` after prototype build and before constructor return                                |

## N24 Policy Table: Mixin Source Set

| Source member on mixin object      | Copied to target? | Policy                                                |
|------------------------------------|-------------------|-------------------------------------------------------|
| Own slot                           | yes               | copied statically at mixin time                       |
| Own method                         | yes               | copied statically at mixin time                       |
| Inherited slot from mixin parent   | yes               | copied from donor effective visible slot interface    |
| Inherited method from mixin parent | yes               | copied from donor effective visible slot interface    |

## Immediate Next Steps

1. Completed: added `N54` regression (`orly-mebbe-truthy-cast-src`).
2. Completed: adjudicated and documented `N44` + `N51` with explicit parser/runtime regressions.
3. Completed: authored `IT_UPDATE_MATRIX.md` and closed `N60` under `IT` contradiction adjudication.
4. Carry out-of-tranche early result: `N62` now has regression coverage (`gimmeh-undeclared-target-runtime-error-src`) pinning declaration-required input target behavior.
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

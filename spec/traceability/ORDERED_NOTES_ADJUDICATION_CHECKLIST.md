# Ordered Adjudication Checklist (Notes x Spec 1.3)

Source inputs (read in order):
- `CURRENT-SPEC-NOTES-BUGS-WORRIES.md`
- `spec/upstream/lolcode-spec-v1.3.md`

Companion mapping audit:
- `spec/traceability/spec-1.3-clause-mapping-audit.md`

Legend:
- `mapped`: clause has a matrix row in `spec-1.3-matrix.rktd`
- `unmapped`: clause currently appears in the unmapped normative list

## Phase 1: Formatting / Lex / Parse (in notes order)

- [x] `01` (notes 1-13) Comma soft-break + line continuation interaction; statement boundary semantics.
  Spec: lines 31, 33, 35. Matrix: `fmt.soft-break-comma`, `fmt.line-continuation-ellipsis`, `fmt.line-continuation-chain` (mapped).  
  Done: added explicit combined-case tests (`comma + ...`, `..., comma`, multi-line chain ending in comma) and lexer token-stream assertions in `tests/spec/parse-negative-test.rkt` + runtime execution checks in `tests/spec/runtime-core-test.rkt`.

- [x] `02` (notes 15-20) Empty-line after continuation, standalone ellipsis line, comment interaction with continuation markers.
  Spec: lines 37, 38, 40, 42. Matrix: `fmt.line-continuation-empty-line`, `fmt.line-continuation-standalone-ellipsis`, `comment.btw-terminates-at-newline`, `string.ignore-line-control-inside-yarn` (mapped).  
  Done: added/kept negative tests for forbidden empty line, positive tests for standalone `...` and `…`, plus comment-with-ellipsis positive/negative edge cases.

- [x] `03` (notes 22) One-line minimal program (`HAI 1.3, KTHXBYE`) and envelope closure.
  Spec: lines 89, 91. Matrix: `program.envelope-hai-kthxbye`, `program.kthxbye-closes-hai` (mapped).  
  Done: added single-line positive test (`HAI 1.3, KTHXBYE`) and malformed one-line negatives (missing close, extra tokens).

- [x] `04` (notes 65) Clarify `AS` in example text.
  Spec: appears in prose example, not grammar keyword. Matrix: n/a.  
  Done: added regression confirming strict parser rejects `MAEK ... AS ...` form and accepts `AS` as ordinary identifier (non-keyword).

## Phase 2: Scope / Names / Vars / Types / Ops (in notes order)

- [x] `05` (notes 24-34) “No global scope” text vs later object-function scope rules.
  Spec: line 105 (`unmapped`) vs line 672 (`mapped`).  
  Done: added matrix adjudication row for line 105 (`var.scope-adjudication-main-vs-object`) documenting lexical main/function scope plus explicit object-function override at line 672 for IT lookup.

- [x] `06` (notes 35-64) Function and variable same namespace; duplicate declaration behavior.
  Spec: line 145 (`unmapped`), declaration lines 117/205.  
  Done: `env-define!` now errors on same-frame redeclaration; function definitions use `env-define!` (not set-or-define). Added regressions for duplicate vars, duplicate functions, function/var namespace collision, and assignment-overwrites-function behavior.

- [x] `07` (notes 67-77) `R NOOB` and GC expectations.
  Spec: deallocation prose (not explicit runtime requirement beyond unbinding semantics). Matrix: no dedicated row.  
  Done: added matrix row `var.deallocation-r-noob`; documented host-GC responsibility and added runtime regressions that verify semantic binding/reference behavior only.

- [x] `08` (notes 78) Primitive immutability interpretation.
  Spec: type prose around primitive behavior. Matrix: partially implicit via cast/op rows.  
  Done: added dedicated matrix row `type.primitives-immutable` and regression showing arithmetic/SMOOSH produce new values while original bindings remain unchanged until explicit assignment.

- [ ] `09` (notes 80) Optional article `A` usage boundaries.
  Spec: line 189 (mapped), MAEK grammar line 362 (mapped).  
  Progress: tightened slot-creation grammar to require `HAS A/AN` and added parse-negative coverage rejecting bare `HAS`.
  To check: finish full grammar-site enumeration for all optional-article positions and add remaining negative tests.

- [ ] `10` (notes 82) Assignment to undeclared identifiers in core scope.
  Spec: line 205 (mapped) but explicit undeclared-assignment behavior is not clearly stated.  
  To check: adjudicate policy from spec examples; add explicit tests and matrix note.

- [ ] `11` (notes 84-101) BUKKIT “reserved” wording vs full bukkit section later.
  Spec: line 219 (`unmapped`) vs bukkit section lines 612+ (`unmapped/mapped mix`).  
  To check: add traceability clarification note: treat later bukkit section as authoritative for 1.3.

- [ ] `12` (notes 88-101) Struck-through TYPE cast sentence + NOOB/TROOF truthiness questions.
  Spec: line 219 (`unmapped`), line 223 (`mapped`), line 259 (`mapped`).  
  To check: confirm strict behavior for NOOB and TYPE literals; add tests for `MAEK TYPE A TROOF`, `MAEK NOOB A TROOF`.

- [ ] `13` (notes 103-108) NUMBR/NUMBAR lexical shape and truncation edge cases.
  Spec: lines 233, 235, 237 (mapped).  
  To check: add tests for `2.` reject, `-0.567` NUMBAR->NUMBR truncation behavior, and lexical strictness documentation.

- [ ] `14` (notes 109-112) Hex escape correctness.
  Spec: line 251 (mapped).  
  To check: add round-trip tests for representative code points (BMP + boundary invalid cases).

- [ ] `15` (notes 115-117) TYPE bare-word domain and cast behavior.
  Spec: line 259 (mapped).  
  To check: extend positive tests for all TYPE literals (`TROOF NOOB NUMBR NUMBAR YARN TYPE`) cast to TROOF/YARN.

- [ ] `16` (notes 119-126) Variadic closure with MKAY/EOL and nested variadics with comma/continuation.
  Spec: lines 269, 286 (line 269 currently `unmapped`, 286 mapped as `op.mkay-variadic-form`).  
  To check: add explicit parser+runtime tests for nested variadics, stack-like MKAY closure order, comma terminators, and continued lines.

- [ ] `17` (notes 127) Optional `AN` for binary operators.
  Spec: line 277 (mapped `op.an-optional-binary`).  
  To check: ensure full operator family covered in positive+negative tests.

- [ ] `18` (notes 129-141) Equality semantics and no implicit cast for non-numeric equality.
  Spec: comparison section around lines 326+ (currently not represented by dedicated matrix row).  
  To check: add dedicated matrix clause + tests (`BOTH SAEM "3" AN 3` == FAIL, NUMBR/NUMBAR numeric mode).

- [ ] `19` (notes 143-161) `MAEK` is local cast only; underlying variable unchanged.
  Spec: line 362 (mapped `cast.maek`).  
  To check: add explicit regression showing source binding type/value unaffected after `MAEK`.

- [ ] `20` (notes 161) Initialization type choice for literals (`I HAS A foo ITZ 2`).
  Spec: line 123 (`unmapped`).  
  To check: document implementation policy (literal determines value type directly); add explicit tests.

- [ ] `21` (notes 165-167) `VISIBLE` delimiter semantics vs continuation.
  Spec: line 383 (mapped), formatting lines 33/35 (mapped).  
  To check: add tests where `VISIBLE` spans continued lines and comma-separated command boundaries.

## Phase 3: IT / Control / Functions (in notes order)

- [ ] `22` (notes 169-177) Reconcile “IT local scope” vs object-function “IT global lookup”.
  Spec: line 407 (`unmapped`), line 672 (`mapped`).  
  To check: add matrix row for line 407; add tests for local IT in main/function and global IT lookup in object-function context.

- [ ] `23` (notes 179) Assignment operator identification and strict grammar.
  Spec: line 411 (`unmapped`) + line 205 (`mapped`).  
  To check: add parser-focused tests documenting canonical assignment forms.

- [ ] `24` (notes 181-190) `O RLY?` operates on implicit IT; `MEBBE` ordering and `NO WAI` optionality.
  Spec: lines 431, 433, 454 (line 433 currently `unmapped`, 431/454 mapped).  
  To check: add explicit tests for required/optional branch forms and IT source.

- [ ] `25` (notes 192-199) `WTF?` literal interpolation exclusion and escaped-colon edge cases.
  Spec: line 486 (mapped).  
  To check: add tests for `:{var}` rejection and `::` escape non-interpolation behavior.

- [ ] `26` (notes 201-205) Runtime error propagation inside `WTF?` and empty `OMG` blocks.
  Spec: line 486 (mapped).  
  To check: add tests confirming runtime exceptions stop execution and blank case blocks parse/execute correctly.

- [ ] `27` (notes 207) Loop updater variable is temporary/local.
  Spec: line 564 (mapped).  
  To check: add explicit shadowing regression demonstrating no outer-scope mutation.

- [ ] `28` (notes 209) Function argument identifier shape (“single-word identifiers”).
  Spec: line 582 (`unmapped`).  
  To check: add parse-negative tests for invalid arg identifiers; decide whether this is redundant with general identifier rule.

- [ ] `29` (notes 211-216) Function return semantics (`GTFO` => NOOB, fallthrough returns IT).
  Spec: line 590 (mapped).  
  To check: add explicit positive tests for both return paths in same fixture.

- [ ] `30` (notes 218-220) Clarify “I parameter” in call syntax.
  Spec: line 604 (`unmapped`).  
  To check: add docs/matrix note: this is syntactic marker for namespace-style call forms, not an implicit runtime parameter.

## Phase 4: BUKKIT / Methods / Inheritance (in notes order)

- [ ] `31` (notes 222-230) Slot re-declaration overwrite semantics and SRS slotname support.
  Spec: lines 632/634 prose and line 738 mapped.  
  To check: add targeted slot re-init and `SRS` slotname tests; clarify “identifier may be a function” wording.

- [ ] `32` (notes 231-237) `HOW IZ <object> <slot>` method declaration and nested-def behavior.
  Spec: lines 649+ prose. Matrix: covered indirectly by `bukkit.slot-access`/`bukkit.declaration`; nested defs are currently parser-rejected in strict mode.  
  To check: add explicit parser-policy test and note in matrix.

- [ ] `33` (notes 239-253) Function lookup order in object context (`function -> object -> global`) and IT rule.
  Spec: lines 666-672 (line 672 mapped; 666-670 currently not dedicated).  
  To check: add matrix row + tests for each namespace resolution step.

- [ ] `34` (notes 255-272) `ME` semantics, `ME HAS A`, and `ME` outside object-call error.
  Spec: line 684 (mapped).  
  To check: extend positive and negative tests to include declaration on receiver via `ME`.

- [ ] `35` (notes 274-280) `IM LIEK` inheritance behavior, parent mutation, and super-like lookup.
  Spec: line 709 (mapped), lines 790/798 (mapped).  
  To check: add explicit tests for parent mutation visibility and child write copy-on-write behavior.

- [ ] `36` (notes 282-304) Slot operator syntax, indirect `SRS`, and method-call failure when slot is not callable.
  Spec: line 738 (mapped), line 741 (`unmapped`).  
  To check: add runtime-error tests for non-callable slot invocation and parse tests for call syntax variants.

- [ ] `37` (notes 306-313) Dynamic method name via `SRS` sample program.
  Spec: line 741 (`unmapped`).  
  To check: add full snippet as executable fixture.

- [ ] `38` (notes 314-320) `omgwtf` default/override semantics and definition of “slot access fails”.
  Spec: line 768 (mapped).  
  To check: add tests for missing-slot read, missing-slot call, and non-function slot value behavior.

- [ ] `39` (notes 321-329) Reparenting (`parent` slot mutation), cycle safety, and lookup behavior in cyclic graphs.
  Spec: line 790 (mapped) + lookup prose around 792+ (partly unmapped).  
  To check: add cycle-focused tests for slot lookup and assignment traversal.

- [ ] `40` (notes 331-337) Inherited-name assignment copy-on-write and declaration error when not found.
  Spec: line 798 (mapped).  
  To check: ensure both positive and negative tests exist; include cycle path safety check.

- [ ] `41` (notes 338-343) Slot-Access Function call lexical source object semantics.
  Spec: lines 804/810 (`unmapped`).  
  To check: add dedicated matrix row and regression tests using receiver-dependent variable resolution.

- [ ] `42` (notes 344-362) “funkin/prefix” receiver-dependent lookup example.
  Spec: lines 804/810 (`unmapped`).  
  To check: add snippet verbatim as strict 1.3 fixture (normalized into full program).

- [ ] `43` (notes 364-372) Mixins reverse order and static snapshot semantics (+ parent/child mixin edge cases).
  Spec: line 849 (mapped) and static behavior prose nearby (`unmapped`).  
  To check: add tests for post-mixin source mutation non-propagation and parent/child mixin combinations.

## Phase 5: Matrix and Test Harness Integrity (ordered follow-through)

- [ ] `44` Convert each `unmapped` normative clause in `spec-1.3-clause-mapping-audit.md` into either:
  `new matrix row`, `explicitly merged with existing row (with note)`, or `example-only clause (with rationale)`.

- [ ] `45` For each checklist item above, add:
  one positive test and one negative test unless clause is explicitly non-erroring.

- [ ] `46` AST/runtime ergonomics check:
  document whether each new test required parser hacks vs compositional AST support; file follow-up refactors where pain is highest.

## Phase 6: Corpus / Harvest Check (run in order and recorded)

Completed run sequence:
1. `./scripts/analyze_corpus_gaps.sh`
2. `./scripts/eval_tier2_corpus.sh`
3. `./scripts/test_external_evidence.sh`

Current snapshots from latest run:
- Tier2 classified totals: `223` files, `184` likely-programs, outcomes: `167 parse-error`, `9 ok`, `7 lex-error`, `1 runtime-error`.
- Strict in-scope 1.3 (gap report): `13` files, `10 parse-ok`, `9 eval-ok`, `3 parse-error`, `1 runtime-error`.
- External harvested evidence: `302` fixtures assessed; observed statuses `301 parse-error`, `1 ok`; all currently triaged `unknown` in evidence table.

Next corpus/harvest actions tied to this checklist:
- [ ] `47` Partition parse-errors into `strict-non-1.3`, `spec-divergence`, `program-bug`.
- [ ] `48` Promote any checklist-related external fixtures into stable positive/negative regressions.
- [ ] `49` Re-run all three scripts after each checklist batch and append deltas to this file.

# Item-by-Item Resolution Map (`N01`-`N85`)

Scope:
- Source concern lists:
  - `/Users/jhemann/Code/lolcode-lang/spec/traceability/archive/legacy-inputs/CURRENT-SPEC-NOTES-BUGS-WORRIES.md`
  - `/Users/jhemann/Code/lolcode-lang/spec/traceability/archive/legacy-inputs/NEXT-BOTTOM-UP-SPEC-CONCERNS-2026-03-05.md`
  - `/Users/jhemann/Code/lolcode-lang/spec/traceability/archive/legacy-inputs/third-tier-of-40-issues.md`
  - `/Users/jhemann/Code/lolcode-lang/spec/traceability/archive/legacy-inputs/fourth-tier-of-40-issues.md`
- Canonical adjudication ledger:
  - `/Users/jhemann/Code/lolcode-lang/spec/traceability/NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md`

Legend:
- `implemented`: code path changed or pinned with regression tests.
- `policy`: spec underdetermined/contradictory; behavior explicitly adjudicated and pinned.
- `policy+implemented`: adjudicated policy with explicit implementation and regression pinning.
- `provisional-policy`: implemented/pinned behavior that remains provisional because an umbrella contradiction is still open in the active queue.
- `mooted`: item treated as non-normative prose conflict; strict-core behavior unchanged and documented.

## One-by-one map

| ID    | Disposition        | Implementation locus                                                                  | Evidence locus                                       |
|-------|--------------------|---------------------------------------------------------------------------------------|------------------------------------------------------|
| `N01` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/ast.rkt`                                       | `NEXT-BOTTOM-UP-TRANCHE-1-ADJUDICATION.md` row `N01` |
| `N02` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                   | adjudication row `N02`                               |
| `N03` | implemented        | `src/lolcode/ast.rkt`, `src/lolcode/parser.rkt`                                       | adjudication row `N03`                               |
| `N04` | implemented        | `src/lolcode/ast.rkt`, `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`            | adjudication row `N04`                               |
| `N05` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/ast.rkt`                                       | adjudication row `N05`                               |
| `N06` | implemented        | `src/lolcode/parser.rkt`                                                              | adjudication row `N06`                               |
| `N07` | implemented        | `src/lolcode/parser.rkt`                                                              | adjudication row `N07`                               |
| `N08` | implemented        | `src/lolcode/runtime.rkt` (binding/special-name policy)                               | adjudication row `N08`                               |
| `N09` | implemented        | `src/lolcode/lexer.rkt`, `src/lolcode/parser.rkt`                                     | adjudication row `N09`                               |
| `N10` | policy             | `src/lolcode/runtime.rkt` (scope lookup precedence)                                   | adjudication row `N10`                               |
| `N11` | policy             | `src/lolcode/runtime.rkt`                                                             | adjudication row `N11`                               |
| `N12` | policy+implemented | `src/lolcode/runtime.rkt` (`IT` split by context)                                     | adjudication row `N12`                               |
| `N13` | implemented        | `src/lolcode/runtime.rkt` (object-body lookup)                                        | adjudication rows `N13` + `N13 (edge policy)`        |
| `N14` | implemented        | `src/lolcode/runtime.rkt` (`env-define!` duplicate gate)                              | adjudication row `N14`                               |
| `N15` | implemented        | `src/lolcode/runtime.rkt` (receiver-projected slot call)                              | adjudication row `N15`                               |
| `N16` | implemented        | `src/lolcode/runtime.rkt`                                                             | adjudication row `N16`                               |
| `N17` | mooted             | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (full BUKKIT support retained)    | adjudication row `N17`                               |
| `N18` | implemented        | `src/lolcode/runtime.rkt` (prototype/copy-on-write)                                   | adjudication row `N18`                               |
| `N19` | implemented        | `src/lolcode/runtime.rkt` (`izmakin` ordering/reentrancy)                             | adjudication row `N19`                               |
| `N20` | policy+implemented | `src/lolcode/runtime.rkt` (`omgwtf` memoization + strict zero-arity hook call`)       | adjudication rows `N20` + `N20 (extended)`           |
| `N21` | implemented        | `src/lolcode/runtime.rkt` (cycle-safe parent traversal)                               | adjudication row `N21`                               |
| `N22` | implemented        | `src/lolcode/runtime.rkt` (inherited assignment COW)                                  | adjudication row `N22`                               |
| `N23` | policy             | `src/lolcode/runtime.rkt` + policy table in adjudication doc                          | adjudication row `N23` + `N23 Policy Table`          |
| `N24` | policy             | `src/lolcode/runtime.rkt` + mixin-source policy                                       | adjudication row `N24` + `N24 Policy Table`          |
| `N25` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                   | adjudication row `N25`                               |
| `N26` | implemented        | `src/lolcode/runtime.rkt` (construction binding timing)                               | adjudication row `N26`                               |
| `N27` | implemented        | `src/lolcode/runtime.rkt` (nearest `GTFO` target)                                     | adjudication row `N27`                               |
| `N28` | implemented        | `src/lolcode/runtime.rkt` (loop label matching)                                       | adjudication row `N28`                               |
| `N29` | implemented        | `src/lolcode/runtime.rkt` (condition/update order)                                    | adjudication row `N29`                               |
| `N30` | implemented        | `src/lolcode/runtime.rkt` (unary updater contract)                                    | adjudication row `N30`                               |
| `N31` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (numeric-mode duplicate handling) | adjudication row `N31`                               |
| `N32` | implemented        | `src/lolcode/runtime.rkt` (switch error propagation)                                  | adjudication row `N32`                               |
| `N33` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                   | adjudication row `N33`                               |
| `N34` | implemented        | `src/lolcode/lexer.rkt`, `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`          | adjudication row `N34`                               |
| `N35` | mooted             | runtime semantics unchanged; GC prose treated non-normative                           | adjudication row `N35`                               |
| `N36` | policy             | `src/lolcode/runtime.rkt` (identity semantics for complex values)                     | adjudication row `N36`                               |
| `N37` | implemented        | `src/lolcode/runtime.rkt` (TYPE/NOOB distinction + casts)                             | adjudication row `N37`                               |
| `N38` | implemented        | `src/lolcode/parser.rkt` (optional-article grammar sites)                             | adjudication row `N38`                               |
| `N39` | policy             | parser/call-shape remains name/slot based                                             | adjudication row `N39`                               |
| `N40` | policy+implemented | `src/lolcode/runtime.rkt` (left-to-right eager eval)                                  | adjudication row `N40`                               |
| `N41` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (dynamic labels)                  | adjudication row `N41`                               |
| `N42` | policy+implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (expr args for methods)           | adjudication row `N42`                               |
| `N43` | implemented        | `src/lolcode/lexer.rkt`, `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`          | adjudication row `N43`                               |
| `N44` | implemented        | `src/lolcode/lexer.rkt` + `PREPROCESSING_AND_KEYWORD_POLICY.md`                       | adjudication row `N44`                               |
| `N45` | implemented        | `src/lolcode/lexer.rkt` (ellipsis normalization/whitespace policy)                    | adjudication row `N45`                               |
| `N46` | implemented        | `src/lolcode/lexer.rkt`, `src/lolcode/parser.rkt` (inline block comment handoff)      | adjudication row `N46`                               |
| `N47` | implemented        | `src/lolcode/lexer.rkt` (strict numeric literal lexing)                               | adjudication row `N47`                               |
| `N48` | implemented        | `src/lolcode/runtime.rkt` (strict YARN->number cast parsing)                          | adjudication row `N48`                               |
| `N49` | implemented        | `src/lolcode/lexer.rkt`, `src/lolcode/format-placeholder.rkt`                         | adjudication row `N49`                               |
| `N50` | implemented        | `src/lolcode/format-placeholder.rkt`                                                  | adjudication row `N50`                               |
| `N51` | implemented        | `src/lolcode/lexer.rkt` (keyword longest-match/phrase collapse)                       | adjudication row `N51`                               |
| `N52` | implemented        | `src/lolcode/parser.rkt` (lvalue-only assignment)                                     | adjudication row `N52`                               |
| `N53` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (`O RLY?` from current `IT`)      | adjudication row `N53`                               |
| `N54` | implemented        | `src/lolcode/runtime.rkt` (`MEBBE` TROOF-cast semantics)                              | adjudication row `N54`                               |
| `N55` | implemented        | `src/lolcode/parser.rkt` (orphan branch rejection)                                    | adjudication row `N55`                               |
| `N56` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (`WTF?` on current `IT`)          | adjudication row `N56`                               |
| `N57` | implemented        | `src/lolcode/runtime.rkt` (case-sensitive loop labels)                                | adjudication row `N57`                               |
| `N58` | implemented        | `src/lolcode/parser.rkt` (strict `HOW IZ I`)                                          | adjudication row `N58`                               |
| `N59` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (`SRS` dynamic-name handling)     | adjudication row `N59`                               |
| `N60` | policy+implemented | `src/lolcode/runtime.rkt` + `IT_UPDATE_MATRIX.md`                                     | adjudication row `N60`                               |
| `N61` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (`VISIBLE` variadic closure)      | adjudication row `N61`                               |
| `N62` | implemented        | `src/lolcode/runtime.rkt` (`GIMMEH` implicit target declare)                          | adjudication row `N62`                               |
| `N63` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (TYPE dual role by context)       | adjudication row `N63`                               |
| `N64` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (cast target gate)                | adjudication row `N64`                               |
| `N65` | policy+implemented | `src/lolcode/runtime.rkt` (numeric-mode + identity behavior)                          | adjudication row `N65`                               |
| `N66` | policy+implemented | `src/lolcode/runtime.rkt`                                                             | adjudication row `N66`                               |
| `N67` | implemented        | `src/lolcode/runtime.rkt` (`ME` runtime resolution gate)                              | adjudication row `N67`                               |
| `N68` | implemented        | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt` (receiver existence/type checks)  | adjudication row `N68`                               |
| `N69` | implemented        | `src/lolcode/runtime.rkt` (receiver late binding for mixin-copied functions)          | adjudication row `N69`                               |
| `N70` | implemented        | `src/lolcode/runtime.rkt` (reserved-name binding rejection)                           | adjudication row `N70`                               |
| `N71` | implemented        | `src/lolcode/parser.rkt` (strict `HAI 1.3`)                                           | adjudication row `N71`                               |
| `N72` | implemented        | `src/lolcode/runtime.rkt` (BUKKIT truthiness policy)                                  | adjudication row `N72`                               |
| `N73` | policy+implemented | `src/lolcode/runtime.rkt` (host numeric portability decisions)                        | adjudication row `N73`                               |
| `N74` | policy+implemented | `src/lolcode/runtime.rkt` + `IT_UPDATE_MATRIX.md`                                     | adjudication row `N74`                               |
| `N75` | policy+implemented | `src/lolcode/runtime.rkt` (RHS sequencing guarantees)                                 | adjudication row `N75`                               |
| `N76` | implemented        | `src/lolcode/runtime.rkt` (no forward prebinding)                                     | adjudication row `N76`                               |
| `N77` | implemented        | `src/lolcode/runtime.rkt` (duplicate param rejection)                                 | adjudication row `N77`                               |
| `N78` | implemented        | `src/lolcode/parser.rkt` (nested def rejection in strict 1.3)                         | adjudication row `N78`                               |
| `N79` | implemented        | `src/lolcode/runtime.rkt` (`ME HAS A` shadow behavior)                                | adjudication row `N79`                               |
| `N80` | implemented        | `src/lolcode/runtime.rkt` (`ME'Z slot R expr` sequencing)                             | adjudication row `N80`                               |
| `N81` | policy+implemented | `src/lolcode/runtime.rkt` (mixin shallow alias policy)                                | adjudication row `N81`                               |
| `N82` | policy+implemented | `src/lolcode/runtime.rkt` (call-by-sharing consistency)                               | adjudication row `N82`                               |
| `N83` | implemented        | `src/lolcode/runtime.rkt` (non-BUKKIT parent chain termination)                       | adjudication row `N83`                               |
| `N84` | implemented        | `src/lolcode/runtime.rkt` (method-call miss uses full slot-access + one-shot `omgwtf`) | adjudication row `N84`                               |
| `N85` | implemented        | `src/lolcode/runtime.rkt` (`izmakin` failure atomicity)                               | adjudication row `N85`                               |

## Notes on “already correct” and “mistake”

- “already handled / code correct” concerns are reflected here as `implemented` with test pinning (no later divergence found).
- “mistake fixed” concerns were moved to `implemented` after correction; examples called out in the assessment ledger include strict cast-target gating and strict-case enforcement.
- “mooted” concerns are prose/spec-conflict items where strict 1.3 behavior is maintained and documented rather than extending semantics.

# First-Principles Spec Subtlety Audit (2026-03-10)

Scope:
- `spec/upstream/lolcode-spec-v1.3.md` read first, without trusting adjudication outputs.
- Then cross-checked against active traceability/adjudication docs for consistency and adequacy.

Method:
1. Extracted candidate subtle/contradictory clauses directly from upstream 1.3 text.
2. Wrote independent “best coherent reading” per clause cluster.
3. Compared those readings to current policy/docs/tests.
4. Marked each as:
   - `aligned` (decision appears textually coherent and documented),
   - `policy-pin` (spec underdetermined/contradictory; policy required),
   - `needs-clarity` (decision may be fine but docs should be sharpened).

---

## 1) Clause-by-clause first-principles results

| ID | Spec anchors | First-principles reading | Current decision refs | Result |
|---|---|---|---|---|
| FP-01 | 89 | Grammar requires `HAI <version>` but text says no standard behavior for using version number. | `N71`, parse negatives `unsupported-v12`, `unsupported-v14`, `missing-version` | `policy-pin` (strict 1.3 chosen; coherent with project scope) |
| FP-02 | 105, 666-672, 725 | `global` terminology conflicts with “no global scope”; must be reconciled as namespace-layer wording, not process-global mutable singleton. | `N12`, `N60`, `N74`, textual checklist C1/C2/C3 | `policy-pin` (activation-local `IT`, receiver-bypass for bare `IT`) |
| FP-03 | 111 | Identifier shape is broad (letters/digits/underscore) and does not define keyword reservation explicitly. | `ADJUDICATION_POLICY.md` reserved-keyword section, `N70`, parser negatives | `policy-pin` (strict reserved keywords in direct identifier positions) |
| FP-04 | 170-199 | `SRS` says “anywhere identifier expected”, including declaration shorthand (`I HAS SRS name ...`). | `N59`, parser/runtime SRS tests | `aligned` (contextual grammar sites are explicit and tested) |
| FP-05 | 277-287, 356, 383-387 | Optional `AN` applies for operators/variadics; `VISIBLE` syntax is adjacency-based (`VISIBLE <expr> [<expr> ...]`) and does not require `AN`. | `N61`, parser change on 2026-03-10, edge-case regression for adjacent composite expressions | `aligned` (recently fixed) |
| FP-06 | 582, 599-604, 744 | Function-call args are expressions; slot-call signature says `<variable>` and is ambiguous against expression semantics. | `N42`, method expression-arg tests | `policy-pin` (expression args for method calls) |
| FP-07 | 729, 732 | Slot operator prose says `-`, syntax examples use `'Z`; treat as equivalent or choose one and reject the other. | `N06`, textual checklist A8 | `policy-pin` (accept both as equivalence) |
| FP-08 | 768 | `omgwtf` trigger/return defined; argument list unspecified; “default implementation of canhas” appears editorial typo. | `N20`, `N84`, `G4` | `policy-pin` (zero-arity hook, one-shot after full miss-path, memoize) |
| FP-09 | 770, 790, 855 | `izmakin` runs after full prototype construction and before return; must see restored parent/mixin-complete state. | `N19`, `N23` | `aligned` |
| FP-10 | 796-800 | Lookup/assignment up parent chain plus cycle stopping and child-local shadow-on-write are explicit. | `N21`, `N22`, cycle/copy-on-write regressions | `aligned` |
| FP-11 | 804-831 | Slot-call functions are receiver-dynamic regardless of where function value is stored. | `N15`, `N69` | `aligned` |
| FP-12 | 849, 857, 871 | Mixin copy semantics conflict: “defined on mixin” vs “and parent slots” example comment; static snapshot is explicit. | `N24`, `N81` | `policy-pin` (effective-visible donor members + static snapshot + shallow alias) |
| FP-13 | 33-35 | Line continuation explicitly allows both `...` and Unicode ellipsis `u2026`. | `N45`, lexer continuation tests | `aligned` |
| FP-14 | 219 vs 608-878 | “Arrays (BUKKIT) reserved for future expansion” conflicts with extensive BUKKIT semantics below; treat early phrase as stale/editorial. | `N17` (mooted), full object/runtime support | `aligned` (documented as non-normative conflict) |
| FP-15 | 145 (`HOW DUZ I`) vs 574 (`HOW IZ I`) | The spec contains two definition-site spellings; strict parser accepts `HOW IZ` and `HOW DUZ` as definition-site synonyms while keeping call syntax `IZ` only. | `N58`, `N89`, parser/runtime `HOW DUZ` coverage and `I DUZ` negative | `aligned` |

---

## 2) Adequacy check on current docs

### Strongly adequate
- `IT` contradiction and method fallthrough behavior now consistently documented as activation-local policy.
- `omgwtf` boundary/arity/non-callable-after-synthesis behavior is explicit and regression-pinned.
- Receiver-dynamic slot-call semantics and copy-on-write parent behavior are clearly covered.
- Mixin reverse/static behavior and source-set conflict are explicitly policy-pinned.

### Still policy-pinned (by necessity, not drift)
- Global-scope wording conflict (`105` vs `666-672` vs `725`).
- Reserved-keyword policy vs broad identifier grammar.
- Mixin source-set conflict (`849` vs `871`).
- `omgwtf` call signature omission.
- Method-call arg “variable” wording vs expression-level call semantics.

### Minor clarity opportunities
1. Keep an explicit note that `VISIBLE` adjacency-without-`AN` is now supported for composite expressions (recent parser fix), to prevent future regression via typo-guard heuristics.
2. Keep editorial-conflict notes visible for:
   - `HOW DUZ I` vs `HOW IZ I` (definition-site synonym accepted; call syntax remains `IZ`),
   - “BUKKIT reserved for future expansion” vs full BUKKIT chapter.

---

## 3) Bottom line

This first-principles pass converges to the same core adjudications already in use.

No new hard spec contradictions were discovered beyond the known policy-pinned set.
The main actionable issue discovered during this pass (and already fixed in code/tests) was `VISIBLE` adjacency parsing for composite expressions.

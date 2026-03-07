# LOLCODE 1.3 Expert Checklist Adjudication (Pass 1)

Date: 2026-03-06
Inputs:
- `spec/traceability/lolcode_1_3_expert_review_checklist.md`
- `spec/upstream/lolcode-spec-v1.3.md`
- `src/lolcode/parser.rkt`
- `src/lolcode/runtime.rkt`
- `src/lolcode/runtime/value.rkt`
- `tests/spec/runtime-core-test.rkt`
- `tests/spec/spec-audit/known-gaps-failing-test.rkt`
- Governing adjudication policy:
  - `spec/traceability/SPEC_ADJUDICATION_POLICY.md`
  - This pass applies that policy's Decision Ladder and Exegesis Principles to each item.
- Follow-on deep audit delta:
  - `spec/traceability/EXPERT_REVIEW_DEEP_AUDIT_DELTA_2026-03-06.md`

Legend:
- `MATCH` = implementation aligns with adjudicated reading.
- `DIVERGENCE` = implementation likely deviates from strict textual reading.
- `OPEN` = underspecified/contradictory area; narrow policy selected but should remain explicitly tracked.

## Post-Pass1 Remediation Snapshot (2026-03-07)

Closed from prior `DIVERGENCE` queue:

1. `B7/H1` method-namespace split removed; dispatch now uses callable slots only.
2. `B8/H2/H3/H4` synthetic receiver fallback removed.
3. `omgwtf` slot-assigned callable convention defect fixed (env-first slot-call path).

Evidence:
- `src/lolcode/runtime.rkt`
- `src/lolcode/runtime/value.rkt`
- `tests/spec/runtime-core-test.rkt`:
  - `method-defs-are-slot-callables`
  - `omgwtf-slot-function-call-convention`

## A. Parsing / AST distinctions

- `A1` ordinary function def vs slot-function def: `T/I`; `MATCH`.
  Evidence: spec `HOW IZ I ...` (line ~574) vs `HOW IZ <object> <slot>` (line ~649); parser emits `stmt-function-def` vs `stmt-method-def`; AST split tested (`N01`) in `runtime-core-test.rkt`.

- `A2` ordinary call vs slot-call: `T`; `MATCH` (with one caveat in B8/B9).
  Evidence: spec plain call (line ~599) vs slot-call examples (object section); parser emits `expr-call` vs `expr-method-call`.

- `A3` expression `SMOOSH` vs inheritance/mixin `SMOOSH`: `T/I`; `MATCH`.
  Evidence: spec variadic `SMOOSH ... MKAY` (line ~356) vs mixin `SMOOSH` in inheritance (line ~835+); parser emits `expr-variadic` vs `expr-prototype`; disambiguation test `N05` exists.

- `A4` slot access vs slot call vs identifier lookup: `T`; `MATCH`.
  Evidence: parser has distinct forms (`expr-slot`, `expr-method-call`, `expr-ident`) and runtime dispatch paths differ.

- `A5` `SRS` is dynamic slot-name/call-name, not receiver reinterpretation: `T + X`; `DIVERGENCE`.
  Evidence: spec `SRS` slot-name usage (line ~738, line ~750). Current runtime has synthetic identifier-only fallback in `expr-method-call` (`runtime.rkt`) that is not textually grounded.
  Decision: forbid receiver-name fallback extension.

- `A6` `O HAI IM` contextual `I`: `T/U`; `MATCH` under runtime-context policy.
  Evidence: spec says inside `O HAI IM` anything `I` refers to object (line ~709+). Current implementation does runtime contextual handling (object-def context + method-def lowering), not parser rewrite.
  Decision: keep runtime contextual evaluation; do not add ad hoc parser rewrites unless needed for strictness.

- `A7` `O HAI IM` lookup regime: `T`; `MATCH` (with IT contradiction tracked in section C).
  Evidence: spec says slot-first then global then error (line ~725). Runtime method/slot-call environment layering implements function namespace then receiver slots then global root.

- `A8` slot operator typo (`-` vs `'Z`): `C`; `MATCH` with conservative resolution.
  Evidence: prose typo line ~729 conflicts with grammar examples line ~738. Lexer/parser canonicalize `'Z`; no `-` slot operator accepted.
  Decision: keep `'Z` only; treat `-` prose as editorial defect.

## B. Receiver, lookup, and call mechanics

- `B1` receiver-dynamic slot-function calls: `T`; `MATCH`.
  Evidence: bukkit scope text + parent/testClass example (line ~815+). Implemented through receiver-projected env during slot-call (`runtime.rkt`) and tested by receiver-namespace regressions.

- `B2` function namespace -> object namespace -> global: `T`; `MATCH` as implemented policy.
  Evidence: spec line ~672 + nearby bukkit scope prose. Runtime uses call env (params/local), then receiver projection, then root env.
  Note: conflicts with “no global scope” tracked in C1.

- `B3` `ME` only with calling object: `T`; `MATCH`.
  Evidence: spec line ~684. Runtime only binds `ME` in method/slot-call contexts; plain-call `ME` is runtime error.

- `B4` `ME HAS A` / `ME'Z` target receiver slots: `T`; `MATCH`.
  Evidence: spec line ~689 and ~698 examples. Runtime `ME'Z` compiles to slot lvalue on receiver object.

- `B5` params/locals shadow slots; `ME'Z` escape hatch: `I`; `MATCH`.
  Evidence: lookup order + explicit prose around `ME'Z`; runtime environment ordering and tests support this.

- `B6` slot-call on non-function slot: `U`; `MATCH` with conservative policy.
  Policy: runtime type error.
  Evidence: test `method-call-noncallable-slot` exercises this boundary.

- `B7` distinct method namespace outranking callable slots: `X`; `DIVERGENCE`.
  Evidence: spec presents functions-in-slots model; runtime currently tries method-table dispatch before callable-slot dispatch.
  Decision: remove method-table precedence for strict mode.

- `B8` synthetic namespaced fallback (`I IZ ghost'Z hi MKAY` when `ghost` unbound): `X`; `DIVERGENCE`.
  Evidence: not recoverable from plain-call or slot-call grammar; runtime currently synthesizes fallback name.
  Decision: remove extension; require explicit valid call forms only.

- `B9` no equivalent fallback for `SRS` receiver path: fallback itself `X`; asymmetry confirms artifact.
  Status: `OPEN` only until B8 removed; then this becomes moot by design.

## C. Scope contradictions and IT

- `C1` “no global scope” vs “global lookup in bukkit scope”: `C`; `OPEN`.
  Current policy: treat runtime root frame as the practical “global” namespace for call resolution.
  Decision: keep policy documented; do not create hidden extra scopes.

- `C2` local IT vs method IT global lookup: `C`; `OPEN` (currently implemented per bukkit clause).
  Evidence: expression IT local prose (line ~407) vs bukkit IT-global clause (line ~672).
  Current implementation aliases method IT to runtime root IT.

- `C3` default method return via IT under contradiction: `C`; `OPEN`.
  Current behavior follows C2 policy (global IT in method context). Keep explicitly documented until formal adjudication chooses otherwise.

## D. Prototyping, parent chains, mutation

- `D1` parent slot auto-created: `T`; `MATCH`.
  Evidence: inheritance prose (line ~790); runtime ensures `parent` special slot and resets parent after mixin application.

- `D2` parent mutation allowed: `T`; `MATCH`.
  Evidence: spec explicitly allows changing parent slot; lookup uses dynamic parent chain.

- `D3` cycle detection on parent-chain lookup: `T`; `MATCH`.
  Evidence: lookup stop condition line ~796; runtime uses visited-set in slot/method lookup.

- `D4` cycle detection on assignment existence search: `I`; `MATCH`.
  Evidence: assignment chain prose line ~798 + runtime assignment path uses same cycle-safe lookup.

- `D5` assignment to inherited name shadows locally (copy-on-write): `T`; `MATCH`.
  Evidence: spec line ~798 explicit; runtime assignment creates local slot when name exists only in ancestor.

- `D6` assignment to missing name is declaration error: `T`; `MATCH`.
  Evidence: spec line ~798; runtime raises unknown slot when chain lookup fails.

- `D7` shallow aliasing for nested BUKKIT across parent/child: `I/U`; `MATCH` under conservative non-deep-copy policy.
  Decision: keep shallow alias semantics; do not invent deep cloning.

## E. Special slots (`omgwtf`, `izmakin`)

- `E1` every bukkit contains `parent/omgwtf/izmakin`: `T`; `MATCH`.
  Evidence: special-slot list line ~762+; implemented in object initialization.

- `E2` `omgwtf` on missing slot access; result installed or throw: `T`; `MATCH` (slot-access path).
  Evidence: spec line ~768; runtime `get-slot` -> `call-omgwtf!` memoizes returned value.

- `E3` what counts as “slot access fails”: `U`; `OPEN`.
  Current policy: missing-slot lookup only. Non-callable slot-call is type error, not `omgwtf` hook trigger.

- `E4` parent-chain first, then single `omgwtf`: `U`; `MATCH` with conservative policy.
  Current runtime searches chain, then invokes hook once on original receiver.

- `E5` which object’s `omgwtf`: `U`; `MATCH` with conservative policy.
  Current runtime invokes on original receiver only.

- `E6` `omgwtf` vs global fallback interaction: `U/X`; `OPEN` until B8 removed.
  Policy target: keep slot lookup distinct from global call fallback.

- `E7` per-object defaults masking inherited special slots: `U/X`; `OPEN`/partial divergence.
  Nuance: inherited special methods can still be found via method-chain lookup, but slot-assigned hooks can be masked by per-object defaults.
  Decision: do not bless masking behavior without explicit textual necessity.

- `E8` `izmakin` timing and inheritance details: high-level `T`, details `U`; `OPEN`.
  Current behavior: invoked after object construction/prototyping; inherited method form can run; slot-form inheritance depends on masking behavior.

- `E9` state visible to `izmakin`: `U`; `MATCH` with conservative policy.
  Current behavior: runs after parent+mixin shaping and body execution in object-def path.

## F. Mixins and inheritance `SMOOSH`

- `F1` reverse mixin order: `T`; `MATCH`.

- `F2` mixin copy is static snapshot: `T`; `MATCH`.

- `F3` own-only vs own+inherited mixin copy: `C`; `MATCH` under narrow conservative policy (own-only).
  Decision: keep own-only until explicit stronger text overrides.

- `F4` shallow vs deep copy of slot values: `U`; `MATCH` under conservative shallow-copy policy.

- `F5` copied functions remain receiver-dynamic on slot-call: `I`; `MATCH`.

- `F6` parent/child combinations in mixin sets: `U`; `OPEN` (edge behavior depends on F3/F4 policy interactions).

- `F7` post-construction manual mixin/prototype surgery pattern: `T`; `MATCH`.

## G. Evaluation order and side effects

- `G1` are SMOOSH args eager: evaluation required `I`, order `U`; `OPEN` policy.
  Current behavior is eager left-to-right; keep documented as implementation policy unless stronger text found.

- `G2` distinct missing slot operands in one SMOOSH invoke hook per access: `I/U`; `MATCH` with current policy.

- `G3` earlier side effects before later operand error: `U`; `OPEN`.
  Current implementation preserves earlier effects before later error in left-to-right evaluation.

- `G4` slot-call after omgwtf synthesizes non-function: `U`; `OPEN`.
  Desired conservative policy: synthesize value, then runtime type error if call attempted on non-function.
  Note: current method-call path may bypass `omgwtf` on missing method names; this should be revisited with B7/B8 cleanup.

## H. User-supplied observations triage

- `H1` method over callable slot on `obj IZ name`: `X`; `DIVERGENCE`.
- `H2` synthetic fallback for `I IZ ghost'Z hi MKAY`: `X`; `DIVERGENCE`.
- `H3` fallback blocked when receiver bound non-BUKKIT: artifact of H2; `DIVERGENCE`.
- `H4` no same fallback for `SRS` receiver: artifact evidence; `OPEN` until H2 removed.
- `H5` inherited slot function receiver-dynamic: `T`; `MATCH`.
- `H6` shallow copy-on-write aliasing: `I/U`; `MATCH` policy.
- `H7` SMOOSH eager effects: `I/U`; `OPEN` policy.
- `H8` omgwtf fires per missing operand access: `I/U`; `MATCH` policy.
- `H9` reverse mixin precedence: `T`; `MATCH`.
- `H10` child defaults mask inherited special hooks: `U/X`; `OPEN` partial divergence.

## Priority Fix Queue From This Pass

1. Remove synthetic namespaced receiver fallback (`B8/H2/H3/H4`).
2. Remove method-table precedence over callable slot values (`B7/H1`).
3. Resolve/normalize special-slot masking behavior for slot-assigned `omgwtf`/`izmakin` (`E7/H10`).
4. Add explicit tests for `G4` and for `E4/E5` (single hook call on original receiver after chain failure).
5. Keep contradiction policies (`C1/C2/C3`) explicitly documented unless/until expert chooses alternate narrow repair.

## Confirmed Test Run During This Pass

- `raco test tests/spec/runtime-core-test.rkt tests/spec/spec-audit/known-gaps-failing-test.rkt`
- Result: `486 tests passed`.

## I. Do-Not-Extend Rules Compliance (Checklist Section I)

1. Do not add separate method namespace outranking callable slots: `VIOLATED` (B7/H1).
2. Do not add synthetic namespaced fallback for `I IZ ghost'Z hi MKAY`: `VIOLATED` (B8/H2).
3. Do not reinterpret `SRS` receiver result as namespace name: `MATCH` (no generic reinterpretation path for `SRS` receiver branch).
4. Do not silently treat slot-call on non-function as ordinary slot access: `MATCH` (runtime error).
5. Do not invoke `omgwtf` once per ancestor hop by default: `MATCH` (single invocation after total miss).
6. Do not assume inherited `omgwtf`/`izmakin` masked by defaults unless compelled: `OPEN/PARTIAL` (slot-based special hooks can be masked).
7. Do not introduce deep-copy mixin semantics: `MATCH` (shallow copy policy).
8. Do not switch to parent-locked/definition-locked receiver semantics: `MATCH` (receiver-dynamic).
9. Do not repair IT contradiction via hidden extra scope machinery: `MATCH` (current behavior is explicit root-frame policy).

## J. Recommended Tests Coverage (Checklist Section J)

Status legend:
- `covered` = explicit existing test(s).
- `partial` = related tests exist but not the exact edge.
- `missing` = no direct dedicated test yet.

| Test ID | Requested scenario | Status | Current evidence |
|---|---|---|---|
| J1 | parent/child receiver-dynamic method call | covered | receiver-namespace tests around inherited slot function behavior. |
| J2 | inherited assignment shadows child-local, not parent mutation | covered | parent copy-on-write tests (`runtime-core-test.rkt`, parent chain section). |
| J3 | assign missing slot in hierarchy errors | covered | unknown-slot assignment errors and cycle-assignment missing-name tests. |
| J4 | parent-cycle lookup terminates | covered | `parent-cycle-lookup-terminates`. |
| J5 | parent-cycle assignment search terminates | covered | `parent-cycle-assignment-terminates` and existing-name variant. |
| J6 | missing slot + parent chain + omgwtf: original receiver vs ancestor | partial | single-receiver omgwtf behavior tested; explicit ancestor-vs-receiver comparator test should be added. |
| J7 | synthesized non-function then called | missing | not currently explicit after `omgwtf` materialization path. |
| J8 | inherited `izmakin`: runs or not | partial | broad izmakin tests exist; explicit inherited-only/no-child-override case should be isolated. |
| J9 | child without explicit special hooks: inherited visible or masked | partial | child-shadow tests exist; explicit no-child-hook inheritance test should be added for slot-assigned hooks. |
| J10 | mixins `m1 AN m2`: leftmost wins | covered | `mixin-object` precedence test. |
| J11 | later donor mutation does not affect recipient | covered | `mixin-static-snapshot`. |
| J12 | mixin own-only vs own+inherited copy source | covered | `mixin-source-own-only-slots` and methods variant. |
| J13 | nested mutable slot alias/copy behavior | covered | `mixin-static-snapshot-mutable-alias`. |
| J14 | SMOOSH with two missing slots: hook count/order | missing | no dedicated two-missing-slot count/order test in SMOOSH form. |
| J15 | SMOOSH side effect in earlier arg then later arg errors | missing | no dedicated error-ordering test for SMOOSH operands. |
| J16 | slot-call non-function exact runtime error | covered | `method-call-noncallable-slot`. |
| J17 | `ME` in plain function call errors | partial | current tests imply this behavior; add direct dedicated `ME` plain-call test. |
| J18 | `ME'Z` vs param shadowing | partial | related `ME'Z` tests exist; add dedicated param-shadow pair. |
| J19 | IT in ordinary function vs method default return | covered | `function-implicit-it-return`, IT-local/global method tests. |
| J20 | `O HAI IM` lookup in block incl nested `HOW IZ I` | covered | object lookup and contextual method-def tests; nested defs forbidden in strict parser checks. |

## K. Minimal Spec Anchors (Checklist Section K)

Anchors from `spec/upstream/lolcode-spec-v1.3.md` used in this pass:
- Scope/no-global statement (~line 105).
- `SRS` operator (~line 168).
- Variadic `SMOOSH` and optional `MKAY` closure (~line 356).
- Expression statements and local IT (~line 407).
- Functions/default return (~line 574 and ~line 592).
- Bukkit function scope, `ME`, and IT-global clause (~line 672+).
- `O HAI IM` and lookup regime (~line 709+ and ~line 725).
- Slot access and `SRS` dynamic slot names (~line 738+).
- Special slots `parent`, `omgwtf`, `izmakin` (~line 762+).
- Inheritance/parent-chain lookup + assignment semantics (~line 790, ~line 796, ~line 798).
- Function + inheritance receiver example (~line 815+).
- Mixin inheritance rules and examples (~line 835+ to ~line 872).

## L. What about all the printing?

Do we print all the types correctly? Does our printer print values like booleans correctly? What about strings? *Is* there a way to print strings unambiguously? Should they be read back in as is? What about other datatypes--do we get that printing of values back out right? 

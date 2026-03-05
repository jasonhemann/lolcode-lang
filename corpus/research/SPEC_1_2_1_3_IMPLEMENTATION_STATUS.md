# LOLCODE 1.3 Implementation Status (Project Snapshot)

Last updated: 2026-03-05

## Scope and Caveat

- Normative target for this project is strict 1.3 behavior.
- Parser rejects non-1.3 program headers (`HAI 1.2`, `HAI 1.4`, bare `HAI`, codename-style headers).
- 1.4-like library/import features are explicitly out of scope for core conformance.
- This is a code-and-test grounded status snapshot, not a claim of line-by-line formal spec completeness.

## Coverage Summary

- Conformance fixtures in `tests/spec/fixtures/manifest.rktd`: `16`
- Current full suite result: `409 tests passed` (`./scripts/test_racket.sh`)
- Clause-level traceability artifacts now live under:
  - `spec/upstream/` (vendored 1.2/1.3 spec snapshots + provenance)
  - `spec/traceability/spec-1.3-matrix.rktd` (machine-readable clause status)
  - `spec/traceability/spec-1.3-clause-index.tsv` (generated heading/normative index)
  - `scripts/check_spec_traceability.rkt`, `scripts/extract_spec_clauses.rkt`
  - `tests/spec/spec-audit/traceability-test.rkt`, `tests/spec/spec-audit/edge-cases-test.rkt`

## Implemented

| Area                                                                                                                                              | Status      | Evidence                                                                                |
|---------------------------------------------------------------------------------------------------------------------------------------------------|-------------|-----------------------------------------------------------------------------------------|
| Program envelope (`HAI ... KTHXBYE`)                                                                                                              | Implemented | `src/lolcode/parser.rkt`                                                                |
| Declarations/assignment (`I HAS A`, `R`, typed defaults)                                                                                          | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                     |
| Input/output (`GIMMEH`, `VISIBLE`, `VISIBLE ... !`)                                                                                               | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, `tests/spec/runtime-core-test.rkt` |
| Arithmetic and logic core ops (`SUM`, `DIFF`, `PRODUKT`, `QUOSHUNT`, `MOD`, `BIGGR`, `SMALLR`, `BOTH/EITHER/WON`, `NOT`, `BOTH SAEM`, `DIFFRINT`) | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                     |
| Strict operator spelling for core ops (reject aliases like `DIFFERENCE`, `QOUSHUNT`)                                                            | Implemented | `src/lolcode/parser.rkt`, `tests/spec/parse-negative-test.rkt`, `tests/spec/spec-audit/edge-cases-test.rkt` |
| Variadics (`SMOOSH`, `ALL OF`, `ANY OF`)                                                                                                          | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                     |
| Casting (`MAEK`, `IS NOW A`)                                                                                                                      | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                     |
| `O RLY?` / `MEBBE` / `NO WAI`                                                                                                                     | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| `WTF?` / `OMG` / `OMGWTF` / fallthrough / `GTFO`                                                                                                  | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| Loops (`IM IN YR` / `IM OUTTA YR`, `UPPIN`/`NERFIN`, `TIL`/`WILE`)                                                                                | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| Functions (`HOW IZ I`, `I IZ`, `FOUND YR`)                                                                                                        | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| Standalone function-call statement (`I IZ ... MKAY`)                                                                                              | Implemented | `src/lolcode/parser.rkt` (`call-stmt`), `tests/spec/runtime-core-test.rkt`              |
| Objects (`O HAI IM`, `IM LIEK`, slots via `HAS` / `HAS A` / `HAS AN` / `'Z`, methods)                                                            | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| Dynamic identifiers (`SRS`) for declaration and slot/target access                                                                                | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| Comments and line continuation (`BTW`, `OBTW`/`TLDR`, `...`, `…`)                                                                                 | Implemented | `src/lolcode/lexer.rkt`, parse-negative/runtime tests                                   |
| Numeric literal validation (reject malformed forms like `1..23`, `- 123`)                                                                        | Implemented | `src/lolcode/lexer.rkt`, `src/lolcode/parser.rkt`, `tests/spec/parse-negative-test.rkt` |
| Core literals (`WIN`, `FAIL`, `NOOB`)                                                                                                             | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, tests                              |

## Partial / Known Limitations

| Area                             | Status  | Notes                                                                                                                                                                                    |
|----------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Standalone expression statements | Implemented | Statement-position expressions now compile via full `expr` grammar, including postfix slot/method forms that feed `IT` for subsequent `O RLY?` usage. |
| Parser conflict profile          | Partial | Grammar currently runs with high parser-tool conflict counts (SR/RR). Functional behavior is tested and passing, but grammar shape still has technical debt.                              |
| YARN escape + interpolation surface | Implemented | Escapes include `::`, `:\"`, `:)`, `:>`, `:o`, `:(hex)`, and `:[UNICODE NORMATIVE NAME]`; runtime also expands `:{name}` placeholders against lexical environment bindings. |
| Function-definition placement    | Implemented restriction | Strict 1.3 mode rejects nested `HOW IZ I` definitions; function defs are accepted only at top-level and object-body method declaration sites. |
| Line-continuation empty-line rule | Implemented | Lexer now rejects continuation lines followed by blank lines, except continuation-only line behavior described in 1.3 text. |
| Optional `AN` parsing behavior   | Implemented | Parser supports optional `AN` as documented by 1.3 operator grammar; this can make `AND` lex as an identifier in omitted-`AN` expressions. |
| Variadic EOL closure (`ALL OF` / `ANY OF` without trailing `MKAY`) | Implemented | Parser accepts EOL closure for open variadics per 1.3 line 269 (covered in `tests/spec/spec-audit/known-gaps-failing-test.rkt`). |
| Identifier lexical constraints | Implemented | 1.3 line 111 enforced: identifiers must start with a letter and contain only letters/digits/underscore; invalid forms like `_x`, `x-y`, `++` are parse errors (see `tests/spec/parse-negative-test.rkt`). |
| `OMG` interpolation restriction | Implemented | Parser rejects interpolated YARN case literals in `OMG` per 1.3 line 486. |
| Object special-slot semantics (`parent`/`omgwtf`/`izmakin`) | Implemented | Runtime now supports parent-chain slot lookup, `omgwtf` fallback slot/method hook, and post-construction `izmakin` hook. |

## Not Yet Implemented (or intentionally deferred)

| Area                                                                        | Status                  | Notes                                                                                                            |
|-----------------------------------------------------------------------------|-------------------------|------------------------------------------------------------------------------------------------------------------|
| Source-file include semantics for `CAN HAS <path>?` (1.2/1.3 behavior)     | Implemented             | Runtime resolves and executes `CAN HAS "file.lol"?` includes with load-once behavior and nested relative-path base-dir handling. |
| Mixin inheritance syntax (`IM LIEK <parent> SMOOSH <mixin> ...`)           | Implemented             | Parser and runtime support mixin inheritance for object header and declaration forms. |
| `WAZZUP` / `BUHBYE` variable-block delimiters                               | Out of spec             | Not present in archived 1.1 nor official 1.2/1.3 specs; treat as non-normative dialect syntax from third-party implementations. |
| Strict YARN-to-number cast acceptance                                       | Implemented             | Runtime now accepts only strict decimal numeric lexical forms for YARN-to-number coercion. |
| 1.4 library/import model (`CAN HAS ...?`, library-qualified extension APIs) | Deferred / Out of scope | See `corpus/research/SPEC_1_4_EXTENSION_STATUS.md`.                                                              |

## Prioritized Next Fixes

1. Reduce parser conflict footprint while preserving strict 1.3 behavior.
2. Extend conformance coverage depth for dynamic identifier interactions (`SRS`) across corpus-derived edge cases.
3. Expand targeted corpus triage for external issue/PR/commit evidence waves.

## Chosen Approach: `CAN HAS` Libraries

- Decision: implement `CAN HAS STDIO?` and `CAN HAS STRING?` as runtime-resolved library names in a Racket-native library registry, plus `CAN HAS "<file>"?` source includes in strict 1.3 mode.
- Representation: each library exposes LOLCODE-callable bindings through existing runtime value/function mechanisms.
- Default non-goal: no C FFI dependency for baseline support; only consider FFI for future platform-specific extensions that cannot be covered by Racket libraries.

## Audit Regression Tests

- `tests/spec/spec-audit/known-gaps-failing-test.rkt` now acts as regression coverage for previously-missing spec behaviors.
- Cases include variadic EOL closure, `OMG` interpolation rejection, and object special-slot/parent-chain semantics.

## Cast Strictness Follow-up Samples

- LCI integer relaxed-cast sample (now correctly rejected in strict mode):
  `corpus/tier1/lci/files/test/1.3-Tests/7-Operators/17-ExplicitCast/3-ToInteger/5-FromString/4-RelaxedNumbers/test.lol`
- LCI float relaxed-cast sample (now correctly rejected in strict mode):
  `corpus/tier1/lci/files/test/1.3-Tests/7-Operators/17-ExplicitCast/4-ToFloat/5-FromString/4-RelaxedNumbers/test.lol`
- Context note:
  `corpus/research/RELAXED_CAST_SPEC_NOTE_2026-03-02.md`.

## Why this snapshot is reliable

- It is based on current parser/runtime implementation plus tests/fixtures in-tree.
- Unsupported ops are now surfaced early (compile-stage) and mapped into structured `unsupported` results.
- As of this snapshot, `tests/spec/spec-audit/known-gaps-failing-test.rkt` is green and retained as regression protection.

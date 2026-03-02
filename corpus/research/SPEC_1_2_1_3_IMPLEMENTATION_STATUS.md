# LOLCODE 1.3 Implementation Status (Project Snapshot)

Last updated: 2026-03-02

## Scope and Caveat

- Normative target for this project is strict 1.3 behavior.
- Parser rejects non-1.3 program headers (`HAI 1.2`, `HAI 1.4`, bare `HAI`, codename-style headers).
- 1.4-like library/import features are explicitly out of scope for core conformance.
- This is a code-and-test grounded status snapshot, not a claim of line-by-line formal spec completeness.

## Coverage Summary

- Conformance fixtures in `tests/spec/fixtures/manifest.rktd`: `16`
- Current full suite result: `286 tests passed` (`./scripts/test_racket.sh`)

## Implemented

| Area                                                                                                                                              | Status      | Evidence                                                                                |
|---------------------------------------------------------------------------------------------------------------------------------------------------|-------------|-----------------------------------------------------------------------------------------|
| Program envelope (`HAI ... KTHXBYE`)                                                                                                              | Implemented | `src/lolcode/parser.rkt`                                                                |
| Declarations/assignment (`I HAS A`, `R`, typed defaults)                                                                                          | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                     |
| Input/output (`GIMMEH`, `VISIBLE`, `VISIBLE ... !`)                                                                                               | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, `tests/spec/runtime-core-test.rkt` |
| Arithmetic and logic core ops (`SUM`, `DIFF`, `PRODUKT`, `QUOSHUNT`, `MOD`, `BIGGR`, `SMALLR`, `BOTH/EITHER/WON`, `NOT`, `BOTH SAEM`, `DIFFRINT`) | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                     |
| Variadics (`SMOOSH`, `ALL OF`, `ANY OF`)                                                                                                          | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                     |
| Casting (`MAEK`, `IS NOW A`)                                                                                                                      | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                     |
| `O RLY?` / `MEBBE` / `NO WAI`                                                                                                                     | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| `WTF?` / `OMG` / `OMGWTF` / fallthrough / `GTFO`                                                                                                  | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| Loops (`IM IN YR` / `IM OUTTA YR`, `UPPIN`/`NERFIN`, `TIL`/`WILE`)                                                                                | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| Functions (`HOW IZ I`, `I IZ`, `FOUND YR`)                                                                                                        | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| Standalone function-call statement (`I IZ ... MKAY`)                                                                                              | Implemented | `src/lolcode/parser.rkt` (`call-stmt`), `tests/spec/runtime-core-test.rkt`              |
| Objects (`O HAI IM`, `IM LIEK`, slots via `HAS A` / `'Z`, methods)                                                                                | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| Dynamic identifiers (`SRS`) for declaration and slot/target access                                                                                | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                           |
| Comments and line continuation (`BTW`, `OBTW`/`TLDR`, `...`)                                                                                      | Implemented | `src/lolcode/lexer.rkt`, parse-negative/runtime tests                                   |
| Core literals (`WIN`, `FAIL`, `NOOB`)                                                                                                             | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, tests                              |

## Partial / Known Limitations

| Area                             | Status  | Notes                                                                                                                                                                                    |
|----------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Standalone expression statements | Partial | Only direct function-call statement form (`I IZ ... MKAY`) is accepted as a statement. Generic bare expressions and bare method-call statements are not fully opened as statement forms. |
| Parser conflict profile          | Partial | Grammar currently runs with expected reduce/reduce conflicts (`3`). Functional behavior is tested, but grammar shape still has technical debt.                                           |
| YARN escape surface              | Partial | Implemented escapes include `::`, `:\"`, `:)`, `:>`, `:o`. More advanced string template semantics are not fully implemented (see next section).                                         |

## Not Yet Implemented (or intentionally deferred)

| Area                                                                        | Status                  | Notes                                                                                                            |
|-----------------------------------------------------------------------------|-------------------------|------------------------------------------------------------------------------------------------------------------|
| Full YARN interpolation semantics (for example `:{name}`)                   | Not implemented         | Patterns appear in tier-2 corpus examples, but current lexer/runtime do not evaluate interpolation placeholders. |
| Extended YARN codepoint/escape variants beyond current set                  | Not implemented         | Current lexer escape handling is limited to a core subset.                                                       |
| `WAZZUP` / `BUHBYE` variable-block delimiters                               | Out of spec             | Not present in archived 1.1 nor official 1.2/1.3 specs; treat as non-normative dialect syntax from third-party implementations. |
| 1.4 library/import model (`CAN HAS ...?`, library-qualified extension APIs) | Deferred / Out of scope | See `corpus/research/SPEC_1_4_EXTENSION_STATUS.md`.                                                              |

## Why this snapshot is reliable

- It is based on current parser/runtime implementation plus tests/fixtures in-tree.
- Unsupported ops are now surfaced early (compile-stage) and mapped into structured `unsupported` results.
- The test suite is green at snapshot time (`286 tests passed`).

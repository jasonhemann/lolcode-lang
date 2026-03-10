# LOLCODE 1.3 Implementation Status (Project Snapshot)

Last updated: 2026-03-05

## Scope and Policy

- Normative target is strict upstream 1.3 only.
- Parser rejects non-1.3 headers (`HAI 1.2`, `HAI 1.4`, bare `HAI`, metadata/codename headers).
- Extension syntax/features are intentionally unsupported in core mode.
- This is code-and-test grounded status, not a formal proof artifact.

## Coverage Summary

- Conformance fixtures in `tests/spec/fixtures/manifest.rktd`: `16`
- Current full suite result: `405 tests passed` (`./scripts/test_racket.sh`)
- Parser conflict profile: `SR=21`, `RR=0`
- Traceability matrix summary (`./scripts/check_spec_traceability.sh`):
  - `implemented: 58`
  - `partial: 1`
  - `known-divergence: 1`
  - `total: 60`
- Clause traceability artifacts live under:
  - `spec/upstream/`
  - `spec/traceability/spec-1.3-matrix.rktd`
  - `spec/traceability/spec-1.3-clause-index.tsv`
  - `scripts/check_spec_traceability.rkt`, `scripts/extract_spec_clauses.rkt`

## Implemented (Strict 1.3)

| Area                                                                                                                                              | Status      | Evidence                                                                                         |
|---------------------------------------------------------------------------------------------------------------------------------------------------|-------------|--------------------------------------------------------------------------------------------------|
| Program envelope (`HAI ... KTHXBYE`)                                                                                                              | Implemented | `src/lolcode/parser.rkt`                                                                         |
| Declarations/assignment (`I HAS [A/AN]?`, `R`, typed defaults)                                                                                   | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                              |
| Input/output (`GIMMEH`, `VISIBLE`, `VISIBLE ... !`)                                                                                               | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, `tests/spec/runtime-core-test.rkt`         |
| Arithmetic and logic core ops (`SUM`, `DIFF`, `PRODUKT`, `QUOSHUNT`, `MOD`, `BIGGR`, `SMALLR`, `BOTH/EITHER/WON`, `NOT`, `BOTH SAEM`, `DIFFRINT`) | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, `src/lolcode/runtime/operators.rkt`        |
| Strict operator spelling for core ops (reject aliases like `DIFFERENCE`, `QOUSHUNT`)                                                            | Implemented | `tests/spec/parse-negative-test.rkt`, `tests/spec/spec-audit/edge-cases-test.rkt`               |
| Variadics (`SMOOSH`, `ALL OF`, `ANY OF`)                                                                                                          | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                              |
| Casting (`MAEK`, `IS NOW A`)                                                                                                                      | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`                                              |
| Control flow (`O RLY?`, `MEBBE`, `NO WAI`, `WTF?`, `OMG`, `OMGWTF`, `GTFO`)                                                                     | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                                    |
| Loops (`IM IN YR` / `IM OUTTA YR`, `UPPIN`/`NERFIN`, `TIL`/`WILE`)                                                                                | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                                    |
| Functions/methods (`HOW IZ I`, `I IZ`, `FOUND YR`)                                                                                                | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                                    |
| Objects (`O HAI IM`, `IM LIEK`, slots via `HAS` / `HAS A` / `HAS AN` / `'Z`, methods)                                                            | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, `src/lolcode/runtime/value.rkt`, fixtures  |
| Dynamic identifiers (`SRS`) for declaration, target, slot, function/method names                                                                 | Implemented | `src/lolcode/parser.rkt`, `src/lolcode/runtime.rkt`, fixtures                                    |
| Comments and line continuation (`BTW`, `OBTW`/`TLDR`, `...`, `…`)                                                                                 | Implemented | `src/lolcode/lexer.rkt`, parse-negative/runtime tests                                            |
| Numeric literal validation (reject malformed forms like `1..23`, `- 123`)                                                                        | Implemented | `src/lolcode/lexer.rkt`, `tests/spec/parse-negative-test.rkt`                                    |
| Unicode string escapes (`:(hex)`, `:[NORMATIVE NAME]`, `:{var}`)                                                                                 | Implemented | `src/lolcode/lexer.rkt`, `tests/spec/runtime-core-test.rkt`, `tests/spec/parse-negative-test.rkt` |

## Key Strictness Decisions (2026-03-05)

- `CAN HAS ...` removed from parser/runtime as non-spec extension.
- `STRING'Z ...`/`STDIO` runtime extension path removed.
- `SRS` dynamic alias side-channel bindings removed from function call frames.
- Parser no longer allows accidental same-line statement concatenation without separators.
- Unicode normative-name escapes now require full Racket `codepoint` name data (no partial hardcoded fallback map).

## Out-of-Scope Extension Patterns Seen In Corpora

- `CAN HAS <LIB>?` imports (`STRING`, `STDIO`, `SOCKS`, `STDLIB`, etc.).
- Library-qualified call conventions (`STRING'Z LEN`, `STRING'Z AT`, related namespace forms).
- Dialect-only syntax (`WAZZUP` / `BUHBYE`).
- Misspelled operator families accepted by permissive implementations (`DIFFERENCE`, `QOUSHUNT`, etc.).
- Relaxed cast behavior in some implementations/corpora that accepts non-strict numeric YARNs.

These are documented for corpus triage but intentionally rejected for strict 1.3 conformance.

## Known Strict-Core Gaps (Tracked)

1. `TYPE` literal domain is partial (`spec line 259`):
   - Bare type words like `NUMBR` are currently parsed as identifiers rather than TYPE literals.
   - Evidence: `tests/spec/spec-audit/known-gaps-failing-test.rkt` (`KNOWN-PARTIAL` case).
2. Object-function `IT` lookup diverges (`spec line 672`):
   - Spec text says object-function `IT` lookup is from global namespace.
   - Current implementation initializes method-local `IT` in call frames.
   - Evidence: `tests/spec/spec-audit/known-gaps-failing-test.rkt` (`KNOWN-DIVERGENCE` case).

## External Bug/Drift Patterns Worth Tracking

- Implementations silently accepting non-spec headers or defaulting missing version tags.
- Implementations accepting relaxed YARN-to-number casts contrary to strict lexical numeric forms.
- Implementations diverging on parser strictness for operator spelling and statement delimitation.
- Extension-heavy repos labeling behavior as "1.3" despite depending on non-spec import/library features.

## Prioritized Next Fixes

1. Reduce parser SR conflicts further while preserving current strict behavior.
2. Improve strict parse/runtime diagnostics for common corpus drift classes (especially extension-like syntax).
3. Continue external issue/PR evidence harvesting as GitHub auth/network allows; queue now includes explicit `core-1.2/1.3` vs `extension` scope labels.

## Corpus Reclassification Snapshot (2026-03-05)

- Tier2 files: `223`; likely programs: `184`; non-programs: `39`.
- In-scope strict-1.3 files: `13`; parse-ok: `10`; eval-ok: `9`.
- Remaining in-scope corpus failures are currently corpus-input issues, not additional confirmed core-implementation gaps:
  - `DIFFRENCE`/`DIFFERENCE` operator misspellings (strict parse rejection).
  - `//` comment syntax (invalid identifier in strict parser).
  - One runtime `unknown slot` case in external corpus code relying on non-portable behavior.

Spec-audit review does still track the two strict-core gaps listed above.

## Audit Regression Tests

- `tests/spec/spec-audit/known-gaps-failing-test.rkt` and `tests/spec/spec-audit/edge-cases-test.rkt` remain the core guardrails for previously-missed semantics.
- Parse negatives in `tests/spec/parse-negative-test.rkt` now include strict rejection of extension syntax.

## Why this snapshot is reliable

- Grounded in current in-tree parser/runtime behavior and green tests.
- Strict-vs-extension boundary is now explicit in code (not only in docs).
- Unsupported behavior is rejected consistently at parse/runtime boundary rather than partially emulated.

# Implementation Oracle Matrix

As of **February 28, 2026** (UTC), this matrix ranks implementation repos from the PDF-derived candidate set by differential-testing usefulness.

Primary sources used:
- `corpus/tier2/CANDIDATE_REPOS.tsv`
- `corpus/research/availability/availability.json`
- `corpus/research/lci_issues/issues.json`
- Live GitHub API metadata snapshots collected on 2026-02-28

Scoring intent:
- **Oracle usefulness** estimates value as a *secondary* behavioral oracle (spec is still authoritative).
- **Issue/PR depth** favors repos with actionable behavior reports, not build/system-only tickets.
- **Bugfix signal (30 commits)** is a rough indicator from commit headlines containing terms like `fix`, `bug`, `crash`, `regress`, `issue`.

## Ranked Matrix

| Rank | Repo | Kind | Last Push (UTC) | Issues (Open/Closed) | PRs (Open/Closed) | Bugfix Signal (Last 30) | Oracle Usefulness | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `justinmeza/lci` | interpreter | 2026-02-24 | 38 / 21 | 6 / 21 | 10 | Very High | Rich issue/PR history with many language-semantics reports; still non-authoritative due known divergence from spec. |
| 2 | `NullDev/I-HAS-JS` | interpreter | 2023-03-01 | 1 / 0 | 0 / 3 | 0 | Medium | Independent runtime stack; limited issue depth but some PR history. |
| 3 | `JasonBock/LOLCode.net` | compiler/interpreter | 2021-03-21 | 5 / 4 | 0 / 0 | 0 | Medium | Has issue history (mostly tooling/architecture); useful for parser/frontend contrasts. |
| 4 | `jD91mZM2/rust-lci` | interpreter | 2018-08-01 | 0 / 0 | 0 / 0 | 7 | Medium | No tracker depth, but strong fix-heavy commit history with semantic hints (recursion/scope/panics). |
| 5 | `YS-L/hlci` | interpreter | 2017-02-05 | 0 / 0 | 0 / 0 | 5 | Medium | No issues/PRs, but meaningful fix commits on casting, loops, parser edge cases. |
| 6 | `jpcarreon/loco` | interpreter | 2022-06-02 | 0 / 0 | 0 / 0 | 2 | Low-Medium | No tracker, but commit history has parser/runtime crash and tokenization fixes. |
| 7 | `DvaeFroot/cmsc124-lolcode-interpreter` | interpreter | 2022-12-11 | 0 / 0 | 0 / 74 | 15 | Low-Medium | High PR volume and fix language in commits, but mostly course-project cadence/quality; use selectively. |
| 8 | `SADAsuncion/LOLCodeInterpreter` | interpreter | 2024-01-08 | 0 / 0 | 0 / 0 | 12 | Low-Medium | No tracker depth; commit log includes semantic fix terms (comparison/visible/function syntax). |
| 9 | `eggyknap/pllolcode` | extension | 2014-02-20 | 1 / 0 | 0 / 0 | 1 | Low | Not a full general interpreter; extension-oriented and stale. |
| 10 | `qoobaa/lol` | interpreter | 2009-10-20 | 0 / 1 | 0 / 0 | 0 | Low | Archived and old; useful mostly as historical reference. |

## Seeded Top 10 External Regression Targets

These are external bug reports/bugfix references to convert into minimal repro fixtures in this repository.

| Priority | Source | Reference | Topic | Proposed Fixture ID | Why It Matters |
| --- | --- | --- | --- | --- | --- |
| P1 | `lci` issue | [#71](https://github.com/justinmeza/lci/issues/71) | Loop variable creation/initialization behavior | `ext_lci_71_loop_var_scope` | Loop-scope semantics frequently break portability and program meaning. |
| P1 | `lci` issue | [#65](https://github.com/justinmeza/lci/issues/65) | `LIEK` deep-copy semantics | `ext_lci_65_liek_copy` | Object/value copying affects aliasing and closure-like object patterns. |
| P1 | `lci` issue | [#60](https://github.com/justinmeza/lci/issues/60) | Function mutating outer scope | `ext_lci_60_fn_scope_isolation` | Scope isolation is essential for reliable higher-order encodings. |
| P1 | `lci` issue | [#59](https://github.com/justinmeza/lci/issues/59) | EOL vs `MKAY` in variadic call parsing | `ext_lci_59_variadic_eol` | Parser edge case likely to affect large multi-line codebases. |
| P1 | `lci` issue | [#58](https://github.com/justinmeza/lci/issues/58) | `NUMBAR` + line continuation behavior | `ext_lci_58_numbar_line_cont` | Numeric parsing corner case with real runtime impact. |
| P1 | `lci` issue | [#56](https://github.com/justinmeza/lci/issues/56) | Colon + quote string escape interaction | `ext_lci_56_string_escape_colon_quote` | Lexer correctness for strings is foundational and error-prone. |
| P2 | `rust-lci` commit | [a81f263](https://github.com/jD91mZM2/rust-lci/commit/a81f263ea5ca1653442a17c7806c4bb82cb9372e) | Function recursion fix | `ext_rust_lci_recursion` | Recursion correctness is required for miniKanren-style interpreters. |
| P2 | `hlci` commit | [a5eb34c](https://github.com/YS-L/hlci/commit/a5eb34c92bde676377632cb1feb6f1b8cf426d10) | `NOOB`/`YARN` casting + negative float behavior | `ext_hlci_casting_numbar` | Casting/coercion drift causes subtle cross-impl divergence. |
| P2 | `loco` commit | [6f2a595](https://github.com/jpcarreon/loco/commit/6f2a59592be2e86475eff9be228bdbab6c21b5d5) | Comma tokenization interfering with `YARN` parsing | `ext_loco_comma_yarn_lex` | Comma/newline dual semantics are core LOLCODE syntax risk. |
| P3 | `cmsc124-lolcode-interpreter` PR | [#61](https://github.com/DvaeFroot/cmsc124-lolcode-interpreter/pull/61) | Newline skipping before `HAI` | `ext_cmsc124_preamble_newlines` | Startup/preamble tolerance differs across implementations; good parser-hardening case. |

## Immediate Conversion Plan

1. Add one fixture + expected output/error per target in `tests/spec/fixtures/programs/`.
2. Tag each fixture in `manifest.rktd` with `source-ref` as external reference URL + short descriptor.
3. Record result classification in `corpus/research/lci_issues/TRIAGE.md` as one of:
   - `fixed-here`
   - `known-divergence`
   - `spec-ambiguous`
4. Keep spec conformance authoritative when external references conflict.

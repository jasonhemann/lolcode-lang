# lci Divergence Triage

Purpose: track known/suspected `lci` behavior gaps so we can proactively build regression tests and avoid reproducing them.

Scope rule:
- `lolcode-spec` 1.2/1.3 remains the primary oracle.
- `lci` issue/PR behavior is treated as secondary evidence only.

## Workflow

1. Sync issue/PR data:
   - `./scripts/sync_lci_issue_backlog.sh`
2. Pick a candidate issue/PR.
3. Map to spec section(s).
4. Write a minimal repro program in `tests/spec/fixtures/programs/`.
5. Add expected output/error in manifest + tests.
6. Mark result as:
   - `fixed-here`
   - `matches-lci`
   - `known-divergence`
   - `spec-ambiguous`

## Seed Candidates (from lci tracker)

These are high-value candidates to convert into explicit regression tests.

| Source | Type | Status in lci | Topic | Spec Area | Local Status | Link |
|---|---|---|---|---|---|---|
| `lci#71` | Issue | Open | loops always create/zero variable | loop variable semantics | `todo` | [#71](https://github.com/justinmeza/lci/issues/71) |
| `lci#65` | Issue | Open | `LIEK` not deep copy | object/copy semantics | `todo` | [#65](https://github.com/justinmeza/lci/issues/65) |
| `lci#62` | Issue | Open | `BTW` on same line as `TLDR` | comment lexical semantics | `todo` | [#62](https://github.com/justinmeza/lci/issues/62) |
| `lci#60` | Issue | Open | function mutates outer scope | function scope semantics | `todo` | [#60](https://github.com/justinmeza/lci/issues/60) |
| `lci#59` | Issue | Open | `...` EOL not replacing `MKAY` for variadics | line continuation + call syntax | `todo` | [#59](https://github.com/justinmeza/lci/issues/59) |
| `lci#58` | Issue | Open | `NUMBAR` with line continuation | numeric lex/parse edge cases | `todo` | [#58](https://github.com/justinmeza/lci/issues/58) |
| `lci#57` | Issue | Open | octal `NUMBR` sign behavior | numeric literal semantics | `todo` | [#57](https://github.com/justinmeza/lci/issues/57) |
| `lci#56` | Issue | Open | colon/quote in strings | string escape lexical semantics | `todo` | [#56](https://github.com/justinmeza/lci/issues/56) |
| `lci#47` | Issue | Open | crash around implicit `IT` use | runtime safety + `IT` semantics | `todo` | [#47](https://github.com/justinmeza/lci/issues/47) |
| `lci#52` | PR | Open | fix loop variable creation behavior | loop variable semantics | `todo` | [#52](https://github.com/justinmeza/lci/pull/52) |
| `lci#50` | PR | Open | fix double-free of implicit variable | runtime memory safety | `todo` | [#50](https://github.com/justinmeza/lci/pull/50) |
| `lci#6` | PR | Open | `GIMMEH` optional modes | input operator extensions | `todo` | [#6](https://github.com/justinmeza/lci/pull/6) |
| `lci#17` | Issue | Closed | behavior referenced in external corpus (`loleuler`) | numeric/runtime edge case | `todo` | [#17](https://github.com/justinmeza/lci/issues/17) |

## Notes

- As of February 28, 2026, GitHub list pages for `justinmeza/lci` showed both open and closed issue/PR sets. We should treat list counts as mutable and refresh before milestone reports.
- Some tracker items may describe `future`/extension behavior; those must be tagged `out-of-spec` unless they map cleanly to 1.2/1.3.

# Spec 1.3 Confluence Matrix

Date: 2026-03-05

Purpose: track clause intersections where bugs tend to emerge only when two (or more) features interact.

## Initial Prioritized Intersections

| Intersection ID | Clauses | Risk | Tests |
| --- | --- | --- | --- |
| `flow.return × loops` | 552, 564, 586 | high | `confluence: FOUND YR inside loop exits function (not just loop)`; `confluence: FOUND YR remains invalid outside function even inside loop` |
| `lexical-scope × loop-local-updater × function-call` | 101, 564, 602 | high | `confluence: loop updater shadow does not dynamically capture function lookup`; `confluence: function cannot resolve loop-local updater name by dynamic scope` |
| `methods × GTFO-validity × loops` | 552, 564, 586, 612 | high | `confluence: GTFO in method loop breaks loop and method continues`; `confluence: GTFO in method body returns NOOB`; `confluence: GTFO in object definition body remains invalid` |
| `methods × switch × return` | 486, 586, 612 | high | `confluence: FOUND YR from method-local WTF? escapes full method`; `confluence: FOUND YR in object definition body remains invalid` |

## Test Location

- `tests/spec/spec-audit/confluence-intersections-test.rkt`

## Notes

- These cases are intentionally paired as `should-pass` and `should-fail` checks.
- The goal is to catch control/scope regressions that unit tests for isolated features miss.

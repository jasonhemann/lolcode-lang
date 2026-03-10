# Relaxed YARN->NUMBR/NUMBAR Cast Behavior (Strict 1.3 Decision)

Date: 2026-03-02

## Question

Do LOLCODE 1.2/1.3 specs require relaxed numeric parsing for explicit casts from
`YARN` (for example leading whitespace tolerance, stop-at-first-nondigit, octal
or hex prefixes)?

## Primary Sources

- Official 1.2 spec:
  <https://github.com/justinmeza/lolcode-spec/blob/master/v1.2/lolcode-spec-v1.2.md>
- Official 1.3 spec:
  <https://github.com/justinmeza/lolcode-spec/blob/master/v1.3/lolcode-spec-v1.3.md>
- LCI corpus tests that encode relaxed behavior expectations:
  - `corpus/tier1/lci/files/test/1.3-Tests/7-Operators/17-ExplicitCast/3-ToInteger/5-FromString/4-RelaxedNumbers/test.lol`
  - `corpus/tier1/lci/files/test/1.3-Tests/7-Operators/17-ExplicitCast/4-ToFloat/5-FromString/4-RelaxedNumbers/test.lol`

## Findings

- 1.2 and 1.3 cast text specifies that `YARN` converts to numeric only when the
  string is a valid numeric literal; otherwise it errors.
- The relaxed cases above are documented in LCI test comments but are not
  normative spec language.

## Project policy

- In strict 1.3 mode, relaxed partial parsing is intentionally rejected.
- The listed `RelaxedNumbers` corpus files are treated as intentional
  non-conformance to this project target, not implementation bugs.

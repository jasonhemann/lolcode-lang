# Tier2 Classified Eval Snapshot

Generated: `Monday, March 2nd, 2026 3:02:07pm`

- Corpus root: `corpus/tier2`
- Timeout seconds: `2.0`

## Totals

- Files: `223`
- Likely programs: `184`
- Non-programs: `39`

### Classification Reasons

- `leading-hai`: `184`
- `no-hai-header`: `26`
- `empty-or-comments-only`: `13`

### Outcome Counts (All Files)

- `parse-error`: `166`
- `non-program`: `39`
- `ok`: `11`
- `lex-error`: `6`
- `runtime-error`: `1`

### Outcome Counts (Likely Programs)

- `parse-error`: `166`
- `ok`: `11`
- `lex-error`: `6`
- `runtime-error`: `1`

### Top Messages (Likely Programs)

- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`: `95`
- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`: `41`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 4`: `9`
- `lex-source: unterminated string literal at line 6, col 27`: `3`
- `parse-source: syntax error: unexpected ID ("OPEN") at line 3, col 5`: `3`
- `parse-source: unsupported version: 1.4 (this implementation only accepts HAI 1.3)`: `3`
- `lex-source: unterminated string literal at line 8, col 31`: `2`
- `parse-source: syntax error: unexpected ID ("VAR!!1") at line 3, col 8`: `2`
- `parse-source: syntax error: unexpected STRING ("Dear curious test reader") at line 1, col 5`: `2`
- `parse-source: syntax error: unexpected ID ("VAR!!1") at line 6, col 6`: `1`
- `parse-source: syntax error: unexpected ID ("TODO") at line 264, col 12`: `1`
- `parse-source: syntax error: unexpected GTFO at line 35, col 5`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 4, col 4`: `1`
- `lex-source: unterminated string literal at line 8, col 27`: `1`
- `parse-source: syntax error: unexpected VISIBLE at line 150, col 25`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 47`: `1`
- `parse-source: syntax error: unexpected STRING ("This iz teh test") at line 1, col 5`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 5`: `1`
- `parse-source: syntax error: unexpected LIEK at line 37, col 20`: `1`
- `parse-source: syntax error: unexpected STRING ("Dear reader") at line 1, col 5`: `1`
- `parse-source: syntax error: unexpected ID ("ME") at line 241, col 17`: `1`
- `run-program: unknown identifier: MEMLIMIT`: `1`

## Sample Error Rows

- `corpus/tier2/aurasphere-ftpd-lol/files/ftpd.lol` => `parse-error` (`parse-source: syntax error: unexpected VISIBLE at line 150, col 25`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/checkerboard/bonus_features.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/01_variables.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 2, col 4`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/02_gimmeh.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/03_arith.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/04_smoosh_assign.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/05_bool.lol` => `lex-error` (`lex-source: unterminated string literal at line 8, col 31`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/06_comparison.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/07_ifelse.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/08_switch.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/09_loops.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/10_functions.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/01_variables.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 2, col 4`)
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/02_gimmeh.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/03_arith.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/04_smoosh_assign.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/05_bool.lol` => `lex-error` (`lex-source: unterminated string literal at line 6, col 27`)
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/06_comparison.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/07_ifelse.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/08_switch.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)


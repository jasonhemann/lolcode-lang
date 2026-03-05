# Tier2 Classified Eval Snapshot

Generated: `Wednesday, March 4th, 2026 7:13:25pm`

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
- `ok`: `9`
- `lex-error`: `7`
- `timeout`: `1`
- `runtime-error`: `1`

### Outcome Counts (Likely Programs)

- `parse-error`: `166`
- `ok`: `9`
- `lex-error`: `7`
- `timeout`: `1`
- `runtime-error`: `1`

### Top Messages (Likely Programs)

- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`: `94`
- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`: `39`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 4`: `9`
- `lex-source: unterminated string literal at line 6, col 27`: `3`
- `parse-source: syntax error: unexpected ID ("AND") at line 77, col 34`: `2`
- `parse-source: syntax error: unexpected ID ("NOES") at line 6, col 7`: `2`
- `parse-source: syntax error: unexpected IZ at line 5, col 5`: `2`
- `parse-source: unsupported version: 1.4 (this implementation only accepts HAI 1.3)`: `2`
- `lex-source: unterminated string literal at line 8, col 31`: `2`
- `parse-source: syntax error: unexpected STRING ("Dear curious test reader") at line 1, col 5`: `2`
- `parse-source: syntax error: unexpected NEWLINE at line 4, col 4`: `1`
- `lex-source: unterminated string literal at line 8, col 27`: `1`
- `parse-source: syntax error: unexpected OF at line 30, col 23`: `1`
- `parse-source: syntax error: unexpected OF at line 13, col 12`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 47`: `1`
- `run-program: unknown identifier: //`: `1`
- `parse-source: syntax error: unexpected OF at line 49, col 37`: `1`
- `parse-source: syntax error: unexpected OF at line 12, col 19`: `1`
- `parse-source: syntax error: unexpected ID ("AND") at line 166, col 83`: `1`
- `parse-source: syntax error: unexpected IZ at line 8, col 3`: `1`
- `parse-source: syntax error: unexpected ID ("NOES") at line 6, col 5`: `1`
- `parse-source: syntax error: unexpected STRING ("Dear reader") at line 1, col 5`: `1`
- `parse-source: syntax error: unexpected STRING ("This iz teh test") at line 1, col 5`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 5`: `1`
- `evaluation timed out after 2.0 seconds`: `1`
- `parse-source: syntax error: unexpected OF at line 30, col 33`: `1`
- `lex-source: line continuation marker must be at end of line at line 19, col 48`: `1`
- `parse-source: syntax error: unexpected OF at line 8, col 27`: `1`

## Sample Error Rows

- `corpus/tier2/aurasphere-ftpd-lol/files/ftpd.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("AND") at line 166, col 83`)
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


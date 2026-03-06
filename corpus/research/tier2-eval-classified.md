# Tier2 Classified Eval Snapshot

Generated: `Friday, March 6th, 2026 8:41:58am`

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

- `parse-error`: `167`
- `non-program`: `39`
- `ok`: `9`
- `lex-error`: `7`
- `runtime-error`: `1`

### Outcome Counts (Likely Programs)

- `parse-error`: `167`
- `ok`: `9`
- `lex-error`: `7`
- `runtime-error`: `1`

### Top Messages (Likely Programs)

- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`: `94`
- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`: `28`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 4`: `9`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 9`: `6`
- `lex-source: unterminated string literal at line 6, col 27`: `3`
- `lex-source: unterminated string literal at line 8, col 31`: `2`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 11, col 13`: `2`
- `parse-source: syntax error: unexpected ID ("VAR!!1") at line 3, col 8`: `2`
- `parse-source: syntax error: unexpected ID ("RAYLIB?") at line 2, col 9`: `2`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "Dear curious test reader")))) at line 1, col 5`: `2`
- `parse-source: syntax error: unexpected MOD at line 13, col 42`: `1`
- `parse-source: syntax error: unexpected I at line 24, col 25`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "This iz teh test")))) at line 1, col 5`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 4, col 4`: `1`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 26, col 17`: `1`
- `lex-source: unterminated string literal at line 8, col 27`: `1`
- `run-program: unknown slot: 7288`: `1`
- `parse-source: syntax error: unexpected OF at line 30, col 23`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "Dear reader")))) at line 1, col 5`: `1`
- `parse-source: syntax error: unexpected OF at line 13, col 12`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 47`: `1`
- `parse-source: syntax error: unexpected OF at line 30, col 33`: `1`
- `parse-source: invalid identifier syntax: "//"`: `1`
- `parse-source: syntax error: unexpected OF at line 12, col 19`: `1`
- `parse-source: syntax error: unexpected SUM at line 3, col 13`: `1`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 11`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text " years old")))) at line 34, col 34`: `1`
- `parse-source: syntax error: unexpected ID ("STRING?") at line 2, col 9`: `1`
- `parse-source: syntax error: unexpected DIFFRINT at line 42, col 13`: `1`
- `parse-source: syntax error: unexpected DIFFRINT at line 22, col 13`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 5`: `1`
- `lex-source: line continuation marker must be at end of line at line 19, col 48`: `1`
- `parse-source: syntax error: unexpected DIFFRINT at line 17, col 27`: `1`
- `parse-source: syntax error: unexpected OF at line 49, col 37`: `1`
- `parse-source: syntax error: unexpected BOTH at line 5, col 43`: `1`

## Sample Error Rows

- `corpus/tier2/aurasphere-ftpd-lol/files/ftpd.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("STDIO?") at line 26, col 17`)
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


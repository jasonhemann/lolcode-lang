# Tier2 Classified Eval Snapshot

Generated: `Monday, March 2nd, 2026 3:04:30pm`

- Corpus root: `corpus/research/promoted-1_3-tier2-fresh`
- Timeout seconds: `2.0`

## Totals

- Files: `111`
- Likely programs: `111`
- Non-programs: `0`

### Classification Reasons

- `leading-hai`: `111`

### Outcome Counts (All Files)

- `ok`: `57`
- `parse-error`: `45`
- `lex-error`: `6`
- `runtime-error`: `2`
- `timeout`: `1`

### Outcome Counts (Likely Programs)

- `ok`: `57`
- `parse-error`: `45`
- `lex-error`: `6`
- `runtime-error`: `2`
- `timeout`: `1`

### Top Messages (Likely Programs)

- `parse-source: syntax error: unexpected I at line 5, col 9`: `9`
- `parse-source: syntax error: unexpected I at line 4, col 17`: `9`
- `parse-source: syntax error: unexpected I at line 4, col 9`: `4`
- `parse-source: syntax error: unexpected OF at line 10, col 31`: `4`
- `parse-source: syntax error: unexpected I at line 6, col 9`: `3`
- `lex-source: unterminated string literal at line 7, col 27`: `3`
- `lex-source: unterminated string literal at line 9, col 31`: `2`
- `parse-source: syntax error: unexpected NEWLINE at line 20, col 55`: `1`
- `lex-source: unterminated string literal at line 9, col 27`: `1`
- `parse-source: syntax error: unexpected VISIBLE at line 4, col 9`: `1`
- `parse-source: syntax error: unexpected I at line 19, col 9`: `1`
- `parse-source: syntax error: unexpected ITZ at line 14, col 1`: `1`
- `parse-source: syntax error: unexpected BANG at line 14, col 51`: `1`
- `parse-source: syntax error: unexpected ID ("DUZ") at line 16, col 5`: `1`
- `parse-source: syntax error: unexpected ID ("result") at line 14, col 62`: `1`
- `/: division by zero`: `1`
- `parse-source: syntax error: unexpected GIMMEH at line 17, col 17`: `1`
- `parse-source: syntax error: unexpected I at line 123, col 9`: `1`
- `parse-source: syntax error: unexpected ID ("y") at line 4, col 23`: `1`
- `parse-source: syntax error: unexpected IZ at line 9, col 1`: `1`
- `run-program: unknown identifier: ++`: `1`
- `evaluation timed out after 2.0 seconds`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 7, col 63`: `1`
- `parse-source: syntax error: unexpected VISIBLE at line 4, col 5`: `1`
- `parse-source: syntax error: unexpected OF at line 26, col 50`: `1`
- `parse-source: syntax error: unexpected STRING ("world!") at line 6, col 9`: `1`
- `parse-source: syntax error: unexpected ID ("VAR") at line 8, col 5`: `1`

## Sample Error Rows

- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/checkerboard/bonus_features.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 123, col 9`)
- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/final/01_variables.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 6, col 9`)
- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/final/02_gimmeh.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 5, col 9`)
- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/final/03_arith.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 5, col 9`)
- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/final/04_smoosh_assign.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 5, col 9`)
- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/final/05_bool.lol` => `lex-error` (`lex-source: unterminated string literal at line 9, col 31`)
- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/final/06_comparison.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 4, col 9`)
- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/final/07_ifelse.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 4, col 17`)
- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/final/08_switch.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 4, col 17`)
- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/final/09_loops.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 4, col 17`)
- `corpus/research/promoted-1_3-tier2-fresh/bernardjezua-lolcode-interpreter/files/testcases/final/10_functions.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 19, col 9`)
- `corpus/research/promoted-1_3-tier2-fresh/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/03_arith.lol` => `parse-error` (`parse-source: syntax error: unexpected OF at line 10, col 31`)
- `corpus/research/promoted-1_3-tier2-fresh/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/05_bool.lol` => `lex-error` (`lex-source: unterminated string literal at line 7, col 27`)
- `corpus/research/promoted-1_3-tier2-fresh/garthendrich-lolcode-interpreter/files/sample_codes/03_arith.lol` => `parse-error` (`parse-source: syntax error: unexpected OF at line 10, col 31`)
- `corpus/research/promoted-1_3-tier2-fresh/garthendrich-lolcode-interpreter/files/sample_codes/05_bool.lol` => `lex-error` (`lex-source: unterminated string literal at line 7, col 27`)
- `corpus/research/promoted-1_3-tier2-fresh/loco/files/Samples/diamond_swan.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 20, col 55`)
- `corpus/research/promoted-1_3-tier2-fresh/loco/files/Samples/even_nums.lol` => `parse-error` (`parse-source: syntax error: unexpected BANG at line 14, col 51`)
- `corpus/research/promoted-1_3-tier2-fresh/loco/files/Samples/perfect_nums.lol` => `timeout` (`evaluation timed out after 2.0 seconds`)
- `corpus/research/promoted-1_3-tier2-fresh/lol-ruby/files/examples/ifthenelse.lol` => `parse-error` (`parse-source: syntax error: unexpected IZ at line 9, col 1`)
- `corpus/research/promoted-1_3-tier2-fresh/lol-ruby/files/examples/loops.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("VAR") at line 8, col 5`)


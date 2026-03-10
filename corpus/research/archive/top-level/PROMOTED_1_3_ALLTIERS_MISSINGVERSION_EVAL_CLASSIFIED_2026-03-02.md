# Tier2 Classified Eval Snapshot

Generated: `Monday, March 2nd, 2026 3:06:57pm`

- Corpus root: `corpus/research/promoted-1_3-alltiers-missingversion`
- Timeout seconds: `2.0`

## Totals

- Files: `121`
- Likely programs: `121`
- Non-programs: `0`

### Classification Reasons

- `leading-hai`: `121`

### Outcome Counts (All Files)

- `parse-error`: `61`
- `ok`: `48`
- `lex-error`: `9`
- `runtime-error`: `2`
- `timeout`: `1`

### Outcome Counts (Likely Programs)

- `parse-error`: `61`
- `ok`: `48`
- `lex-error`: `9`
- `runtime-error`: `2`
- `timeout`: `1`

### Top Messages (Likely Programs)

- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`: `11`
- `parse-source: syntax error: unexpected I at line 5, col 9`: `9`
- `parse-source: syntax error: unexpected I at line 4, col 17`: `9`
- `parse-source: syntax error: unexpected I at line 4, col 9`: `4`
- `parse-source: syntax error: unexpected I at line 6, col 9`: `3`
- `lex-source: unterminated string literal at line 9, col 31`: `2`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 4`: `2`
- `lex-source: unterminated string literal at line 6, col 27`: `2`
- `parse-source: syntax error: unexpected STRING ("file.lol") at line 5, col 11`: `2`
- `parse-source: syntax error: unexpected OF at line 10, col 31`: `2`
- `parse-source: syntax error: unexpected ID ("VAR") at line 7, col 9`: `2`
- `parse-source: syntax error: unexpected NEWLINE at line 20, col 55`: `1`
- `parse-source: syntax error: unexpected ID ("DUZ") at line 3, col 5`: `1`
- `lex-source: unterminated string literal at line 7, col 27`: `1`
- `lex-source: unterminated string literal at line 9, col 27`: `1`
- `parse-source: syntax error: unexpected VISIBLE at line 4, col 9`: `1`
- `parse-source: syntax error: unexpected ID ("IPTR") at line 9, col 5`: `1`
- `lex-source: unterminated string literal at line 7, col 17`: `1`
- `parse-source: syntax error: unexpected VISIBLE at line 4, col 5`: `1`
- `parse-source: syntax error: unexpected I at line 19, col 9`: `1`
- `parse-source: syntax error: unexpected ITZ at line 14, col 1`: `1`
- `parse-source: syntax error: unexpected BANG at line 14, col 51`: `1`
- `parse-source: syntax error: unexpected STRING ("world!") at line 6, col 9`: `1`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 14, col 25`: `1`
- `parse-source: syntax error: unexpected ID ("DUZ") at line 16, col 5`: `1`
- `parse-source: syntax error: unexpected ID ("result") at line 14, col 62`: `1`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 19, col 41`: `1`
- `/: division by zero`: `1`
- `parse-source: syntax error: unexpected GIMMEH at line 17, col 17`: `1`
- `parse-source: syntax error: unexpected I at line 123, col 9`: `1`
- `parse-source: syntax error: unexpected ID ("y") at line 4, col 23`: `1`
- `parse-source: syntax error: unexpected IZ at line 9, col 1`: `1`
- `run-program: unknown identifier: ++`: `1`
- `evaluation timed out after 2.0 seconds`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 7, col 63`: `1`
- `parse-source: syntax error: unexpected ID ("VAR") at line 8, col 5`: `1`

## Sample Error Rows

- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier1/lolcode-net/files/LOLCode.Compiler.Tests/Samples/INPUT1.lol` => `lex-error` (`lex-source: unterminated string literal at line 7, col 17`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier1/lolcode-net/files/LOLCode.Compiler.Tests/Samples/INPUT2.lol` => `lex-error` (`lex-source: unterminated :(... ) Unicode escape in string literal at line 14, col 25`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier1/lolcode-net/files/LOLCode.Compiler.Tests/Samples/INPUT3.lol` => `lex-error` (`lex-source: unterminated :(... ) Unicode escape in string literal at line 19, col 41`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier1/lolcode-net/files/LOLCode.Compiler.Tests/Samples/fulltest.lol` => `parse-error` (`parse-source: syntax error: unexpected STRING ("file.lol") at line 5, col 11`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier1/lolcode-net/files/LOLCode.Compiler.Tests/Samples/upz1.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("VAR") at line 7, col 9`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier1/lolcode-net/files/LOLCode.Compiler.Tests/Samples/upz2.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("VAR") at line 7, col 9`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier1/lolcode-net/files/LOLCode/bf.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("IPTR") at line 9, col 5`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier1/lolcode-net/files/LOLCode/fulltest.lol` => `parse-error` (`parse-source: syntax error: unexpected STRING ("file.lol") at line 5, col 11`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier1/lolcode-net/files/LOLCode/test.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("DUZ") at line 3, col 5`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/checkerboard/bonus_features.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 123, col 9`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/01_variables.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 6, col 9`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/02_gimmeh.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 5, col 9`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/03_arith.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 5, col 9`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/04_smoosh_assign.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 5, col 9`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/05_bool.lol` => `lex-error` (`lex-source: unterminated string literal at line 9, col 31`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/06_comparison.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 4, col 9`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/07_ifelse.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 4, col 17`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/08_switch.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 4, col 17`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/09_loops.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 4, col 17`)
- `corpus/research/promoted-1_3-alltiers-missingversion/corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/10_functions.lol` => `parse-error` (`parse-source: syntax error: unexpected I at line 19, col 9`)


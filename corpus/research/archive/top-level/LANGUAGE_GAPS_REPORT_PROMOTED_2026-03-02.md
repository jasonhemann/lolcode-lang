# Language Gap Report (Strict 1.3)

Generated: `Monday, March 2nd, 2026 12:18:46pm`

## Totals

- Corpus files: `223`
- In-scope 1.3 files: `133`
- In-scope parse-ok files: `78`
- In-scope eval-ok files: `75`
- Promoted missing-version files: `120`
- Fixture files: `16`
- Fixture parse-ok files: `16`

### Corpus Header Classes (Original)

- `out-of-scope-hai-without-version`: `121`
- `out-of-scope-version-1.2`: `44`
- `non-program-no-leading-hai`: `26`
- `in-scope-1.3`: `13`
- `out-of-scope-version-1.4`: `6`
- `out-of-scope-version-1.0`: `4`
- `non-program-empty-or-comments`: `4`
- `out-of-scope-version-"dear`: `3`
- `out-of-scope-version-btw`: `1`
- `out-of-scope-version-"this`: `1`

### Corpus Header Classes (Effective For Analysis)

- `in-scope-1.3-promoted`: `120`
- `out-of-scope-version-1.2`: `44`
- `non-program-no-leading-hai`: `26`
- `in-scope-1.3`: `13`
- `out-of-scope-version-1.4`: `6`
- `out-of-scope-version-1.0`: `4`
- `non-program-empty-or-comments`: `4`
- `out-of-scope-version-"dear`: `3`
- `out-of-scope-version-btw`: `1`
- `out-of-scope-hai-without-version`: `1`
- `out-of-scope-version-"this`: `1`

### In-Scope 1.3 Status Counts

- `parse-ok`: `78`
- `ok`: `75`
- `parse-error`: `48`
- `lex-error`: `7`
- `runtime-error`: `3`

### In-Scope Lex Errors

- `lex-source: unterminated string literal at line 7, col 27`: `4`
- `lex-source: unterminated string literal at line 9, col 31`: `2`
- `lex-source: unterminated string literal at line 9, col 27`: `1`

### In-Scope Parse Errors

- `parse-source: syntax error: unexpected I at line 5, col 9`: `9`
- `parse-source: syntax error: unexpected I at line 4, col 17`: `9`
- `parse-source: syntax error: unexpected I at line 4, col 9`: `4`
- `parse-source: syntax error: unexpected OF at line 10, col 31`: `4`
- `parse-source: syntax error: unexpected I at line 6, col 9`: `3`
- `parse-source: syntax error: unexpected OF at line 26, col 50`: `2`
- `parse-source: syntax error: unexpected ID ("TODO") at line 264, col 12`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 20, col 55`: `1`
- `parse-source: syntax error: unexpected I at line 19, col 9`: `1`
- `parse-source: syntax error: unexpected ITZ at line 14, col 1`: `1`
- `parse-source: syntax error: unexpected BANG at line 14, col 51`: `1`
- `parse-source: syntax error: unexpected ID ("DUZ") at line 16, col 5`: `1`
- `parse-source: syntax error: unexpected ID ("result") at line 14, col 62`: `1`
- `parse-source: syntax error: unexpected GIMMEH at line 17, col 17`: `1`
- `parse-source: syntax error: unexpected I at line 123, col 9`: `1`
- `parse-source: syntax error: unexpected ID ("y") at line 4, col 23`: `1`
- `parse-source: syntax error: unexpected IZ at line 9, col 1`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 7, col 63`: `1`
- `parse-source: syntax error: unexpected VISIBLE at line 4, col 9`: `1`
- `parse-source: syntax error: unexpected VISIBLE at line 4, col 5`: `1`
- `parse-source: syntax error: unexpected STRING ("world!") at line 6, col 9`: `1`
- `parse-source: syntax error: unexpected OF at line 10, col 29`: `1`
- `parse-source: syntax error: unexpected ID ("VAR") at line 8, col 5`: `1`

### In-Scope Runtime Errors

- `/: division by zero`: `1`
- `run-program: unknown identifier: ++`: `1`
- `run-program: unknown identifier: MEMLIMIT`: `1`

### Missing Statement Forms In In-Scope Corpus

- `stmt-object-def`

### Missing Expression Forms In In-Scope Corpus

- `expr-method-call`

### Missing Binary Operators In In-Scope Corpus

- (none)

### Missing Unary Operators In In-Scope Corpus

- (none)

### Missing Variadic Operators In In-Scope Corpus

- (none)

### Used In Fixtures But Not In In-Scope Corpus (Statements)

- `stmt-object-def`

### Used In Fixtures But Not In In-Scope Corpus (Expressions)

- `expr-method-call`

### In-Scope Branch Shape Counts

- `if-total`: `69`
- `loop-total`: `67`
- `loop-with-update`: `60`
- `loop-with-cond-wile`: `42`
- `if-with-else`: `38`
- `function-total`: `28`
- `loop-with-cond-til`: `17`
- `switch-with-default`: `6`
- `if-with-mebbe`: `6`
- `switch-total`: `6`

### Fixture Branch Shape Counts

- `loop-with-cond-til`: `3`
- `loop-total`: `3`
- `loop-with-update`: `3`
- `object-total`: `2`
- `method-call-total`: `2`
- `if-total`: `2`
- `function-total`: `2`
- `switch-with-default`: `1`
- `if-with-else`: `1`
- `if-with-mebbe`: `1`
- `switch-total`: `1`

### Sample Issues

- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/checkerboard/bonus_features.lol` (`parse`): `parse-source: syntax error: unexpected I at line 123, col 9`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/01_variables.lol` (`parse`): `parse-source: syntax error: unexpected I at line 6, col 9`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/02_gimmeh.lol` (`parse`): `parse-source: syntax error: unexpected I at line 5, col 9`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/03_arith.lol` (`parse`): `parse-source: syntax error: unexpected I at line 5, col 9`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/04_smoosh_assign.lol` (`parse`): `parse-source: syntax error: unexpected I at line 5, col 9`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/05_bool.lol` (`lex`): `lex-source: unterminated string literal at line 9, col 31`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/06_comparison.lol` (`parse`): `parse-source: syntax error: unexpected I at line 4, col 9`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/07_ifelse.lol` (`parse`): `parse-source: syntax error: unexpected I at line 4, col 17`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/08_switch.lol` (`parse`): `parse-source: syntax error: unexpected I at line 4, col 17`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/09_loops.lol` (`parse`): `parse-source: syntax error: unexpected I at line 4, col 17`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/10_functions.lol` (`parse`): `parse-source: syntax error: unexpected I at line 19, col 9`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/03_arith.lol` (`parse`): `parse-source: syntax error: unexpected OF at line 10, col 31`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/05_bool.lol` (`lex`): `lex-source: unterminated string literal at line 7, col 27`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/03_arith.lol` (`parse`): `parse-source: syntax error: unexpected OF at line 10, col 31`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/05_bool.lol` (`lex`): `lex-source: unterminated string literal at line 7, col 27`
- `corpus/tier2/loco/files/Samples/diamond_swan.lol` (`parse`): `parse-source: syntax error: unexpected NEWLINE at line 20, col 55`
- `corpus/tier2/loco/files/Samples/even_nums.lol` (`parse`): `parse-source: syntax error: unexpected BANG at line 14, col 51`
- `corpus/tier2/lol-ruby/files/examples/ifthenelse.lol` (`parse`): `parse-source: syntax error: unexpected IZ at line 9, col 1`
- `corpus/tier2/lol-ruby/files/examples/loops.lol` (`parse`): `parse-source: syntax error: unexpected ID ("VAR") at line 8, col 5`
- `corpus/tier2/lolcode-py-cmsc124/files/project-examples/03_arith.lol` (`parse`): `parse-source: syntax error: unexpected OF at line 10, col 31`
- `corpus/tier2/lolcode-py-cmsc124/files/project-examples/05_bool.lol` (`lex`): `lex-source: unterminated string literal at line 7, col 27`
- `corpus/tier2/lolcode-py-cmsc124/files/project-examples/08_switch.lol` (`parse`): `parse-source: syntax error: unexpected OF at line 26, col 50`
- `corpus/tier2/lolcode-py-sada/files/CMSC_124_testcases/01_variables.lol` (`parse`): `parse-source: syntax error: unexpected I at line 6, col 9`
- `corpus/tier2/lolcode-py-sada/files/CMSC_124_testcases/02_gimmeh.lol` (`parse`): `parse-source: syntax error: unexpected I at line 5, col 9`
- `corpus/tier2/lolcode-py-sada/files/CMSC_124_testcases/03_arith.lol` (`parse`): `parse-source: syntax error: unexpected I at line 5, col 9`
- `corpus/tier2/lolcode-py-sada/files/CMSC_124_testcases/04_smoosh_assign.lol` (`parse`): `parse-source: syntax error: unexpected I at line 5, col 9`
- `corpus/tier2/lolcode-py-sada/files/CMSC_124_testcases/05_bool.lol` (`lex`): `lex-source: unterminated string literal at line 9, col 27`
- `corpus/tier2/lolcode-py-sada/files/CMSC_124_testcases/06_comparison.lol` (`parse`): `parse-source: syntax error: unexpected I at line 4, col 9`
- `corpus/tier2/lolcode-py-sada/files/CMSC_124_testcases/07_ifelse.lol` (`parse`): `parse-source: syntax error: unexpected I at line 4, col 17`
- `corpus/tier2/lolcode-py-sada/files/CMSC_124_testcases/08_switch.lol` (`parse`): `parse-source: syntax error: unexpected I at line 4, col 17`
- `corpus/tier2/lolcode-py-sada/files/CMSC_124_testcases/09_loops.lol` (`parse`): `parse-source: syntax error: unexpected I at line 4, col 17`
- `corpus/tier2/lolcode-py-sada/files/CMSC_124_testcases/10_functions.lol` (`parse`): `parse-source: syntax error: unexpected ID ("y") at line 4, col 23`
- `corpus/tier2/lolcode-simple-algorithms/files/BASICS.lol` (`parse`): `parse-source: syntax error: unexpected ID ("TODO") at line 264, col 12`
- `corpus/tier2/loleuler/files/014.lol` (`eval`): `run-program: unknown identifier: MEMLIMIT`
- `corpus/tier2/maadriana-lolcode-interpreter/files/week2-3/test/conditional.lol` (`parse`): `parse-source: syntax error: unexpected ITZ at line 14, col 1`
- `corpus/tier2/maadriana-lolcode-interpreter/files/week2-3/test/final_test.lol` (`eval`): `/: division by zero`
- `corpus/tier2/maadriana-lolcode-interpreter/files/week2-3/test/invalid_input.lol` (`parse`): `parse-source: syntax error: unexpected NEWLINE at line 7, col 63`
- `corpus/tier2/markwatkinson-loljs/files/test/programs/bf.lol` (`parse`): `parse-source: syntax error: unexpected ID ("DUZ") at line 16, col 5`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/03_arith.lol` (`parse`): `parse-source: syntax error: unexpected OF at line 10, col 31`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/e02_line_continuation.lol` (`parse`): `parse-source: syntax error: unexpected STRING ("world!") at line 6, col 9`


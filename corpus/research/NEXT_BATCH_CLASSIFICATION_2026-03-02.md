# Next Batch Classification (Plausible/Uncertain Programs)

Generated: `2026-03-02T20:08:23Z`

## Totals

- Files scanned: `575`
- Likely programs: `534`
- Non-program files: `41`

## Category Buckets

- Good programs that work (as-is): `268`
- Fixed by adding version number: `48`
- Irredeemably bad out-of-version: `59`
- Bad programs remaining: `159`

## Failure Breakdown (All Likely Programs)

- Lexing errors: `12`
- Parsing errors: `229`
- Runtime errors: `24`
- Timeout (possible infinite loops): `1`

### Outcome Counts (Failures Only)

- `parse-error`: `229`
- `runtime-error`: `24`
- `lex-error`: `12`
- `timeout`: `1`

## Fixed By Adding Version Number

- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/3-MustIncludeVersion/test.lol`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/01_variables.lol`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/02_gimmeh.lol`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/04_smoosh_assign.lol`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/06_comparison.lol`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/07_ifelse.lol`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/08_switch.lol`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/09_loops.lol`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/06_comparison.lol`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/07_ifelse.lol`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/08_switch.lol`
- `corpus/tier2/learn-lolcode/files/LOLCode/End-Keyword/KTHXBYE/KTHXBYE_EndKeyword_InLOLCode.lol`
- `corpus/tier2/learn-lolcode/files/LOLCode/End-Keyword/KTHXBYE/KTHXBYE_EndKeyword_InLOLCode_V1.lol`
- `corpus/tier2/learn-lolcode/files/LOLCode/Shebang/Misc/MiscLOLCode_Shebang.lol`
- `corpus/tier2/learn-lolcode/files/LOLCode/Shebang/Misc/MiscLOLCode_Shebang_V1.lol`
- `corpus/tier2/learn-lolcode/files/OldVersions/PROJECT_LANGUAGE/LOLCODE/PROJECT_LANG_1_V1.lol`
- `corpus/tier2/learn-lolcode/files/PROJECT_LANG_1.lol`
- `corpus/tier2/loco/files/Samples/cmp_3_nums.lol`
- `corpus/tier2/loco/files/Samples/diamond.lol`
- `corpus/tier2/loco/files/Samples/diamond_box.lol`
- `corpus/tier2/loco/files/Samples/diamond_campfire.lol`
- `corpus/tier2/loco/files/Samples/factorial.lol`
- `corpus/tier2/loco/files/Samples/factorial_accumulator.lol`
- `corpus/tier2/loco/files/Samples/hollow_diamond1.lol`
- `corpus/tier2/loco/files/Samples/hollow_diamond2.lol`
- `corpus/tier2/loco/files/Samples/pascal_triangle.lol`
- `corpus/tier2/loco/files/Samples/prime_nums.lol`
- `corpus/tier2/loco/files/Samples/simple_calculator.lol`
- `corpus/tier2/lol-ruby/files/examples/hello.lol`
- `corpus/tier2/lolcode-py-cmsc124/files/sample/c.lol`
- `corpus/tier2/lolcode-py-cmsc124/files/sample/d.lol`
- `corpus/tier2/maadriana-lolcode-interpreter/files/week2-3/test/hello_world.lol`
- `corpus/tier2/maadriana-lolcode-interpreter/files/week2-3/test/logical_ops.lol`
- `corpus/tier2/maadriana-lolcode-interpreter/files/week2-3/test/nested_expr.lol`
- `corpus/tier2/maadriana-lolcode-interpreter/files/week2-3/test/smoosh.lol`
- `corpus/tier2/maadriana-lolcode-interpreter/files/week2-3/test/truthy.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/extra/sample.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/01_variables.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/02_gimmeh.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/04_smoosh_assign.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/05_bool.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/06_comparison.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/07_ifelse.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/08_switch.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/09_loops.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/e01_soft_line_breaks.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/e05_suppress_newline.lol`
- `corpus/tier2/nfenciso1-lolcode-interpreter/files/test-cases/e97_ascending_numbers.lol`

## Irredeemably Out-of-Version (Top Messages)

- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`: `49`
- `parse-source: unsupported version: 1.4 (this implementation only accepts HAI 1.3)`: `10`

## Bad Programs Remaining (Outcome Breakdown)

- `parse-error`: `122`
- `runtime-error`: `24`
- `lex-error`: `12`
- `timeout`: `1`

## Bad Programs Remaining (Top Failure Messages)

- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`: `57`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 4`: `6`
- `lex-source: unterminated string literal at line 6, col 27`: `3`
- `parse-source: syntax error: unexpected ID ("-->begin") at line 1, col 1`: `3`
- `parse-source: syntax error: unexpected ID ("OPEN") at line 3, col 5`: `3`
- `parse-source: syntax error: unexpected ID ("foo") at line 5, col 16`: `3`
- `parse-source: syntax error: unexpected ID ("…") at line 3, col 17`: `3`
- `parse-source: syntax error: unexpected KTHXBYE at line 5, col 1`: `3`
- `IS-NOW-A: cannot cast YARN to numeric value: ""`: `2`
- `IS-NOW-A: cannot cast YARN to numeric value: "abc"`: `2`
- `MAEK: cannot cast YARN to numeric value: ""`: `2`
- `MAEK: cannot cast YARN to numeric value: "abc"`: `2`
- `lex-source: unterminated string literal at line 2, col 17`: `2`
- `lex-source: unterminated string literal at line 8, col 31`: `2`
- `parse-source: syntax error: unexpected AN at line 2, col 23`: `2`
- `parse-source: syntax error: unexpected ID ("VAR!!1") at line 3, col 8`: `2`
- `parse-source: syntax error: unexpected ID ("foo") at line 4, col 16`: `2`
- `parse-source: syntax error: unexpected KTHXBYE at line 3, col 1`: `2`
- `parse-source: syntax error: unexpected LIEK at line 9, col 27`: `2`
- `parse-source: syntax error: unexpected STRING ("Dear curious test reader") at line 1, col 5`: `2`
- `remainder: division by zero`: `2`
- `/: division by zero`: `1`
- `IS-NOW-A: cannot cast YARN to numeric value: "1.23x"`: `1`
- `IS-NOW-A: cannot cast YARN to numeric value: "123x"`: `1`
- `MAEK: cannot cast YARN to numeric value: "1.23x"`: `1`
- `MAEK: cannot cast YARN to numeric value: "123x"`: `1`
- `evaluation timed out after 2.0 seconds`: `1`
- `lex-source: invalid Unicode code point in string literal at line 2, col 17`: `1`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 13, col 25`: `1`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 18, col 41`: `1`
- `lex-source: unterminated string literal at line 6, col 17`: `1`
- `lex-source: unterminated string literal at line 8, col 27`: `1`
- `parse-source: WTF? case literal must be NUMBER, STRING, WIN, FAIL, or NOOB; got var`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 15`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 24`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 25`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 26`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 27`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 28`: `1`
- `parse-source: syntax error: unexpected EOF at line 2, col 1`: `1`

## Promoted Missing-Version Eval Outcomes

- Promoted files evaluated: `121`
- `parse-error`: `61`
- `ok`: `48`
- `lex-error`: `9`
- `runtime-error`: `2`
- `timeout`: `1`

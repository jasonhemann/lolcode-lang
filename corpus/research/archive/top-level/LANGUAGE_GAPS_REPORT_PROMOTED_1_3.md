# Language Gap Report (Strict 1.3)

Generated: `Tuesday, March 10th, 2026 12:25:49am`

## Totals

- Corpus files: `223`
- In-scope 1.3 files: `133`
- In-scope parse-ok files: `89`
- In-scope eval-ok files: `51`
- Promoted missing-version files: `120`
- Fixture files: `17`
- Fixture parse-ok files: `17`

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

- `parse-ok`: `89`
- `ok`: `51`
- `runtime-error`: `38`
- `parse-error`: `36`
- `lex-error`: `8`

### In-Scope Lex Errors

- `lex-source: unterminated string literal at line 7, col 27`: `4`
- `lex-source: unterminated string literal at line 9, col 31`: `2`
- `lex-source: unterminated string literal at line 9, col 27`: `1`
- `lex-source: line continuation marker must be at end of line at line 20, col 48`: `1`

### In-Scope Parse Errors

- `parse-source: invalid identifier syntax: "+"`: `8`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`: `5`
- `parse-source: syntax error: unexpected SUM at line 10, col 27`: `4`
- `parse-source: syntax error: unexpected OF at line 26, col 50`: `2`
- `parse-source: syntax error: unexpected PRODUKT at line 26, col 41`: `2`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text " ")))) at line 14, col 47`: `1`
- `parse-source: syntax error: unexpected OF at line 49, col 37`: `1`
- `parse-source: syntax error: unexpected ITZ at line 14, col 1`: `1`
- `parse-source: syntax error: unexpected OF at line 27, col 50`: `1`
- `parse-source: syntax error: unexpected OF at line 30, col 33`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text ") Enter string: ")))) at line 16, col 45`: `1`
- `parse-source: invalid identifier syntax: "//"`: `1`
- `parse-source: syntax error: unexpected ID ("y") at line 4, col 23`: `1`
- `parse-source: invalid identifier syntax: "++"`: `1`
- `parse-source: syntax error: unexpected SUM at line 10, col 25`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text " ")))) at line 31, col 87`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "hello")))) at line 5, col 9`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 7, col 63`: `1`
- `parse-source: syntax error: unexpected ID ("DUZ") at line 16, col 5`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text ">Add what to [")))) at line 14, col 45`: `1`

### In-Scope Runtime Errors

- `run-program: unknown identifier: WAZZUP`: `18`
- `BIGGR: cannot cast NOOB to numeric value`: `9`
- `SUM: cannot cast NOOB to numeric value`: `6`
- `SMALLR: cannot cast NOOB to numeric value`: `4`
- `run-program: unknown slot: 7288`: `1`

### In-Scope Issue Triage

- `parse-core-suspect`: `38`
- `runtime-core-suspect`: `37`
- `likely-operator-spelling-drift`: `5`
- `program-runtime-slot-miss`: `1`
- `non-spec-line-comment-style`: `1`

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

- `loop-total`: `67`
- `if-total`: `66`
- `loop-with-update`: `62`
- `loop-with-cond-wile`: `40`
- `if-with-else`: `38`
- `function-total`: `22`
- `loop-with-cond-til`: `21`
- `switch-with-default`: `10`
- `switch-total`: `10`
- `if-with-mebbe`: `7`

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

- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/checkerboard/bonus_features.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/01_variables.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/02_gimmeh.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/03_arith.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/04_smoosh_assign.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/05_bool.lol` (`lex`, triage=`parse-core-suspect`): `lex-source: unterminated string literal at line 9, col 31`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/06_comparison.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/07_ifelse.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/08_switch.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/09_loops.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/10_functions.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/02_gimmeh.lol` (`eval`, triage=`runtime-core-suspect`): `SUM: cannot cast NOOB to numeric value`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/03_arith.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected SUM at line 10, col 27`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/05_bool.lol` (`lex`, triage=`parse-core-suspect`): `lex-source: unterminated string literal at line 7, col 27`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/06_comparison.lol` (`eval`, triage=`runtime-core-suspect`): `BIGGR: cannot cast NOOB to numeric value`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/07_ifelse.lol` (`eval`, triage=`runtime-core-suspect`): `BIGGR: cannot cast NOOB to numeric value`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/09_loops.lol` (`eval`, triage=`runtime-core-suspect`): `SMALLR: cannot cast NOOB to numeric value`
- `corpus/tier2/eulol/files/problem0003.lol` (`parse`, triage=`likely-operator-spelling-drift`): `parse-source: syntax error: unexpected OF at line 30, col 33`
- `corpus/tier2/eulol/files/problem0005.lol` (`parse`, triage=`likely-operator-spelling-drift`): `parse-source: syntax error: unexpected OF at line 49, col 37`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/02_gimmeh.lol` (`eval`, triage=`runtime-core-suspect`): `SUM: cannot cast NOOB to numeric value`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/03_arith.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected SUM at line 10, col 27`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/05_bool.lol` (`lex`, triage=`parse-core-suspect`): `lex-source: unterminated string literal at line 7, col 27`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/06_comparison.lol` (`eval`, triage=`runtime-core-suspect`): `BIGGR: cannot cast NOOB to numeric value`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/07_ifelse.lol` (`eval`, triage=`runtime-core-suspect`): `BIGGR: cannot cast NOOB to numeric value`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/08_switch.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected PRODUKT at line 26, col 41`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/09_loops.lol` (`eval`, triage=`runtime-core-suspect`): `SMALLR: cannot cast NOOB to numeric value`
- `corpus/tier2/learn-lolcode/files/OldVersions/PROJECT_LANGUAGE/LOLCODE/PROJECT_LANG_1_V1.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`
- `corpus/tier2/learn-lolcode/files/PROJECT_LANG_1.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`
- `corpus/tier2/loco/files/Samples/diamond_swan.lol` (`lex`, triage=`parse-core-suspect`): `lex-source: line continuation marker must be at end of line at line 20, col 48`
- `corpus/tier2/loco/files/Samples/even_nums.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text " ")))) at line 14, col 47`
- `corpus/tier2/loco/files/Samples/pascal_triangle.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text " ")))) at line 31, col 87`
- `corpus/tier2/lol-ruby/files/examples/hello.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`
- `corpus/tier2/lol-ruby/files/examples/ifthenelse.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`
- `corpus/tier2/lol-ruby/files/examples/loops.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`
- `corpus/tier2/lolcode-py-cmsc124/files/project-examples/02_gimmeh.lol` (`eval`, triage=`runtime-core-suspect`): `SUM: cannot cast NOOB to numeric value`
- `corpus/tier2/lolcode-py-cmsc124/files/project-examples/03_arith.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected SUM at line 10, col 27`
- `corpus/tier2/lolcode-py-cmsc124/files/project-examples/05_bool.lol` (`lex`, triage=`parse-core-suspect`): `lex-source: unterminated string literal at line 7, col 27`
- `corpus/tier2/lolcode-py-cmsc124/files/project-examples/06_comparison.lol` (`eval`, triage=`runtime-core-suspect`): `BIGGR: cannot cast NOOB to numeric value`
- `corpus/tier2/lolcode-py-cmsc124/files/project-examples/07_ifelse.lol` (`eval`, triage=`runtime-core-suspect`): `BIGGR: cannot cast NOOB to numeric value`
- `corpus/tier2/lolcode-py-cmsc124/files/project-examples/08_switch.lol` (`parse`, triage=`likely-operator-spelling-drift`): `parse-source: syntax error: unexpected OF at line 26, col 50`


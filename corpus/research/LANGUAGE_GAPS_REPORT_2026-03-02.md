# Language Gap Report (Strict 1.3)

Generated: `Thursday, March 5th, 2026 6:59:58pm`

## Totals

- Corpus files: `223`
- In-scope 1.3 files: `13`
- In-scope parse-ok files: `10`
- In-scope eval-ok files: `9`
- Promoted missing-version files: `0`
- Fixture files: `17`
- Fixture parse-ok files: `17`

### Corpus Header Classes (Original)

- `out-of-scope-hai-without-version`: `112`
- `out-of-scope-version-1.2`: `44`
- `non-program-no-leading-hai`: `26`
- `in-scope-1.3`: `13`
- `non-program-empty-or-comments`: `13`
- `out-of-scope-version-1.4`: `6`
- `out-of-scope-version-1.0`: `4`
- `out-of-scope-version-"dear`: `3`
- `out-of-scope-version-btw`: `1`
- `out-of-scope-version-"this`: `1`

### Corpus Header Classes (Effective For Analysis)

- `out-of-scope-hai-without-version`: `112`
- `out-of-scope-version-1.2`: `44`
- `non-program-no-leading-hai`: `26`
- `in-scope-1.3`: `13`
- `non-program-empty-or-comments`: `13`
- `out-of-scope-version-1.4`: `6`
- `out-of-scope-version-1.0`: `4`
- `out-of-scope-version-"dear`: `3`
- `out-of-scope-version-btw`: `1`
- `out-of-scope-version-"this`: `1`

### In-Scope 1.3 Status Counts

- `parse-ok`: `10`
- `ok`: `9`
- `parse-error`: `3`
- `runtime-error`: `1`

### In-Scope Lex Errors

- (none)

### In-Scope Parse Errors

- `parse-source: syntax error: unexpected OF at line 30, col 33`: `1`
- `parse-source: invalid identifier syntax: "//"`: `1`
- `parse-source: syntax error: unexpected OF at line 49, col 37`: `1`

### In-Scope Runtime Errors

- `run-program: unknown slot: 7288`: `1`

### In-Scope Issue Triage

- `likely-operator-spelling-drift`: `2`
- `program-runtime-slot-miss`: `1`
- `non-spec-line-comment-style`: `1`

### Missing Statement Forms In In-Scope Corpus

- `stmt-object-def`
- `stmt-switch`

### Missing Expression Forms In In-Scope Corpus

- `expr-method-call`

### Missing Binary Operators In In-Scope Corpus

- `WON OF`

### Missing Unary Operators In In-Scope Corpus

- (none)

### Missing Variadic Operators In In-Scope Corpus

- `ALL OF`
- `ANY OF`

### Used In Fixtures But Not In In-Scope Corpus (Statements)

- `stmt-object-def`
- `stmt-switch`

### Used In Fixtures But Not In In-Scope Corpus (Expressions)

- `expr-method-call`

### In-Scope Branch Shape Counts

- `loop-total`: `29`
- `loop-with-update`: `24`
- `loop-with-cond-wile`: `17`
- `if-total`: `17`
- `function-total`: `8`
- `loop-with-cond-til`: `7`
- `if-with-else`: `5`
- `if-with-mebbe`: `1`

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

- `corpus/tier2/eulol/files/problem0003.lol` (`parse`, triage=`likely-operator-spelling-drift`): `parse-source: syntax error: unexpected OF at line 30, col 33`
- `corpus/tier2/eulol/files/problem0005.lol` (`parse`, triage=`likely-operator-spelling-drift`): `parse-source: syntax error: unexpected OF at line 49, col 37`
- `corpus/tier2/lolcode-simple-algorithms/files/BASICS.lol` (`parse`, triage=`non-spec-line-comment-style`): `parse-source: invalid identifier syntax: "//"`
- `corpus/tier2/loleuler/files/014.lol` (`eval`, triage=`program-runtime-slot-miss`): `run-program: unknown slot: 7288`


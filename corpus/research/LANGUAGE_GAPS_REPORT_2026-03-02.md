# Language Gap Report (Strict 1.3)

Generated: `Monday, March 2nd, 2026 12:10:19pm`

## Totals

- Corpus files: `223`
- In-scope 1.3 files: `13`
- In-scope parse-ok files: `12`
- In-scope eval-ok files: `11`
- Fixture files: `16`
- Fixture parse-ok files: `16`

### Corpus Header Classes

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

### In-Scope 1.3 Status Counts

- `parse-ok`: `12`
- `ok`: `11`
- `runtime-error`: `1`
- `parse-error`: `1`

### In-Scope Lex Errors

- (none)

### In-Scope Parse Errors

- `parse-source: syntax error: unexpected ID ("TODO") at line 264, col 12`: `1`

### In-Scope Runtime Errors

- `run-program: unknown identifier: MEMLIMIT`: `1`

### Missing Statement Forms In In-Scope Corpus

- `stmt-import`
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

- `loop-total`: `36`
- `loop-with-update`: `29`
- `if-total`: `28`
- `loop-with-cond-wile`: `22`
- `function-total`: `17`
- `if-with-else`: `10`
- `loop-with-cond-til`: `7`
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

- `corpus/tier2/lolcode-simple-algorithms/files/BASICS.lol` (`parse`): `parse-source: syntax error: unexpected ID ("TODO") at line 264, col 12`
- `corpus/tier2/loleuler/files/014.lol` (`eval`): `run-program: unknown identifier: MEMLIMIT`


# Tier2 Classified Eval Snapshot

Generated: `Monday, March 2nd, 2026 3:02:06pm`

- Corpus root: `corpus/tier1`
- Timeout seconds: `2.0`

## Totals

- Files: `352`
- Likely programs: `350`
- Non-programs: `2`

### Classification Reasons

- `leading-hai`: `347`
- `hai-found-not-leading`: `3`
- `no-hai-header`: `2`

### Outcome Counts (All Files)

- `ok`: `257`
- `parse-error`: `63`
- `runtime-error`: `23`
- `lex-error`: `6`
- `non-program`: `2`
- `timeout`: `1`

### Outcome Counts (Likely Programs)

- `ok`: `257`
- `parse-error`: `63`
- `runtime-error`: `23`
- `lex-error`: `6`
- `timeout`: `1`

### Top Messages (Likely Programs)

- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`: `8`
- `parse-source: unsupported version: 1.4 (this implementation only accepts HAI 1.3)`: `7`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`: `7`
- `parse-source: syntax error: unexpected ID ("…") at line 3, col 17`: `3`
- `parse-source: syntax error: unexpected ID ("foo") at line 5, col 16`: `3`
- `parse-source: syntax error: unexpected KTHXBYE at line 5, col 1`: `3`
- `parse-source: syntax error: unexpected ID ("-->begin") at line 1, col 1`: `3`
- `parse-source: syntax error: unexpected AN at line 2, col 23`: `2`
- `lex-source: unterminated string literal at line 2, col 17`: `2`
- `parse-source: syntax error: unexpected ID ("foo") at line 4, col 16`: `2`
- `IS-NOW-A: cannot cast YARN to numeric value: ""`: `2`
- `IS-NOW-A: cannot cast YARN to numeric value: "abc"`: `2`
- `parse-source: syntax error: unexpected KTHXBYE at line 3, col 1`: `2`
- `remainder: division by zero`: `2`
- `MAEK: cannot cast YARN to numeric value: ""`: `2`
- `MAEK: cannot cast YARN to numeric value: "abc"`: `2`
- `parse-source: syntax error: unexpected LIEK at line 9, col 27`: `2`
- `parse-source: syntax error: unexpected MKAY at line 2, col 36`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 28`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 16`: `1`
- `run-program: function fun expected 0 args, got 1`: `1`
- `parse-source: WTF? case literal must be NUMBER, STRING, WIN, FAIL, or NOOB; got var`: `1`
- `run-program: function fun expected 3 args, got 2`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 24`: `1`
- `lex-source: unterminated string literal at line 6, col 17`: `1`
- `IS-NOW-A: cannot cast YARN to numeric value: "1.23x"`: `1`
- `parse-source: syntax error: unexpected ID ("foo") at line 7, col 16`: `1`
- `parse-source: syntax error: unexpected IF at line 5, col 1`: `1`
- `MAEK: cannot cast YARN to numeric value: "123x"`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 3, col 23`: `1`
- `parse-source: syntax error: unexpected IF at line 4, col 9`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 27`: `1`
- `run-program: function fun expected 1 args, got 2`: `1`
- `run-program: duplicate OMG literal in WTF?: (expr-number "0")`: `1`
- `parse-source: syntax error: unexpected EOF at line 2, col 1`: `1`
- `parse-source: syntax error: unexpected SUM at line 4, col 21`: `1`
- `parse-source: syntax error: unexpected SRS at line 5, col 18`: `1`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 13, col 25`: `1`
- `/: division by zero`: `1`
- `run-program: unknown identifier: fun1`: `1`
- `parse-source: syntax error: unexpected ID ("NEWLINE") at line 5, col 33`: `1`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 18, col 41`: `1`
- `lex-source: invalid Unicode code point in string literal at line 2, col 17`: `1`
- `parse-source: syntax error: unexpected NUMBER ("0") at line 8, col 17`: `1`
- `IS-NOW-A: cannot cast YARN to numeric value: "123x"`: `1`
- `run-program: unknown identifier: 1..23`: `1`
- `MAEK: cannot cast YARN to numeric value: "1.23x"`: `1`
- `parse-source: syntax error: unexpected ID ("sit") at line 3, col 15`: `1`
- `parse-source: syntax error: unexpected GTFO at line 4, col 17`: `1`
- `evaluation timed out after 2.0 seconds`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 26`: `1`
- `run-program: unknown function: foo'Z fun1`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 3, col 22`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 15`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 25`: `1`
- `run-program: unknown identifier: var`: `1`

## Sample Error Rows

- `corpus/tier1/i-has-js/files/examples/LOOP.lol` => `parse-error` (`parse-source: syntax error: unexpected NUMBER ("0") at line 8, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/0-Benchmarks/1-BFInterpreter/test.lol` => `timeout` (`evaluation timed out after 2.0 seconds`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/14-NoNewlineAfterJoinLF/test.lol` => `parse-error` (`parse-source: syntax error: unexpected KTHXBYE at line 5, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/15-NoNewlineAfterJoinCR/test.lol` => `parse-error` (`parse-source: syntax error: unexpected KTHXBYE at line 5, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/16-NoNewlineAfterJoinCRLF/test.lol` => `parse-error` (`parse-source: syntax error: unexpected KTHXBYE at line 5, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/3-MustIncludeVersion/test.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/4-MustEndWithKTHXBYE/test.lol` => `parse-error` (`parse-source: syntax error: unexpected EOF at line 2, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/10-Loops/6-UnaryFunction/test.lol` => `runtime-error` (`run-program: unknown identifier: var`)
- `corpus/tier1/lci/files/test/1.3-Tests/11-Unicode/1-EllipsesJoinLF/test.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("…") at line 3, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/11-Unicode/2-EllipsesJoinCR/test.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("…") at line 3, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/11-Unicode/3-EllipsesJoinCRLF/test.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("…") at line 3, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/11-Unicode/7-InvalidCodePointInString/test.lol` => `lex-error` (`lex-source: invalid Unicode code point in string literal at line 2, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/10-CallingObjectInitialization/test.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("foo") at line 4, col 16`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/11-CallingObjectAlternateSyntax/test.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("foo") at line 5, col 16`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/12-AlternateSyntax/test.lol` => `runtime-error` (`run-program: unknown function: foo'Z fun1`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/13-Inheritance/1-Declaration/test.lol` => `parse-error` (`parse-source: syntax error: unexpected LIEK at line 9, col 27`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/13-Inheritance/2-Assignment/test.lol` => `parse-error` (`parse-source: syntax error: unexpected LIEK at line 9, col 27`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/2-SlotCreation/test.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 3, col 22`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/4-SlotAssignment/test.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 3, col 23`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/5-FunctionStorage/test.lol` => `runtime-error` (`run-program: unknown identifier: fun1`)


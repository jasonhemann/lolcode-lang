# Tier2 Classified Eval Snapshot

Generated: `Monday, March 2nd, 2026 5:47:56pm`

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

- `ok`: `273`
- `parse-error`: `49`
- `runtime-error`: `21`
- `lex-error`: `6`
- `non-program`: `2`
- `timeout`: `1`

### Outcome Counts (Likely Programs)

- `ok`: `273`
- `parse-error`: `49`
- `runtime-error`: `21`
- `lex-error`: `6`
- `timeout`: `1`

### Top Messages (Likely Programs)

- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`: `9`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`: `7`
- `parse-source: unsupported version: 1.4 (this implementation only accepts HAI 1.3)`: `7`
- `parse-source: syntax error: unexpected KTHXBYE at line 5, col 1`: `3`
- `parse-source: syntax error: unexpected ID ("-->begin") at line 1, col 1`: `3`
- `parse-source: syntax error: unexpected AN at line 2, col 23`: `2`
- `lex-source: unterminated string literal at line 2, col 17`: `2`
- `IS-NOW-A: cannot cast YARN to numeric value: ""`: `2`
- `IS-NOW-A: cannot cast YARN to numeric value: "abc"`: `2`
- `parse-source: syntax error: unexpected KTHXBYE at line 3, col 1`: `2`
- `remainder: division by zero`: `2`
- `MAEK: cannot cast YARN to numeric value: ""`: `2`
- `MAEK: cannot cast YARN to numeric value: "abc"`: `2`
- `parse-source: syntax error: unexpected AN at line 2, col 28`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 16`: `1`
- `run-program: function fun expected 0 args, got 1`: `1`
- `parse-source: syntax error: unexpected VISIBLE at line 14, col 9`: `1`
- `parse-source: WTF? case literal must be NUMBER, STRING, WIN, FAIL, or NOOB; got var`: `1`
- `run-program: function fun expected 3 args, got 2`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 24`: `1`
- `lex-source: unterminated string literal at line 6, col 17`: `1`
- `IS-NOW-A: cannot cast YARN to numeric value: "1.23x"`: `1`
- `parse-source: syntax error: unexpected IF at line 5, col 1`: `1`
- `MAEK: cannot cast YARN to numeric value: "123x"`: `1`
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
- `parse-source: syntax error: unexpected AN at line 2, col 25`: `1`

## Sample Error Rows

- `corpus/tier1/i-has-js/files/examples/LOOP.lol` => `parse-error` (`parse-source: syntax error: unexpected NUMBER ("0") at line 8, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/0-Benchmarks/1-BFInterpreter/test.lol` => `timeout` (`evaluation timed out after 2.0 seconds`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/14-NoNewlineAfterJoinLF/test.lol` => `parse-error` (`parse-source: syntax error: unexpected KTHXBYE at line 5, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/15-NoNewlineAfterJoinCR/test.lol` => `parse-error` (`parse-source: syntax error: unexpected KTHXBYE at line 5, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/16-NoNewlineAfterJoinCRLF/test.lol` => `parse-error` (`parse-source: syntax error: unexpected KTHXBYE at line 5, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/3-MustIncludeVersion/test.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/4-MustEndWithKTHXBYE/test.lol` => `parse-error` (`parse-source: syntax error: unexpected EOF at line 2, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/11-Unicode/7-InvalidCodePointInString/test.lol` => `lex-error` (`lex-source: invalid Unicode code point in string literal at line 2, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/11-CallingObjectAlternateSyntax/test.lol` => `parse-error` (`parse-source: syntax error: unexpected VISIBLE at line 14, col 9`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/5-FunctionStorage/test.lol` => `runtime-error` (`run-program: unknown identifier: fun1`)
- `corpus/tier1/lci/files/test/1.3-Tests/2-Comments/1-SingleLine/6-IgnoreContinuation/test.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("sit") at line 3, col 15`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/3-Integer/2-MustHaveAdjacentHyphen/test.lol` => `parse-error` (`parse-source: syntax error: unexpected KTHXBYE at line 3, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/4-Float/1-OnlyOneDecimalPoint/test.lol` => `runtime-error` (`run-program: unknown identifier: 1..23`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/4-Float/2-MustHaveAdjacentHyphen/test.lol` => `parse-error` (`parse-source: syntax error: unexpected KTHXBYE at line 3, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/5-String/2-Syntax/1-IgnoreContinuation/test.lol` => `lex-error` (`lex-source: unterminated string literal at line 2, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/5-String/2-Syntax/3-MustHaveClosingQuote/test.lol` => `lex-error` (`lex-source: unterminated string literal at line 2, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/4-Output/1-MustHaveAnArg/test.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 2, col 16`)
- `corpus/tier1/lci/files/test/1.3-Tests/6-Variables/10-Indirect/6-Functions/test.lol` => `parse-error` (`parse-source: syntax error: unexpected SRS at line 5, col 18`)
- `corpus/tier1/lci/files/test/1.3-Tests/7-Operators/1-Addition/10-ArityCheck/test.lol` => `parse-error` (`parse-source: syntax error: unexpected AN at line 2, col 23`)
- `corpus/tier1/lci/files/test/1.3-Tests/7-Operators/17-ExplicitCast/3-ToInteger/5-FromString/2-EmptyString/test.lol` => `runtime-error` (`MAEK: cannot cast YARN to numeric value: ""`)


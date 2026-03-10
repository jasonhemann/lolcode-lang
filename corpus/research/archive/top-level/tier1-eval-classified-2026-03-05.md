# Tier2 Classified Eval Snapshot

Generated: `Thursday, March 5th, 2026 9:31:33am`

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

- `ok`: `270`
- `parse-error`: `47`
- `runtime-error`: `21`
- `lex-error`: `11`
- `non-program`: `2`
- `timeout`: `1`

### Outcome Counts (Likely Programs)

- `ok`: `270`
- `parse-error`: `47`
- `runtime-error`: `21`
- `lex-error`: `11`
- `timeout`: `1`

### Top Messages (Likely Programs)

- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`: `10`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`: `7`
- `parse-source: invalid identifier syntax: "SOCKS?"`: `3`
- `parse-source: syntax error: unexpected ID ("-->begin") at line 1, col 1`: `3`
- `parse-source: invalid identifier syntax: "STDIO?"`: `3`
- `lex-source: line continuation may not be followed by an empty line at line 2, col 31`: `3`
- `parse-source: syntax error: unexpected AN at line 2, col 23`: `2`
- `SUM: cannot cast NOOB to numeric value`: `2`
- `lex-source: unterminated string literal at line 2, col 17`: `2`
- `IS-NOW-A: cannot cast YARN to numeric value: ""`: `2`
- `IS-NOW-A: cannot cast YARN to numeric value: "abc"`: `2`
- `remainder: division by zero`: `2`
- `MAEK: cannot cast YARN to numeric value: ""`: `2`
- `parse-source: invalid numeric literal: '-' must be adjacent to digits at line 2, col 25`: `2`
- `MAEK: cannot cast YARN to numeric value: "abc"`: `2`
- `parse-source: invalid identifier syntax: "STDLIB?"`: `2`
- `parse-source: invalid identifier syntax: "STRING?"`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 28`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 16`: `1`
- `run-program: function fun expected 0 args, got 1`: `1`
- `parse-source: syntax error: unexpected VISIBLE at line 13, col 9`: `1`
- `parse-source: syntax error: unexpected ID ("FAIL") at line 2, col 113`: `1`
- `parse-source: WTF? case literal must be NUMBER, STRING, WIN, FAIL, or NOOB; got var`: `1`
- `lex-source: invalid Unicode normative name in string literal at line 3, col 17`: `1`
- `run-program: function fun expected 3 args, got 2`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 24`: `1`
- `lex-source: unterminated string literal at line 6, col 17`: `1`
- `MAEK: cannot cast YARN to numeric value: " 1.23"`: `1`
- `run-program: unknown identifier: foo`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 27`: `1`
- `run-program: function fun expected 1 args, got 2`: `1`
- `parse-source: syntax error: unexpected EOF at line 2, col 1`: `1`
- `parse-source: duplicate OMG literal in WTF?: (expr-number "0")`: `1`
- `parse-source: syntax error: unexpected SUM at line 4, col 21`: `1`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 13, col 25`: `1`
- `/: division by zero`: `1`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 18, col 41`: `1`
- `IS-NOW-A: cannot cast YARN to numeric value: " 1.23"`: `1`
- `lex-source: invalid numeric literal at line 2, col 25`: `1`
- `IS-NOW-A: cannot cast YARN to numeric value: " 123"`: `1`
- `MAEK: cannot cast YARN to numeric value: " 123"`: `1`
- `parse-source: syntax error: unexpected ID ("ITS") at line 8, col 13`: `1`
- `parse-source: syntax error: unexpected ID ("sit") at line 3, col 15`: `1`
- `evaluation timed out after 2.0 seconds`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 26`: `1`
- `lex-source: invalid Unicode code point in string literal at line 2, col 17`: `1`
- `parse-source: syntax error: unexpected AN at line 2, col 25`: `1`

## Sample Error Rows

- `corpus/tier1/i-has-js/files/examples/LOOP.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("ITS") at line 8, col 13`)
- `corpus/tier1/lci/files/test/1.3-Tests/0-Benchmarks/1-BFInterpreter/test.lol` => `timeout` (`evaluation timed out after 2.0 seconds`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/14-NoNewlineAfterJoinLF/test.lol` => `lex-error` (`lex-source: line continuation may not be followed by an empty line at line 2, col 31`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/15-NoNewlineAfterJoinCR/test.lol` => `lex-error` (`lex-source: line continuation may not be followed by an empty line at line 2, col 31`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/16-NoNewlineAfterJoinCRLF/test.lol` => `lex-error` (`lex-source: line continuation may not be followed by an empty line at line 2, col 31`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/17-Includes/test.lol` => `parse-error` (`parse-source: invalid identifier syntax: "STDIO?"`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/3-MustIncludeVersion/test.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier1/lci/files/test/1.3-Tests/1-Structure/4-MustEndWithKTHXBYE/test.lol` => `parse-error` (`parse-source: syntax error: unexpected EOF at line 2, col 1`)
- `corpus/tier1/lci/files/test/1.3-Tests/11-Unicode/7-InvalidCodePointInString/test.lol` => `lex-error` (`lex-source: invalid Unicode code point in string literal at line 2, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/11-Unicode/8-InvalidNormativeName/test.lol` => `lex-error` (`lex-source: invalid Unicode normative name in string literal at line 3, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/12-Arrays/13-Inheritance/3-AlternateSyntax/test.lol` => `runtime-error` (`run-program: unknown identifier: foo`)
- `corpus/tier1/lci/files/test/1.3-Tests/2-Comments/1-SingleLine/6-IgnoreContinuation/test.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("sit") at line 3, col 15`)
- `corpus/tier1/lci/files/test/1.3-Tests/2-Comments/2-MultipleLine/4-MustStartOnSeparateLine/test.lol` => `parse-error` (`parse-source: syntax error: unexpected VISIBLE at line 13, col 9`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/1-Nil/2-NilToInteger/test.lol` => `runtime-error` (`SUM: cannot cast NOOB to numeric value`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/1-Nil/3-NilToFloat/test.lol` => `runtime-error` (`SUM: cannot cast NOOB to numeric value`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/3-Integer/2-MustHaveAdjacentHyphen/test.lol` => `parse-error` (`parse-source: invalid numeric literal: '-' must be adjacent to digits at line 2, col 25`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/4-Float/1-OnlyOneDecimalPoint/test.lol` => `lex-error` (`lex-source: invalid numeric literal at line 2, col 25`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/4-Float/2-MustHaveAdjacentHyphen/test.lol` => `parse-error` (`parse-source: invalid numeric literal: '-' must be adjacent to digits at line 2, col 25`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/5-String/2-Syntax/1-IgnoreContinuation/test.lol` => `lex-error` (`lex-source: unterminated string literal at line 2, col 17`)
- `corpus/tier1/lci/files/test/1.3-Tests/3-Types/5-String/2-Syntax/3-MustHaveClosingQuote/test.lol` => `lex-error` (`lex-source: unterminated string literal at line 2, col 17`)


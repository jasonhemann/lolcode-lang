# Tier2 Classified Eval Snapshot

Generated: `Wednesday, April 1st, 2026 7:24:45pm`

- JSON source: `corpus/research/tier2-eval-classified.json`

- Corpus root: `corpus/tier2`
- Timeout seconds: `2.0`

## Totals

- Files: `2097`
- Likely programs: `2035`
- Non-programs: `62`

### Classification Reasons

- `leading-hai`: `1873`
- `hai-found-not-leading`: `162`
- `no-hai-header`: `57`
- `empty-or-comments-only`: `5`

### Outcome Counts (All Files)

- `parse-error`: `1378`
- `ok`: `512`
- `lex-error`: `86`
- `non-program`: `62`
- `runtime-error`: `59`

### Outcome Counts (Likely Programs)

- `parse-error`: `1378`
- `ok`: `512`
- `lex-error`: `86`
- `runtime-error`: `59`

### Top Messages (Likely Programs)

- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`: `582`
- `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`: `498`
- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`: `105`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 9`: `16`
- `run-program: unknown identifier: var`: `14`
- `lex-source: unterminated string literal at line 8, col 27`: `12`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "test")))) at line 3, col 9`: `11`
- `lex-source: unterminated string literal at line 8, col 31`: `10`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 5`: `9`
- `parse-source: syntax error: unexpected ID ("GOT") at line 1, col 5`: `8`
- `lex-source: unterminated string literal at line 6, col 27`: `6`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 11`: `6`
- `lex-source: line continuation may not be followed by an empty line at line 2, col 31`: `6`
- `lex-source: unterminated string literal at line 6, col 17`: `5`
- `lex-source: TLDR must be followed by newline or comma`: `5`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 13, col 25`: `5`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 18, col 41`: `5`
- `parse-source: syntax error: unexpected AN at line 2, col 23`: `4`
- `SUM: cannot cast NOOB to numeric value`: `4`
- `lex-source: unterminated string literal at line 2, col 17`: `4`
- `IS-NOW-A: cannot cast YARN to numeric value: ""`: `4`
- `IS-NOW-A: cannot cast YARN to numeric value: "abc"`: `4`
- `remainder: division by zero`: `4`
- `MAEK: cannot cast YARN to numeric value: ""`: `4`
- `parse-source: invalid numeric literal: '-' must be adjacent to digits at line 2, col 25`: `4`
- `MAEK: cannot cast YARN to numeric value: "abc"`: `4`
- `parse-source: no material allowed after KTHXBYE`: `4`
- `parse-source: syntax error: unexpected ID ("WAY") at line 8, col 20`: `3`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 17`: `3`
- `parse-source: syntax error: unexpected ID ("SOCKS?") at line 2, col 13`: `3`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 13`: `3`
- `parse-source: syntax error: unexpected ID ("STRING?") at line 2, col 13`: `3`
- `parse-source: syntax error: unexpected ID ("STDLIB?") at line 2, col 13`: `2`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 16`: `2`
- `parse-source: syntax error: unexpected AN at line 2, col 28`: `2`
- `run-program: function fun expected 0 args, got 1`: `2`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 4`: `2`
- `run-program: identifier already declared in this scope: var`: `2`
- `parse-source: duplicate OMG literal in WTF?: (expr-number "1")`: `2`
- `lex-source: invalid Unicode normative name in string literal at line 3, col 17`: `2`
- `parse-source: syntax error: unexpected AN at line 3, col 27`: `2`
- `parse-source: syntax error: unexpected ID ("LOL") at line 1, col 5`: `2`
- `parse-source: WTF? case literal must be NUMBER, STRING, WIN, FAIL, or NOOB; got var`: `2`
- `parse-source: syntax error: unexpected AN at line 2, col 24`: `2`
- `parse-source: syntax error: unexpected SRS at line 9, col 48`: `2`
- `lex-source: unterminated string literal at line 4, col 17`: `2`
- `lex-source: unterminated string literal at line 3, col 17`: `2`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 4, col 9`: `2`
- `run-program: unknown identifier: foo`: `2`
- `lex-source: unterminated string literal at line 8, col 33`: `2`
- `MAEK: cannot cast YARN to numeric value: " 1.23"`: `2`
- `parse-source: syntax error: unexpected AN at line 2, col 27`: `2`
- `run-program: function fun expected 1 args, got 2`: `2`
- `parse-source: syntax error: unexpected ID ("GEEK") at line 1, col 5`: `2`
- `parse-source: syntax error: unexpected EOF at line 2, col 1`: `2`
- `parse-source: syntax error: unexpected SUM at line 4, col 21`: `2`
- `parse-source: syntax error: unexpected NEWLINE at line 3, col 12`: `2`
- `parse-source: duplicate OMG literal in WTF?: (expr-number "0")`: `2`
- `IS-NOW-A: cannot cast YARN to numeric value: " 1.23"`: `2`
- `lex-source: invalid numeric literal at line 2, col 25`: `2`
- `lex-source: invalid Unicode code point in string literal at line 2, col 17`: `2`
- `lex-source: OBTW block comment must start at statement boundary at line 2, col 31`: `2`
- `IS-NOW-A: cannot cast YARN to numeric value: " 123"`: `2`
- `parse-source: syntax error: unexpected A at line 13, col 31`: `2`
- `quotient: division by zero`: `2`
- `parse-source: syntax error: unexpected ID ("VAR!!1") at line 3, col 8`: `2`
- `lex-source: unterminated string literal at line 8, col 30`: `2`
- `MAEK: cannot cast YARN to numeric value: " 123"`: `2`
- `parse-source: syntax error: unexpected A at line 3, col 28`: `2`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "Dear curious test reader")))) at line 1, col 5`: `2`
- `parse-source: syntax error: unexpected ID ("sit") at line 3, col 15`: `2`
- `parse-source: unsupported version: 1.4 (this implementation only accepts HAI 1.3)`: `2`
- `parse-source: syntax error: unexpected AN at line 7, col 29`: `2`
- `parse-source: syntax error: unexpected ID ("RAYLIB?") at line 2, col 9`: `2`
- `parse-source: syntax error: unexpected AN at line 2, col 26`: `2`
- `parse-source: syntax error: unexpected AN at line 2, col 15`: `2`
- `parse-source: syntax error: unexpected AN at line 2, col 25`: `2`
- `lex-source: unterminated string literal at line 9, col 31`: `1`
- `parse-source: syntax error: unexpected AN at line 9, col 33`: `1`
- `parse-source: invalid identifier syntax: "MKAY?"`: `1`
- `parse-source: syntax error: unexpected ID ("PARSER?") at line 3, col 9`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 3, col 16`: `1`
- `parse-source: syntax error: unexpected ID ("MKAY?") at line 11, col 6`: `1`
- `parse-source: implicit MKAY omission is only allowed at statement boundary; explicit MKAY required before ! at line 14, col 46`: `1`
- `parse-source: syntax error: unexpected ID ("MAH") at line 9, col 42`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 4, col 4`: `1`
- `parse-source: syntax error: unexpected ID ("NOES") at line 20, col 3`: `1`
- `parse-source: invalid identifier syntax: "+"`: `1`
- `parse-source: syntax error: unexpected MKAY at line 5, col 35`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 15`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "Dear reader")))) at line 1, col 5`: `1`
- `lex-source: invalid Unicode normative name in string literal at line 4, col 13`: `1`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`: `1`
- `lex-source: unterminated :[...] Unicode escape in string literal at line 11, col 26`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "line")))) at line 3, col 9`: `1`
- `parse-source: syntax error: unexpected OF at line 13, col 12`: `1`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 7, col 9`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "has_a")))) at line 3, col 9`: `1`
- `parse-source: syntax error: unexpected ID ("IT") at line 51, col 15`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 47`: `1`
- `parse-source: invalid identifier syntax: "<<N>>"`: `1`
- `parse-source: syntax error: unexpected A at line 6, col 36`: `1`
- `lex-source: invalid Unicode code point escape in string literal at line 3, col 9`: `1`
- `lex-source: OBTW block comment must start at statement boundary at line 4, col 37`: `1`
- `parse-source: syntax error: unexpected A at line 17, col 40`: `1`
- `parse-source: invalid identifier syntax: "//"`: `1`
- `parse-source: syntax error: unexpected DIFF at line 9, col 32`: `1`
- `parse-source: duplicate OMG literal in WTF?: (expr-number "5.0")`: `1`
- `parse-source: syntax error: unexpected ID ("WAY") at line 1, col 92`: `1`
- `run-program: unknown identifier: X`: `1`
- `parse-source: syntax error: unexpected ID ("tries") at line 42, col 24`: `1`
- `parse-source: syntax error: unexpected YR at line 7, col 40`: `1`
- `parse-source: syntax error: unexpected ID ("number") at line 22, col 74`: `1`
- `parse-source: syntax error: unexpected EOF at line 8, col 1`: `1`
- `parse-source: syntax error: unexpected AN at line 8, col 22`: `1`
- `parse-source: syntax error: unexpected KTHX at line 20, col 3`: `1`
- `parse-source: syntax error: unexpected SUM at line 3, col 13`: `1`
- `parse-source: syntax error: unexpected ID ("left") at line 7, col 28`: `1`
- `run-program: unknown identifier: N`: `1`
- `parse-source: syntax error: unexpected EOF at line 8, col 8`: `1`
- `parse-source: syntax error: unexpected KTHX at line 6, col 1`: `1`
- `parse-source: syntax error: unexpected IZ at line 5, col 5`: `1`
- `parse-source: syntax error: unexpected AN at line 165, col 19`: `1`
- `parse-source: syntax error: unexpected ID ("secret") at line 8, col 15`: `1`
- `parse-source: syntax error: unexpected A at line 8, col 31`: `1`
- `parse-source: syntax error: unexpected ID ("STRING?") at line 17, col 11`: `1`
- `parse-source: syntax error: unexpected ID ("JSON?") at line 3, col 9`: `1`
- `parse-source: syntax error: unexpected ID ("STRING?") at line 2, col 9`: `1`
- `lex-source: invalid numeric literal at line 32, col 16`: `1`
- `parse-source: syntax error: unexpected AN at line 8, col 37`: `1`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 3, col 9`: `1`
- `parse-source: syntax error: unexpected MKAY at line 17, col 64`: `1`
- `parse-source: syntax error: unexpected ID ("A_2_KOMPLIKATE_MATEHMATHICC_TINGY_4_ME") at line 67, col 60`: `1`
- `parse-source: syntax error: unexpected KTHXBYE at line 10, col 1`: `1`
- `run-program: unknown identifier: INDEX`: `1`
- `parse-source: syntax error: unexpected ID ("BRAINZ?") at line 2, col 13`: `1`
- `parse-source: syntax error: unexpected ID ("guess") at line 7, col 38`: `1`
- `parse-source: syntax error: unexpected A at line 16, col 34`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "../path")))) at line 4, col 9`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "pairs")))) at line 3, col 9`: `1`
- `lex-source: line continuation marker must be at end of line at line 19, col 48`: `1`
- `parse-source: syntax error: unexpected A at line 20, col 21`: `1`
- `lex-source: invalid numeric literal at line 4, col 25`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "-chu")))) at line 12, col 22`: `1`
- `parse-source: syntax error: unexpected A at line 12, col 32`: `1`
- `lex-source: unterminated :{...} placeholder in string literal at line 4, col 9`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 6`: `1`
- `lex-source: line continuation marker must be at end of line at line 2, col 72`: `1`
- `parse-source: implicit MKAY omission is only allowed at statement boundary; explicit MKAY required before AN YR at line 35, col 71`: `1`
- `lex-source: unterminated string literal at line 11, col 1`: `1`
- `parse-source: syntax error: unexpected NUMBER ("1") at line 7, col 37`: `1`
- `parse-source: syntax error: unexpected YR at line 46, col 25`: `1`

## Sample Error Rows

- `corpus/tier2/aagoshi-lolcode/files/actual testcases/ifelse.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/tier2/aagoshi-lolcode/files/actual testcases/io.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/tier2/aagoshi-lolcode/files/actual testcases/ops/arithop.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/tier2/aagoshi-lolcode/files/actual testcases/ops/assignop.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/tier2/aagoshi-lolcode/files/actual testcases/ops/boolop.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/tier2/aagoshi-lolcode/files/actual testcases/ops/compop.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/tier2/aagoshi-lolcode/files/actual testcases/switch.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/tier2/aagoshi-lolcode/files/actual testcases/vardecinit.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/tier2/aagoshi-lolcode/files/customtestcases/Declaration.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/aagoshi-lolcode/files/customtestcases/VISIBLE_StringLiteral.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/aagoshi-lolcode/files/customtestcases/arith.lol` => `lex-error` (`lex-source: invalid numeric literal at line 32, col 16`)
- `corpus/tier2/aagoshi-lolcode/files/customtestcases/bool.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/aagoshi-lolcode/files/customtestcases/comp.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/aagoshi-lolcode/files/customtestcases/ifelse.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/tier2/aagoshi-lolcode/files/customtestcases/switch.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/tier2/aagoshi-lolcode/files/sample codes lol/arith.lol` => `parse-error` (`parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`)
- `corpus/tier2/aagoshi-lolcode/files/sample codes lol/bool.lol` => `parse-error` (`parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`)
- `corpus/tier2/aagoshi-lolcode/files/sample codes lol/comp.lol` => `parse-error` (`parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`)
- `corpus/tier2/aagoshi-lolcode/files/sample codes lol/io.lol` => `parse-error` (`parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`)
- `corpus/tier2/aagoshi-lolcode/files/sample codes lol/sample.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)


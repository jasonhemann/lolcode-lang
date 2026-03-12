# Tier2 Classified Eval Snapshot

Generated: `Thursday, March 12th, 2026 6:24:59pm`

- JSON source: `corpus/research/github_language_lolcode/hits-eval-classified.json`

- Corpus root: `corpus/research/github_language_lolcode/hits_files`
- Timeout seconds: `2.0`

## Totals

- Files: `739`
- Likely programs: `465`
- Non-programs: `274`

### Classification Reasons

- `leading-hai`: `436`
- `no-hai-header`: `274`
- `hai-found-not-leading`: `29`

### Outcome Counts (All Files)

- `parse-error`: `367`
- `non-program`: `274`
- `ok`: `72`
- `runtime-error`: `16`
- `lex-error`: `9`
- `timeout`: `1`

### Outcome Counts (Likely Programs)

- `parse-error`: `367`
- `ok`: `72`
- `runtime-error`: `16`
- `lex-error`: `9`
- `timeout`: `1`

### Top Messages (Likely Programs)

- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`: `111`
- `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`: `94`
- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`: `66`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 9`: `20`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 11`: `16`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 16`: `5`
- `SUM: cannot cast NOOB to numeric value`: `5`
- `parse-source: syntax error: unexpected AN at line 7, col 29`: `5`
- `run-program: unknown identifier: var`: `5`
- `parse-source: invalid identifier syntax: "MKAY?"`: `4`
- `lex-source: unterminated string literal at line 2, col 17`: `4`
- `MAEK: cannot cast YARN to numeric value: ""`: `4`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 5, col 9`: `3`
- `parse-source: unsupported version: 1.4 (this implementation only accepts HAI 1.3)`: `3`
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 5`: `3`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 17`: `2`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 13`: `2`
- `parse-source: syntax error: unexpected ID ("STRING?") at line 17, col 11`: `2`
- `parse-source: syntax error: unexpected ID ("STRING?") at line 5, col 9`: `2`
- `parse-source: syntax error: unexpected IM at line 54, col 9`: `2`
- `parse-source: unsupported version: GOT (this implementation only accepts HAI 1.3)`: `2`
- `parse-source: syntax error: unexpected NEWLINE at line 3, col 16`: `1`
- `lex-source: unterminated string literal at line 7, col 31`: `1`
- `parse-source: syntax error: unexpected MKAY at line 5, col 35`: `1`
- `parse-source: syntax error: unexpected ID ("NUMBER1INPUT") at line 5, col 7`: `1`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`: `1`
- `parse-source: unsupported version: 1 (this implementation only accepts HAI 1.3)`: `1`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 7, col 9`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "test")))) at line 3, col 9`: `1`
- `parse-source: invalid identifier syntax: "<<N>>"`: `1`
- `parse-source: syntax error: unexpected I at line 9, col 27`: `1`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 12, col 13`: `1`
- `parse-source: syntax error: unexpected ID ("NUMBER1") at line 9, col 7`: `1`
- `parse-source: duplicate OMG literal in WTF?: (expr-number "5.0")`: `1`
- `parse-source: syntax error: unexpected A at line 21, col 12`: `1`
- `lex-source: unterminated :(... ) Unicode escape in string literal at line 13, col 25`: `1`
- `lex-source: unterminated string literal at line 3, col 9`: `1`
- `parse-source: syntax error: unexpected ID ("STRING?") at line 2, col 13`: `1`
- `parse-source: syntax error: unexpected ID ("MYLIB?") at line 2, col 11`: `1`
- `parse-source: implicit MKAY omission is only allowed at statement boundary; explicit MKAY required before AN YR at line 41, col 80`: `1`
- `parse-source: syntax error: unexpected A at line 8, col 31`: `1`
- `parse-source: syntax error: unexpected BANG at line 3, col 5`: `1`
- `parse-source: syntax error: unexpected IZ at line 5, col 5`: `1`
- `IS-NOW-A: cannot cast YARN to numeric value: " 123"`: `1`
- `lex-source: unterminated string literal at line 47, col 13`: `1`
- `run-program: unknown identifier: Z`: `1`
- `parse-source: syntax error: unexpected MKAY at line 17, col 64`: `1`
- `parse-source: syntax error: unexpected ID ("A_2_KOMPLIKATE_MATEHMATHICC_TINGY_4_ME") at line 67, col 60`: `1`
- `parse-source: syntax error: unexpected ID ("guess") at line 7, col 38`: `1`
- `parse-source: syntax error: unexpected A at line 16, col 34`: `1`
- `evaluation timed out after 2.0 seconds`: `1`
- `parse-source: syntax error: unexpected ID ("===========================================") at line 5, col 1`: `1`
- `parse-source: syntax error: unexpected A at line 20, col 21`: `1`
- `lex-source: unterminated OBTW block comment`: `1`

## Sample Error Rows

- `corpus/research/github_language_lolcode/hits_files/A1rPun/nurture/1374f70cfdf80ab66308a83b7fb076101ae665fe/esolang/lolcode/helloworld.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/research/github_language_lolcode/hits_files/ABCD-rgb/lolcode-interpreter/0f363b3c495ae3215263eead7274f752e4ae6b3e/source code/project-testcases/extra.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/research/github_language_lolcode/hits_files/AbhishekR25/cerner_2_5_2022/260116f43dea917b50211300b0fcb818271c384e/PowerOfANum.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/research/github_language_lolcode/hits_files/AharonSambol/AdventOfCode/0325a4d5c7125928e426fab526cce6857427ec1c/2020/LOLAnswers/day2.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("STRING?") at line 2, col 13`)
- `corpus/research/github_language_lolcode/hits_files/Ajlyde/LOLCODE/135a9cc9987732751291dea6bad2fb9f4390bfba/test2.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/research/github_language_lolcode/hits_files/Ajlyde/LOLCODE/13a4b7b5240b43d2e2d882621c335829ef779b44/test1.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/research/github_language_lolcode/hits_files/AldCristobal/CMSC-124-Project-CodeAndDecode/1af61688a3013df1ca4522de0ef037e18a9daf19/samplecodes/this.lol` => `parse-error` (`parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`)
- `corpus/research/github_language_lolcode/hits_files/AlexaCabral/CMSC124_project/115b499144bcfa60a91c164fd1ce3307ed14aeed/project-testcases/04_smoosh_assign.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/research/github_language_lolcode/hits_files/AngJianming/hello-world-in-every-programming-language/17e2645a9295db88fcb0d886d4a784f568b4e30c/reference/contribution/hello-world.lol` => `parse-error` (`parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`)
- `corpus/research/github_language_lolcode/hits_files/AnmiTaliDev/crosshello/199b2e78e0ad3c60dc93d6fcb7c36c81f26703a5/LOLCODE/hello.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 9`)
- `corpus/research/github_language_lolcode/hits_files/Aspirar/hello-world/b82b9fa0bbe490072044dd42ea3407c2f17b57c5/Lolcode/hello.lol` => `parse-error` (`parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)`)
- `corpus/research/github_language_lolcode/hits_files/BJDG-CM/hello-world/0e05293f4d7a1355235baeb5ce445ca776f1431a/HelloWorld.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 9`)
- `corpus/research/github_language_lolcode/hits_files/BrunoMollo/Backend/26de5fdebdf50b7f111b0dea08d886b3f3826cf5/src/index.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 9`)
- `corpus/research/github_language_lolcode/hits_files/Buttars/LOLCODE-FIBONACCI/00a9a0f17c8ef5630d8539a1017f42535e998e4b/himam.lol` => `parse-error` (`parse-source: syntax error: unexpected ID ("STDIO?") at line 7, col 9`)
- `corpus/research/github_language_lolcode/hits_files/CharlesTabuzo/LOLCODE-interpreter/01d22e03bb5918e2aaed8b89fbd7a72d7d006009/t5.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/research/github_language_lolcode/hits_files/CharlesTabuzo/LOLCODE-interpreter/07301d19a36aa99d785b99530016dcb6386b2d93/t1.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/research/github_language_lolcode/hits_files/Danie-A/CMSC124_Project_LolCode_Interpreter/018c1acf065799595d6f2b1826dfb0ad0b7b1d66/test/arith2.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/research/github_language_lolcode/hits_files/Danie-A/CMSC124_Project_LolCode_Interpreter/01964b65f4db00528321cfac08549bc2bceae39a/test/input.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/research/github_language_lolcode/hits_files/Danie-A/CMSC124_Project_LolCode_Interpreter/02b6e6a6f881f8ab8293f0e32f39aaf59f56c91b/test/project-testcases-fixed/project-testcases-fixed/07_ifelse.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)
- `corpus/research/github_language_lolcode/hits_files/Danie-A/CMSC124_Project_LolCode_Interpreter/050e5cf00c5156ab37446e72967839e0eb8f3c76/test/project-testcases-fixed/project-testcases-fixed/08_switch.lol` => `parse-error` (`parse-source: syntax error: unexpected NEWLINE at line 1, col 4`)


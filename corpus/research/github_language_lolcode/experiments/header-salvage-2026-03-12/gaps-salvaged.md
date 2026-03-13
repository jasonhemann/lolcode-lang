# Language Gap Report (Strict 1.3)

Generated: `Thursday, March 12th, 2026 7:12:40pm`

- JSON source: `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/gaps-salvaged.json`

## Totals

- Corpus files: `739`
- In-scope 1.3 files: `325`
- In-scope parse-ok files: `175`
- In-scope eval-ok files: `118`
- Promoted missing-version files: `0`
- Fixture files: `19`
- Fixture parse-ok files: `19`

### Corpus Header Classes (Original)

- `in-scope-1.3`: `325`
- `non-program-no-leading-hai`: `274`
- `out-of-scope-version-1.2`: `108`
- `out-of-scope-version-1.4`: `17`
- `out-of-scope-hai-without-version`: `3`
- `out-of-scope-version-2.0`: `3`
- `out-of-scope-version-lol`: `2`
- `out-of-scope-version-geek`: `2`
- `out-of-scope-version-got`: `2`
- `out-of-scope-version-1.0`: `1`
- `out-of-scope-version-1.2,how`: `1`
- `out-of-scope-version-1`: `1`

### Corpus Header Classes (Effective For Analysis)

- `in-scope-1.3`: `325`
- `non-program-no-leading-hai`: `274`
- `out-of-scope-version-1.2`: `108`
- `out-of-scope-version-1.4`: `17`
- `out-of-scope-hai-without-version`: `3`
- `out-of-scope-version-2.0`: `3`
- `out-of-scope-version-lol`: `2`
- `out-of-scope-version-geek`: `2`
- `out-of-scope-version-got`: `2`
- `out-of-scope-version-1.0`: `1`
- `out-of-scope-version-1.2,how`: `1`
- `out-of-scope-version-1`: `1`

### In-Scope 1.3 Status Counts

- `parse-ok`: `175`
- `parse-error`: `146`
- `ok`: `118`
- `runtime-error`: `57`
- `lex-error`: `4`

### In-Scope Lex Errors

- `lex-source: unterminated string literal at line 2, col 17`: `4`

### In-Scope Parse Errors

- `parse-source: invalid identifier syntax: "+"`: `20`
- `parse-source: invalid identifier syntax: "MKAY?"`: `17`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 9`: `12`
- `parse-source: invalid identifier syntax: "VAR3."`: `6`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 16`: `5`
- `parse-source: syntax error: unexpected ID ("IPTR") at line 8, col 5`: `5`
- `parse-source: syntax error: unexpected AN at line 7, col 29`: `5`
- `parse-source: syntax error: unexpected OF at line 26, col 50`: `4`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 11`: `4`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`: `3`
- `parse-source: syntax error: unexpected AN at line 11, col 15`: `3`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 17`: `2`
- `parse-source: syntax error: unexpected EOF at line 2, col 1`: `2`
- `parse-source: syntax error: unexpected OF at line 16, col 67`: `2`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 13`: `2`
- `parse-source: syntax error: unexpected AN at line 20, col 15`: `2`
- `parse-source: syntax error: unexpected AN at line 21, col 15`: `2`
- `parse-source: syntax error: unexpected IM at line 54, col 9`: `2`
- `parse-source: syntax error: unexpected AN at line 2, col 23`: `1`
- `parse-source: syntax error: unexpected U at line 5, col 9`: `1`
- `parse-source: syntax error: unexpected OF at line 6, col 67`: `1`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "test")))) at line 3, col 9`: `1`
- `parse-source: invalid identifier syntax: "<<N>>"`: `1`
- `parse-source: syntax error: unexpected I at line 9, col 27`: `1`
- `parse-source: syntax error: unexpected DIFF at line 16, col 43`: `1`
- `parse-source: syntax error: unexpected ID ("k") at line 15, col 43`: `1`
- `parse-source: syntax error: unexpected OF at line 42, col 37`: `1`
- `parse-source: syntax error: unexpected ITZ at line 13, col 1`: `1`
- `parse-source: loop label mismatch: LOOP4 closed by LOOP3`: `1`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 12, col 13`: `1`
- `parse-source: syntax error: unexpected OF at line 25, col 50`: `1`
- `parse-source: syntax error: unexpected A at line 6, col 25`: `1`
- `parse-source: invalid identifier syntax: "//"`: `1`
- `parse-source: syntax error: unexpected UPPIN at line 2, col 14`: `1`
- `parse-source: syntax error: unexpected EOF at line 6, col 1`: `1`
- `parse-source: syntax error: unexpected EOF at line 3, col 1`: `1`
- `parse-source: syntax error: unexpected EOF at line 5, col 1`: `1`
- `parse-source: syntax error: unexpected OF at line 18, col 67`: `1`
- `parse-source: syntax error: unexpected DUZ at line 4, col 21`: `1`
- `parse-source: syntax error: unexpected AN at line 16, col 17`: `1`
- `parse-source: syntax error: unexpected OF at line 14, col 17`: `1`
- `parse-source: invalid declaration type in ITZ A: LIZT (expected TROOF, YARN, NUMBR, NUMBAR, NOOB, or BUKKIT)`: `1`
- `parse-source: syntax error: unexpected AN at line 14, col 18`: `1`
- `parse-source: syntax error: unexpected YR at line 34, col 30`: `1`
- `parse-source: syntax error: unexpected IZ at line 5, col 5`: `1`
- `parse-source: syntax error: unexpected EOF at line 1, col 8`: `1`
- `parse-source: syntax error: unexpected BANG at line 3, col 5`: `1`
- `parse-source: syntax error: unexpected ID ("var") at line 18, col 57`: `1`
- `parse-source: invalid numeric literal: '-' must be adjacent to digits at line 2, col 25`: `1`
- `parse-source: syntax error: unexpected IZ at line 6, col 5`: `1`
- `parse-source: syntax error: unexpected OF at line 22, col 23`: `1`
- `parse-source: invalid identifier syntax: "++"`: `1`
- `parse-source: syntax error: unexpected KTHXBYE at line 26, col 1`: `1`
- `parse-source: syntax error: unexpected ID ("guess") at line 7, col 38`: `1`
- `parse-source: syntax error: unexpected A at line 16, col 34`: `1`
- `parse-source: syntax error: unexpected ID ("MANGO?") at line 2, col 11`: `1`
- `parse-source: syntax error: unexpected AN at line 6, col 18`: `1`
- `parse-source: syntax error: unexpected SUM at line 2, col 12`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 22, col 77`: `1`
- `parse-source: syntax error: unexpected DIFF at line 11, col 43`: `1`
- `parse-source: syntax error: unexpected ID ("HAZ") at line 3, col 5`: `1`
- `parse-source: syntax error: unexpected ID ("NOTHING") at line 25, col 27`: `1`
- `parse-source: syntax error: unexpected ID ("NOTHING") at line 11, col 27`: `1`
- `parse-source: syntax error: unexpected ID ("newCount") at line 19, col 14`: `1`
- `parse-source: syntax error: unexpected NEWLINE at line 19, col 38`: `1`
- `parse-source: syntax error: unexpected ID ("</lolxd>") at line 4, col 33`: `1`

### In-Scope Runtime Errors

- `run-program: unknown identifier: WAZZUP`: `22`
- `run-program: unknown identifier: var`: `7`
- `SUM: cannot cast NOOB to numeric value`: `5`
- `MAEK: cannot cast YARN to numeric value: ""`: `4`
- `BIGGR: cannot cast NOOB to numeric value`: `3`
- `run-program: unknown identifier: i`: `3`
- `evaluation timed out (> 2.0 seconds) or exceeded memory limit`: `2`
- `QUOSHUNT: cannot cast NOOB to numeric value`: `2`
- `run-program: unknown identifier: round_tick`: `1`
- `run-program: unknown identifier: a`: `1`
- `IS-NOW-A: cannot cast YARN to numeric value: " 123"`: `1`
- `run-program: unknown identifier: ii`: `1`
- `run-program: unknown identifier: Z`: `1`
- `SMALLR: cannot cast NOOB to numeric value`: `1`
- `run-program: unknown identifier: bool`: `1`
- `run-program: FOUND YR used outside function`: `1`
- `MAEK: cannot cast YARN to numeric value: "123asd"`: `1`

### In-Scope Issue Triage

- `parse-core-suspect`: `120`
- `runtime-core-suspect`: `57`
- `extension-import-like-identifier`: `17`
- `likely-operator-spelling-drift`: `12`
- `non-spec-line-comment-style`: `1`

### Missing Statement Forms In In-Scope Corpus

- `stmt-object-def`

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

### Used In Fixtures But Not In In-Scope Corpus (Expressions)

- `expr-method-call`

### In-Scope Branch Shape Counts

- `if-total`: `69`
- `loop-total`: `50`
- `loop-with-update`: `43`
- `if-with-else`: `33`
- `loop-with-cond-til`: `24`
- `loop-with-cond-wile`: `19`
- `function-total`: `19`
- `switch-total`: `13`
- `switch-with-default`: `8`
- `if-with-mebbe`: `5`

### Fixture Branch Shape Counts

- `if-total`: `5`
- `function-total`: `5`
- `if-with-else`: `4`
- `loop-with-cond-til`: `3`
- `loop-total`: `3`
- `loop-with-update`: `3`
- `object-total`: `2`
- `method-call-total`: `2`
- `if-with-mebbe`: `2`
- `switch-with-default`: `1`
- `switch-total`: `1`

### Sample Issues

- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/A1rPun/nurture/1374f70cfdf80ab66308a83b7fb076101ae665fe/esolang/lolcode/helloworld.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 11`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/ABCD-rgb/lolcode-interpreter/0f363b3c495ae3215263eead7274f752e4ae6b3e/source code/project-testcases/extra.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/AlexaCabral/CMSC124_project/115b499144bcfa60a91c164fd1ce3307ed14aeed/project-testcases/04_smoosh_assign.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected AN at line 20, col 15`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Danie-A/CMSC124_Project_LolCode_Interpreter/018c1acf065799595d6f2b1826dfb0ad0b7b1d66/test/arith2.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected AN at line 14, col 18`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Danie-A/CMSC124_Project_LolCode_Interpreter/01964b65f4db00528321cfac08549bc2bceae39a/test/input.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Danie-A/CMSC124_Project_LolCode_Interpreter/02b6e6a6f881f8ab8293f0e32f39aaf59f56c91b/test/project-testcases-fixed/project-testcases-fixed/07_ifelse.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Danie-A/CMSC124_Project_LolCode_Interpreter/050e5cf00c5156ab37446e72967839e0eb8f3c76/test/project-testcases-fixed/project-testcases-fixed/08_switch.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Danie-A/CMSC124_Project_LolCode_Interpreter/0b34c1890d8e1e539ce9fcd209f0384178281e70/test/arith.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Danie-A/CMSC124_Project_LolCode_Interpreter/0de09cb0505a2bb05d3d1057e7f54aafa0a7e723/test/boolean.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected NEWLINE at line 22, col 77`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Danie-A/CMSC124_Project_LolCode_Interpreter/175524e708ef629c4cd63e9992378e1cdc9ffa6e/test/arith3.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected AN at line 6, col 18`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Danie-A/CMSC124_Project_LolCode_Interpreter/29239f58a7254add1d963eccca150d51c5f5827b/project/07_ifelse.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/DavidLiuWangli/CMSC124Project/2a53313ff04d727bc9cfc83000a6450c6d6bb027/project/error_debug.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected SUM at line 2, col 12`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/DvaeFroot/cmsc124-lolcode-interpreter/210b7b99fb5efa3905e6bf96ccd41f1799c08ebc/project-examples/06_comparison.lol` (`eval`, triage=`runtime-core-suspect`): `BIGGR: cannot cast NOOB to numeric value`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/EbrahimGabriel/lolcode-interpreter/0d853969af5c723ce4af8696db1c1ba90920ebc5/project-testcases/04_smoosh_assign.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/GeSHi/coderepo/a6d3fe9144798c7daebd49ad6d727a26bc6d880c/lolcode/pi.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: FOUND YR used outside function`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Holarse-Linuxgaming/ashley-madison-simulator/a2841dd771d684f20e3cd672f54bb1f527d302c5/ircbot.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 17`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/IrisSec/IrisCTF-2025-Challenges/0a44522ce6f798560d1c70789c5fde59deab920f/rev-lifetime/src/lci/test/1.3-Tests/3-Types/5-String/2-Syntax/3-MustHaveClosingQuote/test.lol` (`lex`, triage=`parse-core-suspect`): `lex-source: unterminated string literal at line 2, col 17`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/IrisSec/IrisCTF-2025-Challenges/0b028a866ec23495c3c21240518328938d69d7ea/rev-lifetime/src/lci/test/1.3-Tests/7-Operators/17-ExplicitCast/4-ToFloat/5-FromString/2-EmptyString/test.lol` (`eval`, triage=`runtime-core-suspect`): `MAEK: cannot cast YARN to numeric value: ""`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/IrisSec/IrisCTF-2025-Challenges/1032a52ed4bae9c8e77d531d68365b43b900a33a/rev-lifetime/src/lci/test/1.3-Tests/12-Arrays/5-FunctionStorage/test.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected AN at line 7, col 29`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/IrisSec/IrisCTF-2025-Challenges/1194dd8dcd16be7562941020c752552e428e468f/rev-lifetime/src/lci/test/1.3-Tests/10-Loops/5-While/test.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: var`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/JasonBock/LOLCode.net/02b33fcb17510559510a6200a35ffed599f66e50/LOLCode.Compiler.Tests/Samples/visible.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "VAR3."`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/JiroKristoferTipan/CMSC-124-PROJECT-bahay-norio-tipan/0a924978760158a50bc35beb8f0d855dab312848/source code/project-testcases/test1.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/JiroKristoferTipan/CMSC-124-PROJECT-bahay-norio-tipan/26f73f402f83cfa5e3d8b59a2e9805be5fe84b56/source code/project-testcases/05_bool.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Keith-S-Thompson/fizzbuzz-polyglot/b656ca3d52c366929c9d70ee6948f4f22a392472/fizzbuzz.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: i`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/KelvinBeliber/CMSC-124-Project/098f5ce5cdcfaef6c9c0f93ae61aeafa764d32b7/src/testcases/10_functions.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/KelvinBeliber/CMSC-124-Project/2479e1d80a56549a6fdb454136dedffea20da66c/src/testcases/08_switch.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "+"`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/KelvinBeliber/CMSC-124-Project/284225905c57b14ea7c83b11aa145790ce4aa4fc/src/testcases/09_loops.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Kenneth-Olano/cmsc124_project/23aadd4a1a376856ccfc8bb4f8cda9eb75e2cf8d/testcases/08_switch.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: WAZZUP`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Kimbsy/lolcode/9814a249b649d7e6e17357fd23b6f078e26fc840/ICANHAZPRIME.lol` (`eval`, triage=`runtime-core-suspect`): `QUOSHUNT: cannot cast NOOB to numeric value`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Kimbsy/lolcode/e96fc6b9ef5572d909d577df504640edb7962d3d/FIZZBUZZ.lol` (`eval`, triage=`runtime-core-suspect`): `SMALLR: cannot cast NOOB to numeric value`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/LeartS/loleuler/2093180b305267adace2d9b5dafbb282365624d4/031.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected A at line 16, col 34`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Meme1079/LOLSCRIPT/2611014cc094f727fa778195c5445875bb0d53ac/scripts/LOLCODE.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected BANG at line 3, col 5`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/MonliH/lulz/00c7a8b81633cd0ef8b1bcffdcf2fe00d2827048/perfs/fib/fib.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected IZ at line 5, col 5`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/MonliH/lulz/0f6975299dbc30bc4d88b97b87da4dde9d410da9/perfs/fib/fib.lci.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "<<N>>"`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/MonliH/lulz/0fcc1cbb83e6648888c09b0aee58802027d2585a/tests/lizt/fail_frunt_out_of_range.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid declaration type in ITZ A: LIZT (expected TROOF, YARN, NUMBR, NUMBAR, NOOB, or BUKKIT)`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/MonliH/lulz/1a7ad234e4f16f9e195771b89de6245d00b70c9e/tests/exprs/casts/fail_string_to_int.lol` (`eval`, triage=`runtime-core-suspect`): `MAEK: cannot cast YARN to numeric value: "123asd"`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/MonliH/lulz/1afc5a11ba9c8ce22343773658ae016bf5bbf62e/tests/exprs/ops/math/uppin.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected UPPIN at line 2, col 14`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/NTMTech/gsb_extranet/2c1474d08515369e694f54980682cf1a87781e3a/salut.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected EOF at line 2, col 1`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/Prithvirajbilla/helloworld/9fff025e176d84a443e6737bfd81862765bdc593/lolcode.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 9`
- `corpus/research/github_language_lolcode/experiments/header-salvage-2026-03-12/hits_files_salvaged/ReciHub/FunnyAlgorithms/0f383c3caee1c00b637ee5ff9d9dc253e7ae1b5c/Factorial/factorial.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 9`


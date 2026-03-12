# Language Gap Report (Strict 1.3)

Generated: `Thursday, March 12th, 2026 6:25:02pm`

- JSON source: `corpus/research/github_language_lolcode/hits-language-gaps.json`

## Totals

- Corpus files: `739`
- In-scope 1.3 files: `141`
- In-scope parse-ok files: `89`
- In-scope eval-ok files: `72`
- Promoted missing-version files: `0`
- Fixture files: `19`
- Fixture parse-ok files: `19`

### Corpus Header Classes (Original)

- `non-program-no-leading-hai`: `303`
- `in-scope-1.3`: `141`
- `out-of-scope-version-1.2`: `130`
- `out-of-scope-hai-without-version`: `128`
- `out-of-scope-version-1.4`: `23`
- `out-of-scope-version-2.0`: `3`
- `out-of-scope-version-1.0`: `2`
- `out-of-scope-version-lol`: `2`
- `out-of-scope-version-geek`: `2`
- `out-of-scope-version-got`: `2`
- `out-of-scope-version-1.2,how`: `1`
- `out-of-scope-version-it`: `1`
- `out-of-scope-version-1`: `1`

### Corpus Header Classes (Effective For Analysis)

- `non-program-no-leading-hai`: `303`
- `in-scope-1.3`: `141`
- `out-of-scope-version-1.2`: `130`
- `out-of-scope-hai-without-version`: `128`
- `out-of-scope-version-1.4`: `23`
- `out-of-scope-version-2.0`: `3`
- `out-of-scope-version-1.0`: `2`
- `out-of-scope-version-lol`: `2`
- `out-of-scope-version-geek`: `2`
- `out-of-scope-version-got`: `2`
- `out-of-scope-version-1.2,how`: `1`
- `out-of-scope-version-it`: `1`
- `out-of-scope-version-1`: `1`

### In-Scope 1.3 Status Counts

- `parse-ok`: `89`
- `ok`: `72`
- `parse-error`: `48`
- `runtime-error`: `17`
- `lex-error`: `4`

### In-Scope Lex Errors

- `lex-source: unterminated string literal at line 2, col 17`: `4`

### In-Scope Parse Errors

- `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`: `24`
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 16`: `5`
- `parse-source: syntax error: unexpected AN at line 7, col 29`: `5`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 11`: `3`
- `parse-source: syntax error: unexpected IM at line 54, col 9`: `2`
- `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "test")))) at line 3, col 9`: `1`
- `parse-source: invalid identifier syntax: "<<N>>"`: `1`
- `parse-source: syntax error: unexpected BANG at line 3, col 5`: `1`
- `parse-source: syntax error: unexpected IZ at line 5, col 5`: `1`
- `parse-source: syntax error: unexpected ID ("guess") at line 7, col 38`: `1`
- `parse-source: syntax error: unexpected A at line 16, col 34`: `1`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`: `1`
- `parse-source: syntax error: unexpected I at line 9, col 27`: `1`
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 12, col 13`: `1`

### In-Scope Runtime Errors

- `SUM: cannot cast NOOB to numeric value`: `5`
- `run-program: unknown identifier: var`: `5`
- `MAEK: cannot cast YARN to numeric value: ""`: `4`
- `IS-NOW-A: cannot cast YARN to numeric value: " 123"`: `1`
- `run-program: unknown identifier: Z`: `1`
- `evaluation timed out (> 2.0 seconds) or exceeded memory limit`: `1`

### In-Scope Issue Triage

- `parse-core-suspect`: `52`
- `runtime-core-suspect`: `17`

### Missing Statement Forms In In-Scope Corpus

- `stmt-object-def`
- `stmt-switch`

### Missing Expression Forms In In-Scope Corpus

- `expr-method-call`

### Missing Binary Operators In In-Scope Corpus

- `BOTH OF`
- `SMALLR OF`
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

- `loop-total`: `12`
- `loop-with-update`: `10`
- `if-total`: `8`
- `loop-with-cond-wile`: `5`
- `loop-with-cond-til`: `5`
- `if-with-else`: `3`
- `function-total`: `1`

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

- `corpus/research/github_language_lolcode/hits_files/A1rPun/nurture/1374f70cfdf80ab66308a83b7fb076101ae665fe/esolang/lolcode/helloworld.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/IrisSec/IrisCTF-2025-Challenges/0a44522ce6f798560d1c70789c5fde59deab920f/rev-lifetime/src/lci/test/1.3-Tests/3-Types/5-String/2-Syntax/3-MustHaveClosingQuote/test.lol` (`lex`, triage=`parse-core-suspect`): `lex-source: unterminated string literal at line 2, col 17`
- `corpus/research/github_language_lolcode/hits_files/IrisSec/IrisCTF-2025-Challenges/0b028a866ec23495c3c21240518328938d69d7ea/rev-lifetime/src/lci/test/1.3-Tests/7-Operators/17-ExplicitCast/4-ToFloat/5-FromString/2-EmptyString/test.lol` (`eval`, triage=`runtime-core-suspect`): `MAEK: cannot cast YARN to numeric value: ""`
- `corpus/research/github_language_lolcode/hits_files/IrisSec/IrisCTF-2025-Challenges/1032a52ed4bae9c8e77d531d68365b43b900a33a/rev-lifetime/src/lci/test/1.3-Tests/12-Arrays/5-FunctionStorage/test.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected AN at line 7, col 29`
- `corpus/research/github_language_lolcode/hits_files/IrisSec/IrisCTF-2025-Challenges/1194dd8dcd16be7562941020c752552e428e468f/rev-lifetime/src/lci/test/1.3-Tests/10-Loops/5-While/test.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: var`
- `corpus/research/github_language_lolcode/hits_files/Keith-S-Thompson/fizzbuzz-polyglot/b656ca3d52c366929c9d70ee6948f4f22a392472/fizzbuzz.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/LeartS/loleuler/2093180b305267adace2d9b5dafbb282365624d4/031.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected A at line 16, col 34`
- `corpus/research/github_language_lolcode/hits_files/Meme1079/LOLSCRIPT/2611014cc094f727fa778195c5445875bb0d53ac/scripts/LOLCODE.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected BANG at line 3, col 5`
- `corpus/research/github_language_lolcode/hits_files/MonliH/lulz/00c7a8b81633cd0ef8b1bcffdcf2fe00d2827048/perfs/fib/fib.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected IZ at line 5, col 5`
- `corpus/research/github_language_lolcode/hits_files/MonliH/lulz/0f6975299dbc30bc4d88b97b87da4dde9d410da9/perfs/fib/fib.lci.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: invalid identifier syntax: "<<N>>"`
- `corpus/research/github_language_lolcode/hits_files/MonliH/lulz/0fcc1cbb83e6648888c09b0aee58802027d2585a/tests/lizt/fail_frunt_out_of_range.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/MonliH/lulz/1373ddc04f9a0404dd211942980040d379e9249f/tests/strings/fail_uni_norm_1.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/MonliH/lulz/166c3901974fffde69bed2f2680aa9951e453cf6/tests/control/conditionals/if_scoping.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/MonliH/lulz/1a7ad234e4f16f9e195771b89de6245d00b70c9e/tests/exprs/casts/fail_string_to_int.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/MonliH/lulz/1afc5a11ba9c8ce22343773658ae016bf5bbf62e/tests/exprs/ops/math/uppin.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/MonliH/lulz/1b82430684ba711dde53b297096014678f3f7161/tests/exprs/ops/math/sum.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/MonliH/lulz/1bb68a971380550d9ec10aee5672a5008f568b39/tests/functions/scope_basic.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/Th3-0b3l1sk/CTFs/0b028a866ec23495c3c21240518328938d69d7ea/ASCWG25/finals/Truth/Artfuscator/elvm/lci/test/1.3-Tests/7-Operators/17-ExplicitCast/4-ToFloat/5-FromString/2-EmptyString/test.lol` (`eval`, triage=`runtime-core-suspect`): `MAEK: cannot cast YARN to numeric value: ""`
- `corpus/research/github_language_lolcode/hits_files/acmeism/RosettaCodeData/0bdc2228dc5b044e8fbd2b35b2a0f5f0c720ed5b/Task/Happy-numbers/LOLCODE/happy-numbers.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/aduros/trollcat/54b23f4bbcc668cfba9461ec506cb9fff7755040/trollcat.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/approvers/RADWIMPS/dca3a2f5c688953b856869ac11000f4385b1c379/RADWIMPS.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 3, col 9`
- `corpus/research/github_language_lolcode/hits_files/belkadan/lolcode-rb/08a9d10e5bf51e2c92d12285bf6e3063986b4cf0/test/feature/maek.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected STRING ((yarn-template (list (yarn-part-text "test")))) at line 3, col 9`
- `corpus/research/github_language_lolcode/hits_files/belkadan/lolcode-rb/10ff0efa8247c757e341d04d14d1068d8bd386c1/examples/animal.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("guess") at line 7, col 38`
- `corpus/research/github_language_lolcode/hits_files/bluebat/mt9x9/f4d58198aeb54de6d3e4d57ea50af6560b44a409/mt9x9.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/chutasano/lolcode/55db1fcf06a1b4477117054ff7fa12341a791c45/quick_sort.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 11`
- `corpus/research/github_language_lolcode/hits_files/chutasano/lolcode/a821539c60f1c72ca3d6b27ade7ce0d9ba89b624/final.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 11`
- `corpus/research/github_language_lolcode/hits_files/chutasano/lolcode/ce320a95ad9152868bf457a1f20088f91fe86d87/make_array.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 11`
- `corpus/research/github_language_lolcode/hits_files/donno2048/Quines/0cec9ca7b3ef1c6cfd73085c1e393b11d4c94d61/quin.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: syntax error: unexpected IM at line 54, col 9`
- `corpus/research/github_language_lolcode/hits_files/e9-o9/ro9se/0bdc2228dc5b044e8fbd2b35b2a0f5f0c720ed5b/Task/Happy-numbers/LOLCODE/happy-numbers.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/jocelyne8/lolcode/028a0af375342271bad2c6c739f1c6a740f20eda/rosalind/022_rna_splicing.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/jocelyne8/lolcode/04fef02a5034a4d17657a3bbf5ca6a4cacd8d71b/rosalind/029_signed_permutations.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/jocelyne8/lolcode/0a583a3ec72024742cf5560e4c76f1efce011ea8/lib/fasta_read_functions.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/jocelyne8/lolcode/135918fb243d7bf49c36e08e6779af5d4e750e9f/lib/string_functions.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/jocelyne8/lolcode/15defe4241a34604b4a4b59aeeecae46c6de0cee/rosalind/024_longest_subsequence.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/jocelyne8/lolcode/1f05f2c205cb3bd7367674a74d0a85bdb3ca35b0/rosalind/012_overlap_graph.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/jocelyne8/lolcode/267be5bfeca6499a1a89414eea149466a532cb4f/rosalind/005_gc_content.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/jocelyne8/lolcode/294ee5381e2838b79a808111ecc8580613f00561/rosalind/015_independent_alleles.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/jocelyne8/lolcode/2a73889ff8146c0a7d871fe4be8d9240899e6d55/rosalind/026_rna_perfect_matching.lol` (`parse`, triage=`parse-core-suspect`): `parse-source: program must begin with HAI opener (no leading comments or tokens before HAI)`
- `corpus/research/github_language_lolcode/hits_files/justinmeza/lci/0b028a866ec23495c3c21240518328938d69d7ea/test/1.3-Tests/7-Operators/17-ExplicitCast/4-ToFloat/5-FromString/2-EmptyString/test.lol` (`eval`, triage=`runtime-core-suspect`): `MAEK: cannot cast YARN to numeric value: ""`
- `corpus/research/github_language_lolcode/hits_files/justinmeza/lci/1194dd8dcd16be7562941020c752552e428e468f/test/1.3-Tests/10-Loops/5-While/test.lol` (`eval`, triage=`runtime-core-suspect`): `run-program: unknown identifier: var`


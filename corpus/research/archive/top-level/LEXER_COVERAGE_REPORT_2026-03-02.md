# Lexer Coverage Report

Generated: `Monday, March 2nd, 2026 12:52:28pm`

## Inputs

- Fixture `.lol` files: `16`
- Corpus `.lol` files: `223`
- Promoted `.lol` files included: `120`
- Include promoted: `#t`

### Test Submodule Status Counts

- `ok`: `3`

### Fixture Lex Status Counts

- `ok`: `16`

### Corpus Lex Status Counts

- `ok`: `204`
- `lex-error`: `19`

### Promoted Lex Status Counts

- `ok`: `113`
- `lex-error`: `7`

### Lexer Branch Hits (Total)

- `scanner/ws`: `120308`
- `scanner/word/ok`: `80699`
- `word->tokens/word`: `77108`
- `skip-comment-tail!/char`: `25845`
- `scan-string-tail!/plain-char`: `23532`
- `scanner/newline/lf`: `15410`
- `skip-block-comment!/word-char`: `13870`
- `skip-block-comment!/delimiter`: `6717`
- `scanner/newline/comma`: `2755`
- `word->tokens/number`: `2643`
- `scanner/string`: `2163`
- `scan-string-tail!/end-string`: `2083`
- `scanner/pending`: `991`
- `word->tokens/split-slot-z`: `991`
- `scanner/word/comment`: `800`
- `word->tokens/comment`: `800`
- `skip-comment-tail!/newline`: `796`
- `scan-string-tail!/start-escape`: `581`
- `scanner/eof`: `387`
- `scan-string-tail!/escaped-unknown`: `382`
- `scanner/newline/crlf`: `323`
- `skip-line-continuation!/lf`: `262`
- `word->tokens/line-continuation`: `223`
- `scanner/word/line-continuation`: `223`
- `scan-string-tail!/codepoint/char`: `140`
- `word->tokens/block-comment`: `92`
- `scanner/word/block-comment`: `92`
- `skip-block-comment!/found-tldr`: `81`
- `scan-string-tail!/escaped-newline`: `63`
- `scan-string-tail!/escaped-quote/end-string`: `51`
- `scanner/word/ok+line-continuation`: `43`
- `word->tokens/ok+line-continuation`: `43`
- `skip-line-continuation!/space-or-tab`: `42`
- `scan-string-tail!/format-placeholder/char`: `34`
- `scan-string-tail!/escaped-codepoint`: `30`
- `scan-string-tail!/codepoint/end`: `30`
- `lex-error`: `29`
- `scan-string-tail!/newline`: `27`
- `scan-string-tail!/escaped-tab`: `21`
- `scan-string-tail!/escaped-quote/literal`: `18`
- `skip-block-comment!/eof`: `11`
- `scan-string-tail!/escaped-placeholder`: `9`
- `scan-string-tail!/format-placeholder/end`: `8`
- `scan-string-tail!/escaped-colon`: `5`
- `skip-comment-tail!/eof`: `4`
- `skip-line-continuation!/other`: `4`
- `scan-string-tail!/escaped-bell`: `2`
- `scan-string-tail!/codepoint/invalid-range`: `1`
- `scan-string-tail!/format-placeholder/newline`: `1`

### Lexer Branches Never Hit (Tests + Fixtures + Corpus + Promoted)

- `scan-string-tail!/codepoint/eof`
- `scan-string-tail!/codepoint/invalid-hex`
- `scan-string-tail!/codepoint/newline`
- `scan-string-tail!/eof`
- `scan-string-tail!/format-placeholder/eof`
- `scanner/newline/cr`
- `skip-line-continuation!/cr`
- `skip-line-continuation!/crlf`
- `skip-line-continuation!/eof`

### Sample Fixture Lex Errors

- (none)

### Sample Corpus Lex Errors

- `corpus/tier2/ai2001-sc-lolcode/files/LICENSE-GPL.lol`: `lex-source: unterminated string literal at line 388, col 60`
- `corpus/tier2/ai2001-sc-lolcode/files/LICENSE-GPL3.lol`: `lex-source: unterminated string literal at line 388, col 60`
- `corpus/tier2/ai2001-sc-lolcode/files/LICENSE.lol`: `lex-source: unterminated string literal at line 388, col 60`
- `corpus/tier2/ai2001-sc-lolcode/files/OldVersions/LICENSE/GPL3/LICENSE-GPL3_V1.lol`: `lex-source: unterminated string literal at line 388, col 60`
- `corpus/tier2/ai2001-sc-lolcode/files/OldVersions/LICENSE/GPL3/LICENSE-GPL_V1.lol`: `lex-source: unterminated string literal at line 388, col 60`
- `corpus/tier2/ai2001-sc-lolcode/files/OldVersions/LICENSE/GPL3/LICENSE_V1.lol`: `lex-source: unterminated string literal at line 388, col 60`
- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/05_bool.lol`: `lex-source: unterminated string literal at line 8, col 31`
- `corpus/tier2/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/05_bool.lol`: `lex-source: unterminated string literal at line 6, col 27`
- `corpus/tier2/garthendrich-lolcode-interpreter/files/sample_codes/05_bool.lol`: `lex-source: unterminated string literal at line 6, col 27`
- `corpus/tier2/learn-lolcode/files/LICENSE-GPL.lol`: `lex-source: unterminated string literal at line 388, col 60`

### Sample Promoted Lex Errors

- `corpus/research/promoted-1_3-programs/bernardjezua-lolcode-interpreter/files/testcases/final/05_bool.lol`: `lex-source: unterminated string literal at line 8, col 31`
- `corpus/research/promoted-1_3-programs/coleenagsao-python-lolcode-interpreter/files/lolcode-imports/05_bool.lol`: `lex-source: unterminated string literal at line 6, col 27`
- `corpus/research/promoted-1_3-programs/garthendrich-lolcode-interpreter/files/sample_codes/05_bool.lol`: `lex-source: unterminated string literal at line 6, col 27`
- `corpus/research/promoted-1_3-programs/lolcode-py-cmsc124/files/project-examples/05_bool.lol`: `lex-source: unterminated string literal at line 6, col 27`
- `corpus/research/promoted-1_3-programs/lolcode-py-sada/files/CMSC_124_testcases/05_bool.lol`: `lex-source: unterminated string literal at line 8, col 27`
- `corpus/research/promoted-1_3-programs/nicodecastro-lolcode-interpreter/files/tests/05_bool.lol`: `lex-source: unterminated string literal at line 8, col 31`
- `corpus/research/promoted-1_3-programs/sallysanban-lolcode-interpreter/files/Project 3/EZR_B-4L/source code/Test Files/05_bool.lol`: `lex-source: unterminated string literal at line 6, col 27`


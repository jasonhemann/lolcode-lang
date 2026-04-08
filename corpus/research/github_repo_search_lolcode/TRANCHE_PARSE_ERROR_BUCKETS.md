# Broad-Search Tranche Parse Error Buckets

- Generated: 2026-04-01T23:40:06Z
- Source tag: `github-repo-search-lolcode-curated-2026-04-01`
- Eval source: `corpus/research/tier2-eval-classified.json`
- New-tranche parse errors: `1201`
- Imported negative-fixture overlay: `81`

Primary buckets are language-cause buckets, not provenance buckets.
The imported negative-fixture overlay is a separate count of rows whose
paths came from bundled conformance/spec-negative suites.

## Bucket Counts

| Bucket | Count | Example |
|---|---:|---|
| `split-hai-header` | `486` | `corpus/tier2/aagoshi-lolcode/files/customtestcases/Declaration.lol` |
| `leading-material-before-hai` | `475` | `corpus/tier2/aagoshi-lolcode/files/actual testcases/ifelse.lol` |
| `unsupported-version-1.2` | `75` | `corpus/tier2/aagoshi-lolcode/files/sample codes lol/arith.lol` |
| `unsupported-version-1.4` | `2` | `corpus/tier2/d-stew-lmaonade-stand/files/lmaonade-stand.lol` |
| `extension-import-or-question-id` | `38` | `corpus/tier2/boxel-rebound-lolcode/files/lol.lol` |
| `string-literal-at-non-expression-site` | `16` | `corpus/tier2/belkadan-lolcode-rb/files/examples/huffman.lol` |
| `strict-switch-negative-fixture` | `7` | `corpus/tier2/d-stew-lmaonade-stand/files/test/1.3-Tests/8-Conditionals/2-Switch/4-MixedTypes/test.lol` |
| `invalid-identifier-syntax` | `3` | `corpus/tier2/ksumallo-lolspeaker/files/project-testcases/test_2.lol` |
| `invalid-numeric-literal` | `4` | `corpus/tier2/d-stew-lmaonade-stand/files/test/1.3-Tests/3-Types/3-Integer/2-MustHaveAdjacentHyphen/test.lol` |
| `post-kthxbye-material` | `4` | `corpus/tier2/d-stew-lmaonade-stand/files/test/1.3-Tests/2-Comments/1-SingleLine/5-AfterKTHXBYE/test.lol` |
| `implicit-mkay-boundary` | `1` | `corpus/tier2/nadineanareta-lolcode-interpreter/files/testcases/bonus3_loop_nesting.lol` |
| `other-grammar-drift` | `90` | `corpus/tier2/belkadan-lolcode-rb/files/examples/animal.lol` |

## Top Parse-Error Repos

| Label | Parse errors |
|---|---:|
| `monlih-lulz` | `124` |
| `danie-a-cmsc124-project-lolcode-interpreter` | `59` |
| `lorenzggabriel-witlang-lolcode-interpreter` | `54` |
| `krispypatata-lolcode-interpreter-py` | `48` |
| `lolcodepp-lci` | `37` |
| `aagoshi-lolcode` | `36` |
| `jocelyne8-lolcode` | `34` |
| `rodflores27-cmsc124project` | `32` |
| `belkadan-lolcode-rb` | `30` |
| `roxanneypr-lolcode-interpreter` | `30` |
| `d-stew-lmaonade-stand` | `29` |
| `redcapital-layo` | `26` |
| `abcd-rgb-lolcode-interpreter` | `20` |
| `cvpua-cmsc124-project` | `20` |
| `camanzanido-lolcode-interpreter` | `19` |
| `darylldan-lolcode-testcases` | `19` |
| `mattleibow-dotnet-lolcode` | `18` |
| `mldamalerio-lolcode-interpreter` | `18` |
| `simark-lolc` | `18` |
| `nadineanareta-lolcode-interpreter` | `17` |

## Notes

- `split-hai-header` is the classic bare-`HAI`/newline-open form that strict `1.3` rejects.
- `leading-material-before-hai` captures files with prose, comments, or other tokens before the opener.
- `unsupported-version-*` is version mismatch, not general parser confusion.
- `extension-import-or-question-id` mostly reflects `CAN HAS ...?` or similar non-strict extension syntax.
- `other-grammar-drift` is the remaining long tail of noncanonical operator/keyword/statement forms.

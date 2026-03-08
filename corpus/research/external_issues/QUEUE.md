# External Regression Queue

- Generated at: 2026-03-08T05:25:45Z
- Source catalog: `corpus/tier2/CANDIDATE_REPOS.tsv`
- Total issues+PR items collected: 2276
- Scope counts (all items): core=493, extension=17, unknown=1766
- Candidate reproducible regression items: 493
- Candidate core-1.2/1.3 items: 493
- Wave size: 10
- Total waves currently: 50
- Warning: partial fetch failures during sync: 30

## How To Process All Items

1. Iterate `wave = 1..50` in `candidate_repros.tsv`.
2. For each row, create a minimal fixture/test + expected behavior.
3. Classify result in triage as `fixed-here`, `known-divergence`, `spec-ambiguous`, or `out-of-spec`.

## Wave Counts

- Wave 1: 10 items
- Wave 2: 10 items
- Wave 3: 10 items
- Wave 4: 10 items
- Wave 5: 10 items
- Wave 6: 10 items
- Wave 7: 10 items
- Wave 8: 10 items
- Wave 9: 10 items
- Wave 10: 10 items
- Wave 11: 10 items
- Wave 12: 10 items
- Wave 13: 10 items
- Wave 14: 10 items
- Wave 15: 10 items
- Wave 16: 10 items
- Wave 17: 10 items
- Wave 18: 10 items
- Wave 19: 10 items
- Wave 20: 10 items
- Wave 21: 10 items
- Wave 22: 10 items
- Wave 23: 10 items
- Wave 24: 10 items
- Wave 25: 10 items
- Wave 26: 10 items
- Wave 27: 10 items
- Wave 28: 10 items
- Wave 29: 10 items
- Wave 30: 10 items
- Wave 31: 10 items
- Wave 32: 10 items
- Wave 33: 10 items
- Wave 34: 10 items
- Wave 35: 10 items
- Wave 36: 10 items
- Wave 37: 10 items
- Wave 38: 10 items
- Wave 39: 10 items
- Wave 40: 10 items
- Wave 41: 10 items
- Wave 42: 10 items
- Wave 43: 10 items
- Wave 44: 10 items
- Wave 45: 10 items
- Wave 46: 10 items
- Wave 47: 10 items
- Wave 48: 10 items
- Wave 49: 10 items
- Wave 50: 3 items

## Top 30 Candidates

- [rank 1, wave 1] justinmeza/lci issue #43: [SIGSEV](https://github.com/justinmeza/lci/issues/43) [runtime-safety, core-1.2-1.3, score=125]
- [rank 2, wave 1] justinmeza/lci issue #47: [segfault or abort with IT in small programs](https://github.com/justinmeza/lci/issues/47) [runtime-safety, core-1.2-1.3, score=125]
- [rank 3, wave 1] justinmeza/lci issue #54: [Shebang without trailing newline causes buffer overflow (segfault)](https://github.com/justinmeza/lci/issues/54) [runtime-safety, core-1.2-1.3, score=125]
- [rank 4, wave 1] justinmeza/lci issue #55: [Failed realloc during program buffering causes segfault](https://github.com/justinmeza/lci/issues/55) [runtime-safety, core-1.2-1.3, score=125]
- [rank 5, wave 1] justinmeza/lci issue #79: [Out of Bounds Read and Null Pointer Dereference in LCI Version 0.10.5](https://github.com/justinmeza/lci/issues/79) [runtime-safety, core-1.2-1.3, score=125]
- [rank 6, wave 1] justinmeza/lci pr #50: [Fix a double free of the implicit variable](https://github.com/justinmeza/lci/pull/50) [runtime-safety, core-1.2-1.3, score=125]
- [rank 7, wave 1] justinmeza/lci commit #c3ded8ddab5c8da3021b21f35c56ff747ce63222: [Fixed a segfault when attempting to declare a function in a non-array type value.](https://github.com/justinmeza/lci/commit/c3ded8ddab5c8da3021b21f35c56ff747ce63222) [runtime-safety, core-1.2-1.3, score=115]
- [rank 8, wave 1] justinmeza/lci issue #33: [segfault](https://github.com/justinmeza/lci/issues/33) [runtime-safety, core-1.2-1.3, score=115]
- [rank 9, wave 1] justinmeza/lci pr #24: [Defensive strategy that prevents a range of possible null pointer errors...](https://github.com/justinmeza/lci/pull/24) [runtime-safety, core-1.2-1.3, score=115]
- [rank 10, wave 1] jD91mZM2/rust-lci commit #9f21cab3a1005d9022ec3ad63d2213005025c432: [Fix yet another panic & lol quines](https://github.com/jD91mZM2/rust-lci/commit/9f21cab3a1005d9022ec3ad63d2213005025c432) [runtime-safety, core-1.2-1.3, score=105]
- [rank 11, wave 2] jpcarreon/loco commit #6d346bc975b2d81a96274b9baa8a2c8be6474e90: [Fix some errors which causes program to crash.](https://github.com/jpcarreon/loco/commit/6d346bc975b2d81a96274b9baa8a2c8be6474e90) [runtime-safety, core-1.2-1.3, score=105]
- [rank 12, wave 2] jpcarreon/loco commit #bc669755496e740459b6de2688de258021924a71: [fixed program crashing when KTHXBYE is not present](https://github.com/jpcarreon/loco/commit/bc669755496e740459b6de2688de258021924a71) [runtime-safety, core-1.2-1.3, score=105]
- [rank 13, wave 2] jpcarreon/loco commit #ddd4086f141358a5c1b9bd0b1e2669e14aaad850: [fix bug which causes the program to crash when no idToken is given](https://github.com/jpcarreon/loco/commit/ddd4086f141358a5c1b9bd0b1e2669e14aaad850) [runtime-safety, core-1.2-1.3, score=105]
- [rank 14, wave 2] justinmeza/lci issue #13: [unexpected error message with undefined variable interpolation](https://github.com/justinmeza/lci/issues/13) [language, core-1.2-1.3, score=105]
- [rank 15, wave 2] justinmeza/lci issue #23: [String and colon](https://github.com/justinmeza/lci/issues/23) [language, core-1.2-1.3, score=105]
- [rank 16, wave 2] justinmeza/lci issue #39: [Invalid Unicode code points are accepted](https://github.com/justinmeza/lci/issues/39) [language, core-1.2-1.3, score=105]
- [rank 17, wave 2] justinmeza/lci issue #56: [Colon and quotation mark conflict in strings](https://github.com/justinmeza/lci/issues/56) [language, core-1.2-1.3, score=105]
- [rank 18, wave 2] justinmeza/lci issue #57: [Octal NUMBR works when negative, but not positive](https://github.com/justinmeza/lci/issues/57) [language, core-1.2-1.3, score=105]
- [rank 19, wave 2] justinmeza/lci issue #58: [NUMBAR doesn't always work with line continuation](https://github.com/justinmeza/lci/issues/58) [language, core-1.2-1.3, score=105]
- [rank 20, wave 2] justinmeza/lci issue #59: [EOL doesn't replace MKAY when calling a variadic function](https://github.com/justinmeza/lci/issues/59) [language, core-1.2-1.3, score=105]
- [rank 21, wave 3] justinmeza/lci issue #60: [Function can read and modify variables in outside scope](https://github.com/justinmeza/lci/issues/60) [language, core-1.2-1.3, score=105]
- [rank 22, wave 3] justinmeza/lci issue #62: [BTW may not appear on the same line as TLDR](https://github.com/justinmeza/lci/issues/62) [language, core-1.2-1.3, score=105]
- [rank 23, wave 3] justinmeza/lci issue #71: [Loops always create a loop-scope variable and initialize it to 0](https://github.com/justinmeza/lci/issues/71) [language, core-1.2-1.3, score=105]
- [rank 24, wave 3] justinmeza/lci issue #78: [Functions of NOOB very limited](https://github.com/justinmeza/lci/issues/78) [language, core-1.2-1.3, score=105]
- [rank 25, wave 3] justinmeza/lci pr #52: [Fixed loop creation of variable even when present](https://github.com/justinmeza/lci/pull/52) [language, core-1.2-1.3, score=105]
- [rank 26, wave 3] JasonBock/LOLCode.net issue #7: [Try Removing Different Parser Types](https://github.com/JasonBock/LOLCode.net/issues/7) [language, core-1.2-1.3, score=95]
- [rank 27, wave 3] justinmeza/httpd.lol pr #3: [Added doctype and head to HTML document](https://github.com/justinmeza/httpd.lol/pull/3) [language, core-1.2-1.3, score=95]
- [rank 28, wave 3] justinmeza/lci commit #0ec7a7f583f6dd93a5fb152d2391a9df30ffdd6d: [converted build toolchain to CMake](https://github.com/justinmeza/lci/commit/0ec7a7f583f6dd93a5fb152d2391a9df30ffdd6d) [language, core-1.2-1.3, score=95]
- [rank 29, wave 3] justinmeza/lci commit #1fc16cd54aca602084a8ebbb467d5101d44516ec: [using type name instead of identifier](https://github.com/justinmeza/lci/commit/1fc16cd54aca602084a8ebbb467d5101d44516ec) [language, core-1.2-1.3, score=95]
- [rank 30, wave 3] justinmeza/lci commit #233aa9481d141bcafe0eaefe9fb44006919189c2: [Added exception handlers to the parser; made SMOOSH require MKAY](https://github.com/justinmeza/lci/commit/233aa9481d141bcafe0eaefe9fb44006919189c2) [language, core-1.2-1.3, score=95]

## Output Files

- `/Users/jhemann/Code/lolcode-lang/corpus/research/external_issues/all_items.json`
- `/Users/jhemann/Code/lolcode-lang/corpus/research/external_issues/ranked_all_items.json`
- `/Users/jhemann/Code/lolcode-lang/corpus/research/external_issues/candidate_repros.json`
- `/Users/jhemann/Code/lolcode-lang/corpus/research/external_issues/candidate_repros_ranked.json`
- `/Users/jhemann/Code/lolcode-lang/corpus/research/external_issues/candidate_repros.tsv`

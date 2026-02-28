# External Regression Queue

- Generated at: 2026-02-28T16:19:40Z
- Source catalog: `corpus/tier2/CANDIDATE_REPOS.tsv`
- Total issues+PR items collected: 179
- Candidate reproducible regression items: 46
- Wave size: 10
- Total waves currently: 5

## How To Process All Items

1. Iterate `wave = 1..5` in `candidate_repros.tsv`.
2. For each row, create a minimal fixture/test + expected behavior.
3. Classify result in triage as `fixed-here`, `known-divergence`, `spec-ambiguous`, or `out-of-spec`.

## Wave Counts

- Wave 1: 10 items
- Wave 2: 10 items
- Wave 3: 10 items
- Wave 4: 10 items
- Wave 5: 6 items

## Top 30 Candidates

- [rank 1, wave 1] justinmeza/lci issue #43: [SIGSEV](https://github.com/justinmeza/lci/issues/43) [runtime-safety, score=120]
- [rank 2, wave 1] justinmeza/lci issue #47: [segfault or abort with IT in small programs](https://github.com/justinmeza/lci/issues/47) [runtime-safety, score=120]
- [rank 3, wave 1] justinmeza/lci issue #49: [SegFault when using STDIO Library](https://github.com/justinmeza/lci/issues/49) [runtime-safety, score=120]
- [rank 4, wave 1] justinmeza/lci issue #54: [Shebang without trailing newline causes buffer overflow (segfault)](https://github.com/justinmeza/lci/issues/54) [runtime-safety, score=120]
- [rank 5, wave 1] justinmeza/lci issue #55: [Failed realloc during program buffering causes segfault](https://github.com/justinmeza/lci/issues/55) [runtime-safety, score=120]
- [rank 6, wave 1] justinmeza/lci issue #79: [Out of Bounds Read and Null Pointer Dereference in LCI Version 0.10.5](https://github.com/justinmeza/lci/issues/79) [runtime-safety, score=120]
- [rank 7, wave 1] justinmeza/lci pr #50: [Fix a double free of the implicit variable](https://github.com/justinmeza/lci/pull/50) [runtime-safety, score=120]
- [rank 8, wave 1] justinmeza/lci issue #33: [segfault](https://github.com/justinmeza/lci/issues/33) [runtime-safety, score=110]
- [rank 9, wave 1] justinmeza/lci pr #24: [Defensive strategy that prevents a range of possible null pointer errors...](https://github.com/justinmeza/lci/pull/24) [runtime-safety, score=110]
- [rank 10, wave 1] justinmeza/lci issue #13: [unexpected error message with undefined variable interpolation](https://github.com/justinmeza/lci/issues/13) [language, score=100]
- [rank 11, wave 2] justinmeza/lci issue #23: [String and colon](https://github.com/justinmeza/lci/issues/23) [language, score=100]
- [rank 12, wave 2] justinmeza/lci issue #39: [Invalid Unicode code points are accepted](https://github.com/justinmeza/lci/issues/39) [language, score=100]
- [rank 13, wave 2] justinmeza/lci issue #56: [Colon and quotation mark conflict in strings](https://github.com/justinmeza/lci/issues/56) [language, score=100]
- [rank 14, wave 2] justinmeza/lci issue #57: [Octal NUMBR works when negative, but not positive](https://github.com/justinmeza/lci/issues/57) [language, score=100]
- [rank 15, wave 2] justinmeza/lci issue #58: [NUMBAR doesn't always work with line continuation](https://github.com/justinmeza/lci/issues/58) [language, score=100]
- [rank 16, wave 2] justinmeza/lci issue #59: [EOL doesn't replace MKAY when calling a variadic function](https://github.com/justinmeza/lci/issues/59) [language, score=100]
- [rank 17, wave 2] justinmeza/lci issue #60: [Function can read and modify variables in outside scope](https://github.com/justinmeza/lci/issues/60) [language, score=100]
- [rank 18, wave 2] justinmeza/lci issue #62: [BTW may not appear on the same line as TLDR](https://github.com/justinmeza/lci/issues/62) [language, score=100]
- [rank 19, wave 2] justinmeza/lci issue #71: [Loops always create a loop-scope variable and initialize it to 0](https://github.com/justinmeza/lci/issues/71) [language, score=100]
- [rank 20, wave 2] justinmeza/lci issue #78: [Functions of NOOB very limited](https://github.com/justinmeza/lci/issues/78) [language, score=100]
- [rank 21, wave 3] justinmeza/lci pr #52: [Fixed loop creation of variable even when present](https://github.com/justinmeza/lci/pull/52) [language, score=100]
- [rank 22, wave 3] JasonBock/LOLCode.net issue #7: [Try Removing Different Parser Types](https://github.com/JasonBock/LOLCode.net/issues/7) [language, score=90]
- [rank 23, wave 3] justinmeza/httpd.lol pr #3: [Added doctype and head to HTML document](https://github.com/justinmeza/httpd.lol/pull/3) [language, score=90]
- [rank 24, wave 3] justinmeza/lci issue #4: [Duplicate literals in Switch statment don't produce error message](https://github.com/justinmeza/lci/issues/4) [language, score=90]
- [rank 25, wave 3] justinmeza/lci issue #7: [BOTH SAEM not working in loops](https://github.com/justinmeza/lci/issues/7) [language, score=90]
- [rank 26, wave 3] justinmeza/lci issue #15: [string interpolation ignored in library calls](https://github.com/justinmeza/lci/issues/15) [language, score=90]
- [rank 27, wave 3] justinmeza/lci issue #18: [Chained slot access on BUKKITS does not work sometimes, with no error message.](https://github.com/justinmeza/lci/issues/18) [language, score=90]
- [rank 28, wave 3] justinmeza/lci pr #29: [relax numeric conversions from string](https://github.com/justinmeza/lci/pull/29) [language, score=90]
- [rank 29, wave 3] justinmeza/lci pr #46: [add constraint for missing TLDR terminator fix #43](https://github.com/justinmeza/lci/pull/46) [language, score=90]
- [rank 30, wave 3] DvaeFroot/cmsc124-lolcode-interpreter pr #3: [refactor: move rules inside the lexer](https://github.com/DvaeFroot/cmsc124-lolcode-interpreter/pull/3) [language, score=80]

## Output Files

- `/Users/jhemann/Code/lolcode-lang/corpus/research/external_issues/all_items.json`
- `/Users/jhemann/Code/lolcode-lang/corpus/research/external_issues/ranked_all_items.json`
- `/Users/jhemann/Code/lolcode-lang/corpus/research/external_issues/candidate_repros.json`
- `/Users/jhemann/Code/lolcode-lang/corpus/research/external_issues/candidate_repros_ranked.json`
- `/Users/jhemann/Code/lolcode-lang/corpus/research/external_issues/candidate_repros.tsv`

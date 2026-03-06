# External Evidence Report

Generated: `Friday, March 6th, 2026 2:06:45am`

- Cases evaluated: `302`
- JSON report: `/Users/jhemann/Code/lolcode-lang/scripts/../corpus/research/external-evidence-report.json`

## Observed Status Counts

- `parse-error`: `301`
- `ok`: `1`

## Bucket Counts

- `strict-non-1.3-or-extension`: `297`
- `program-bug-or-non-spec-input`: `4`
- `ok`: `1`

## Spec Scope Counts

- `1.2`: `295`
- `unknown`: `4`
- `1.3`: `3`

## Unknown Spec Scope Cases

- `ext_lci_issue_0055` (`lci` / `parse-error`): `parse-source: syntax error: unexpected ID ("echo") at line 1, col 1`
- `ext_lci_issue_0079` (`lci` / `parse-error`): `parse-source: syntax error: unexpected ID ("RAX") at line 1, col 2`
- `ext_sallysanban_lolcode_interpreter_commit_6dc7f723d98cb11a4adf127d930879d3897edbb2` (`sallysanban-lolcode-interpreter` / `parse-error`): `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`
- `ext_sallysanban_lolcode_interpreter_pr_0027` (`sallysanban-lolcode-interpreter` / `parse-error`): `parse-source: syntax error: unexpected NEWLINE at line 1, col 4`

## Top Messages

- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)` (`295`)
- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4` (`2`)
- `lex-source: invalid Unicode normative name in string literal at line 25, col 15` (`1`)
- `parse-source: syntax error: unexpected I at line 4, col 9` (`1`)
- `parse-source: syntax error: unexpected ID ("RAX") at line 1, col 2` (`1`)
- `parse-source: syntax error: unexpected ID ("echo") at line 1, col 1` (`1`)

## Possible Divergence Candidates

- None.

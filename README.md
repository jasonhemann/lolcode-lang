lolcode-lang
===========

Most advanced strict HAI 1.3 implementation we know of (we believe), by adjudication depth and traceability completeness. This is a strict-spec, evidence-scoped claim, not a canonical head-to-head benchmark claim. Adjudicated policy choices and implementation-dependent defaults are documented in spec/traceability/.

## Corpus Sync

Tiered corpus sync is now available:

```bash
./scripts/sync_corpus.sh
```

Tier2-only compatibility wrapper:

```bash
./scripts/sync_tier2_corpus.sh
```

Issue/PR sync for `lci` divergence triage:

```bash
./scripts/sync_lci_issue_backlog.sh
```

Tracked triage notes live at:

- `corpus/research/lci_issues/TRIAGE.md`
- `corpus/research/CURRENT_STATUS.md`

## Racket Bootstrap

Step-1 Racket scaffold is under:

- `src/lolcode/main.rkt`
- `tests/`

Step-2 spec fixture conformance harness is under:

- `tests/spec/fixtures/manifest.rktd`
- `tests/spec/fixtures/programs/`
- `tests/spec/conformance-test.rkt`

Step-3 lexer/parser implementation is under:

- `src/lolcode/lexer.rkt`
- `src/lolcode/parser.rkt`
- `src/lolcode/ast.rkt`
- `tests/spec/parse-negative-test.rkt`

Install Unicode lookup dependency (used for `:[<char name>]` escapes):

```bash
raco pkg install --auto codepoint
```

Parser implementation note:

- `src/lolcode/parser.rkt` now uses Racket `parser-tools/yacc` with source-positioned syntax errors.

Run tests:

```bash
./scripts/test_racket.sh
```

or:

```bash
raco test tests
```

## Public Runtime API

Library entrypoints are in `src/lolcode/main.rkt`:

- `parse-program : String -> program`
- `run-program : program -> Void`

`run-program` writes directly to `current-output-port`, reads from
`current-input-port`, and raises Racket exceptions for parse/runtime errors.
It does not return status hashes.

Internal corpus/research tooling uses `src/lolcode/internal/reporting.rkt` for
hash-shaped execution reports.

## CLI

After package install, run:

```bash
lolcode path/to/program.lol
raco lolcode path/to/program.lol
```

Use `--trace` for full stack traces.

## `#lang`

`#lang lolcode` is supported via `lolcode/lang/reader.rkt`.
Module text still uses strict LOLCODE source and requires `HAI 1.3`.

Run spec traceability audit:

```bash
./scripts/check_spec_traceability.sh
```

Regenerate the 1.3 clause index (line-numbered headings + normative lines):

```bash
./scripts/extract_spec_clauses.sh
```

Run external regression evidence (non-gating):

```bash
./scripts/test_external_evidence.sh
```

Import one external regression wave into evidence fixtures/manifest:

```bash
./scripts/import_external_wave.sh 1
```

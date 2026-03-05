lolcode-lang
===========

A Racket-based [LOLCODE](http://lolcode.com) implementation project targeting the 1.2 and 1.3 specs.

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

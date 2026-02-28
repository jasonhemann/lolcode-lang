lolchez
=======

A Scheme REPL & interpreter for [LOLCODE](http://lolcode.com).

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

Run external regression evidence (non-gating):

```bash
./scripts/test_external_evidence.sh
```

Import one external regression wave into evidence fixtures/manifest:

```bash
./scripts/import_external_wave.sh 1
```

# Running the lolchez REPL
We currently lack a boot file, so the repl can be started by loading `repl.scm`
in your chez scheme repl and running `(lol-repl)`. ^D exits.

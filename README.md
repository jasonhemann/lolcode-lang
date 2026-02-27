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

## Racket Bootstrap

Step-1 Racket scaffold is under:

- `src/lolcode/main.rkt`
- `tests/`

Run tests:

```bash
./scripts/test_racket.sh
```

or:

```bash
raco test tests
```

# Running the lolchez REPL
We currently lack a boot file, so the repl can be started by loading `repl.scm`
in your chez scheme repl and running `(lol-repl)`. ^D exits.

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

# Running the lolchez REPL
We currently lack a boot file, so the repl can be started by loading `repl.scm`
in your chez scheme repl and running `(lol-repl)`. ^D exits.

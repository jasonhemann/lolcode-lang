lolcode-lang
===========

Most advanced strict HAI 1.3 implementation we know of (we believe), by adjudication depth and traceability completeness. This is a strict-spec, evidence-scoped claim, not a canonical head-to-head benchmark claim. Adjudicated policy choices and implementation-dependent defaults are documented in spec/traceability/.

## Install

Install the package:

```bash
raco pkg install --auto .
```

## Run Programs

After package install, run:

```bash
lolcode path/to/program.lol
raco lolcode path/to/program.lol
```

Use `--trace` for full stack traces:

```bash
lolcode --trace path/to/program.lol
```

## `#lang` Usage

`#lang lolcode` is supported via `lang/reader.rkt`. Module text still uses strict LOLCODE source and requires `HAI 1.3`.

```racket
#lang lolcode
HAI 1.3
VISIBLE "OH HAI"
KTHXBYE
```

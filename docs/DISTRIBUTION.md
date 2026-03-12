# Distribution

## Package install

```bash
raco pkg install --auto .
```

This installs:

- `raco lolcode`
- `lolcode` launcher
- `#lang lolcode`

## CLI usage

```bash
lolcode path/to/program.lol
raco lolcode path/to/program.lol
```

Use `--trace` for full stack traces:

```bash
lolcode --trace path/to/program.lol
```

## Standalone build

Build a host executable:

```bash
./scripts/build_cli_exe.sh
```

Create a distributable bundle:

```bash
./scripts/package_cli_dist.sh
```

## `#lang` usage

```racket
#lang lolcode
HAI 1.3
VISIBLE "OH HAI"
KTHXBYE
```

`module+ main` auto-runs the program when the module is executed.

# Replacement Candidates Probe (Lex/Parse/Eval)

Generated: `2026-03-02`

Scope:
- Newly added tier2 replacement candidates from shadow-mirror search:
  - `markwatkinson-loljs`
  - `maadriana-lolcode-interpreter`
  - `garthendrich-lolcode-interpreter`
  - `nfenciso1-lolcode-interpreter`
  - `sallysanban-lolcode-interpreter`
  - `kjdeluna-lolcode-interpreter`

Important caveat:
- **Spec-version intent is unknown unless a corpus states it explicitly.**
- For this batch, `HAI` version headers were `unspecified` in all harvested `.lol` files.

## Sync Notes

- Tier2 sync was run prior to probe (`./scripts/sync_tier2_corpus.sh --tier tier2`).
- `sallysanban-lolcode-interpreter` synced with `ok:partial:10` and all harvested `.lol` files are `0` bytes (path/URL encoding issue for files under directories with spaces).
  - Its parse failures are therefore not semantically meaningful yet.

## Probe Summary

Status columns:
- `ok`: parsed and evaluated with `status=ok`
- `parse_fail`: lex/parse failure
- `runtime_error`: evaluated with runtime error status
- `unsupported`: evaluated with unsupported status
- `eval_timeout`: timed out (2s per program)

| Label | Files | ok | parse_fail | runtime_error | unsupported | eval_timeout |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `markwatkinson-loljs` | 2 | 0 | 2 | 0 | 0 | 0 |
| `maadriana-lolcode-interpreter` | 8 | 5 | 2 | 1 | 0 | 0 |
| `garthendrich-lolcode-interpreter` | 9 | 7 | 2 | 0 | 0 | 0 |
| `nfenciso1-lolcode-interpreter` | 19 | 12 | 6 | 0 | 0 | 1 |
| `sallysanban-lolcode-interpreter` | 9 | 0 | 9 | 0 | 0 | 0 |
| `kjdeluna-lolcode-interpreter` | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total** | **47** | **24** | **21** | **1** | **0** | **1** |

## Top Failure Signatures

`markwatkinson-loljs`:
- parse: unexpected `I` at top-level (`I HAS A X`) (1)
- parse: unexpected identifier `DUZ` (`HOW DUZ I ...`) (1)

`maadriana-lolcode-interpreter`:
- parse: unexpected `NEWLINE` with inline `BTW` comment usage in expression context (1)
- parse: unexpected `ITZ` form in statement position (1)
- runtime: division by zero (1)

`garthendrich-lolcode-interpreter`:
- parse: unexpected `OF` in infix-ish `SUM OF` expression usage (1)
- lex: unterminated string literal (1)

`nfenciso1-lolcode-interpreter`:
- parse failures are diverse (6 distinct singletons in this sample), including:
  - unexpected `OF` in `SUM OF` shape (1)
  - unexpected `VISIBLE` in context (2 singleton variants)
  - unexpected `GIMMEH` in context (1)
  - unexpected string literal token in context (1)
- eval timeout: 1 program (2s cutoff)

`sallysanban-lolcode-interpreter`:
- all 9 parse failures are `unexpected EOF` at file start due zero-byte synced files.

## Interpretation

- `maadriana`, `garthendrich`, and `nfenciso1` provide useful mixed signals (some clean runs + localized failures) and are good next differential targets.
- `markwatkinson-loljs` currently contributes parser-shape pressure, mostly around non-1.2/1.3 syntax forms.
- `sallysanban` needs re-harvest (path encoding fix or clone-based ingest) before semantic conclusions.
- `kjdeluna` currently contributes no executable `.lol` corpus.

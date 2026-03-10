# Deprecation Matrix: 1.1 Era -> 1.2 -> 1.3

Date: 2026-03-02

## Sources

- 1.1 (archived): <https://web.archive.org/web/20111101140242/http://lolcode.com/specs/1.1>
- 1.1 (older cross-check): <https://web.archive.org/web/20090113062835/http://lolcode.com/specs/1.1>
- 1.2 (official markdown): <https://raw.githubusercontent.com/justinmeza/lolcode-spec/master/v1.2/lolcode-spec-v1.2.md>
- 1.3 (official markdown): <https://raw.githubusercontent.com/justinmeza/lolcode-spec/master/v1.3/lolcode-spec-v1.3.md>
- Archived specs index (what existed on original site): <https://web.archive.org/web/20120413185942/http://lolcode.com/specs?idx=specs>

## Notes on confidence

- `Confirmed` means the older form is explicitly present in 1.1 and absent/replaced in 1.2+ text.
- `Inferred` means wording changed enough that behavior likely shifted, but not as an explicit "deprecated" label.

## Matrix

| Feature / Syntax | 1.1 | 1.2 | 1.3 | Status |
|---|---|---|---|---|
| `HAI` optional codename header (`HAI GINGER`) | Present | Replaced by numeric version wording (`HAI` + language version number) | Numeric version wording retained | Confirmed replaced after 1.1 |
| Assignment form `LOL <var> R <expr>` | Present | Replaced with `<variable> R <expression>` | `<variable> R <expression>` retained | Confirmed removed after 1.1 |
| Switch header as `WTF [IZ] <expr> [?]` | Present | Reworked to `WTF?` operating on `IT` | `WTF?` retained | Confirmed reworked after 1.1 |
| "ARRAYS AND HASHES" as sectioned feature with PHP-style wording | Present | BUKKIT/arrays moved to "reserved / under-specified" status | BUKKIT gains fuller container/object semantics | Confirmed semantic rework across 1.2/1.3 |
| TYPE literal/type-family details marked as deleted in 1.2 lineage text | Present in 1.1-era language family context | 1.2 archived text includes `[DEL: ... :DEL]` markers around TYPE details | 1.3 keeps the reduced stance | Inferred deprecation/removal in 1.2 cycle |
| `WAZZUP` / `BUHBYE` block delimiters | Not present | Not present | Not present | Not part of official 1.1/1.2/1.3 specs |

## Practical takeaway for this repo

- The strongest objectively confirmed "deprecated/removed since 1.1" items are:
  - `HAI GINGER` style codename header
  - `LOL <var> R <expr>` assignment prefix
  - `WTF [IZ] <expr> [?]` switch shape
- `WAZZUP`/`BUHBYE` are dialect features from third-party implementations, not official spec features.

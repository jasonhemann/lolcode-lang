# Parse-Error Partition (Tier2, strict 1.3 policy)

Date: 2026-03-05
Source: `corpus/research/tier2-eval-classified.json`

## Partition policy

For likely-program parse failures (`outcome=parse-error`):

1. `strict-non-1.3`
   - version-policy failures (`unsupported version`)
   - missing `HAI 1.3` marker patterns (`unexpected NEWLINE at line 1/2, col 4`)
   - unsupported extension/import headers (`CAN HAS STDIO?`, `CAN HAS RAYLIB?`, `CAN HAS STRING?`)
   - non-spec greeting headers (`HAI "Dear ..."` style)
2. `program-bug`
   - malformed/misspelled operators, invalid identifiers, ad-hoc concatenation syntax, etc.
3. `spec-divergence`
   - reserved for strict-1.3 programs that should parse per spec but fail in our parser.

## Results

- Total likely-program parse errors: `167`
- `strict-non-1.3`: `149`
- `program-bug`: `18`
- `spec-divergence`: `0`

## Representative strict-non-1.3 failures

- `parse-source: syntax error: unexpected NEWLINE at line 1, col 4` (`94`)
- `parse-source: unsupported version: 1.2 (this implementation only accepts HAI 1.3)` (`28`)
- `parse-source: syntax error: unexpected NEWLINE at line 2, col 4` (`9`)
- `parse-source: syntax error: unexpected ID ("STDIO?") at line 2, col 9` (`6`)

Examples:

- `corpus/tier2/bernardjezua-lolcode-interpreter/files/testcases/final/03_arith.lol`
- `corpus/tier2/lokalise-lol-post/files/lolcode-fun-post/variables.lol`
- `corpus/tier2/aurasphere-ftpd-lol/files/ftpd.lol`

## Representative program-bug failures

- `parse-source: syntax error: unexpected OF at line 30, col 33` (`1`)  ; `DIFFRENCE OF`
- `parse-source: syntax error: unexpected OF at line 49, col 37` (`1`)  ; `DIFFRENCE OF`
- `parse-source: syntax error: unexpected STRING (" and ") at line 5, col 16` (`1`) ; string concatenation outside `SMOOSH`
- `parse-source: invalid identifier syntax: "//"` (`1`) ; non-spec comment token

Examples:

- `corpus/tier2/eulol/files/problem0003.lol`
- `corpus/tier2/lokalise-lol-post/files/lolcode-fun-post/operators.lol`
- `corpus/tier2/lolcode-simple-algorithms/files/BASICS.lol`

## Notes

- No currently triaged parse failure in tier2 is classified as strict spec divergence.
- This partition is policy-aware: strict 1.3 rejection is intentional and separated from parser defects.

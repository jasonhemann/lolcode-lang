# `justinmeza/lollm` Snapshot

Snapshot date: 2026-02-27  
Upstream: https://github.com/justinmeza/lollm

## What was pulled

- `README.upstream.md`
- `train.lol`
- `chat.lol`
- `lolspeak.txt`
- `metadata.json`

## Quick profile

- `lolspeak.txt`: 1,105 lines, 38,051 bytes
- `train.lol`: 26 lines, 945 bytes
- `chat.lol`: 21 lines, 541 bytes

Heuristic scan of `lolspeak.txt`:

- lines with common LOLCODE markers: 518 / 1,105 (~46.88%)
- narrative/prose segment is present (e.g. "MOAR LOLSPEAK PROSE" section near file tail)

Interpretation:

- This is a mixed corpus (LOLCODE programs + lolspeak prose), not a clean validity oracle.
- Keep it as non-normative stress data for lexer/parser robustness and extension experiments.
- Do not treat the entire file as spec-valid LOLCODE test input.

## Immediate use

- Useful for building "accept/reject/classify" corpus tooling.
- Useful for fuzz-adjacent tests that exercise tokenizer/parser resilience.
- Not suitable as conformance evidence for 1.2/1.3 pass/fail without filtering.

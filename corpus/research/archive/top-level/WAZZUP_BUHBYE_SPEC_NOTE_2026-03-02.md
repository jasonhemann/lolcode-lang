# WAZZUP/BUHBYE Spec Check (2026-03-02)

## Question

Are `WAZZUP` / `BUHBYE` part of the official spec (possibly deprecated between 1.1, 1.2, 1.3)?

## Primary Sources Checked

- Official spec repository root: <https://github.com/justinmeza/lolcode-spec>
- Official 1.2 text: <https://raw.githubusercontent.com/justinmeza/lolcode-spec/master/v1.2/lolcode-spec-v1.2.md>
- Official 1.3 text: <https://raw.githubusercontent.com/justinmeza/lolcode-spec/master/v1.3/lolcode-spec-v1.3.md>
- Archived 1.1 spec snapshot: <https://web.archive.org/web/20111101140242/http://lolcode.com/specs/1.1>

## Findings

- `WAZZUP` / `BUHBYE` do **not** appear in official 1.2 text.
- `WAZZUP` / `BUHBYE` do **not** appear in official 1.3 text.
- `WAZZUP` / `BUHBYE` do **not** appear in archived 1.1 spec text.
- Variable declaration sections in both versions specify `I HAS A ...` forms, not a `WAZZUP`/`BUHBYE` block form.
  - 1.2: file creation + variable declaration sections (`HAI ... KTHXBYE`, `I HAS A ...`) (see lines ~81-83 and ~105 in `v1.2/lolcode-spec-v1.2.md`).
  - 1.3: file creation + declaration section (`I HAS A <variable> ...` variants) (see lines ~89-91 and ~117 in `v1.3/lolcode-spec-v1.3.md`).
- No deprecation note mentioning `WAZZUP` / `BUHBYE` is present in those official 1.2/1.3 texts.

## Project Decision (strict 1.3 mode)

- Treat `WAZZUP` / `BUHBYE` as non-normative dialect syntax.
- Keep strict parser behavior: reject these forms unless a future compatibility mode is explicitly introduced.

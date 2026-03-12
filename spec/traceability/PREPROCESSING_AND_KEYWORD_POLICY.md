# Preprocessing and Keyword Policy (N44, N51)

Date: 2026-03-06
Scope: strict LOLCODE 1.3 parser/lexer behavior.

## N44: Preprocessing Order

Execution order used by implementation:

1. Lexical scan with string shielding (`"` delimited YARNs parsed first; comma/ellipsis inside YARN are literal text).
2. Single-line comment stripping (`BTW ...` to newline) and block-comment skipping (`OBTW ... TLDR`) in lexer stream; `OBTW` is recognized only at logical statement boundaries.
3. Line-continuation processing (`...` and `…`) at line end only.
4. Comma soft-break conversion to `NEWLINE` tokens.
5. Parser-side same-line phrase collapse (`IM IN` -> `IMIN`, `IM OUTTA` -> `IMOUTTA`).
6. Parser-side boundary validation for implicit-`MKAY` omission in variadics (rejected before same-statement continuations such as `!` / `AN YR`).
7. Grammar parse over normalized token stream with optional-`AN` variadic argument forms.

Evidence tests:
- `inline-block-comment-tldr-handoff` in `tests/spec/parse-negative-test.rkt`
- `preprocess-order-runtime-src` in `tests/spec/runtime-core-test.rkt`
- existing continuation/comment edge tests in `tests/spec/parse-negative-test.rkt`

## N51: Longest-Match Keyword Policy

Policy:
- Multiword forms and punctuated forms are recognized only in canonical token shapes.
- `O RLY?` requires `RLY?` token (not `RLY ?`).
- `WTF?` requires `WTF?` token (not `WTF ?`).
- Phrase collapse for `IM IN`/`IM OUTTA` happens only when both tokens are on the same line.

Evidence tests:
- `spaced-orly-question` and `spaced-wtf-question` in `tests/spec/parse-negative-test.rkt`
- `split-im-outta-phrase` in `tests/spec/parse-negative-test.rkt`
- loop positive forms in `tests/spec/runtime-core-test.rkt`

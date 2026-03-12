# Semantic Lint Tranche 2 (Rev3) Integration Memo

Date: 2026-03-12
Source artifacts:
- `lolcode_1_3_semantic_lint_tranche2_memo_2026-03-12-rev3.md`
- `lolcode_tranche2_tests_bundle_rev3.zip`

## Scope
This note records how tranche-2 EXG holdings were integrated into strict 1.3 adjudications, implementation behavior, and regression anchors.

## Holdings Mapping

| EXG | Adjudication | Integrated policy | Primary anchors |
| --- | --- | --- | --- |
| EXG-101 | N86 | Optional `AN` for `SMOOSH`/`ALL OF`/`ANY OF` across general argument positions; leading `AN` remains invalid. | `variadic-optional-an-general-expr`, `variadic-leading-an-negative` |
| EXG-102 | N87 | Implicit `MKAY` omission is statement-boundary only; explicit `MKAY` required before `!` and `AN YR` continuations. | `implicit-mkay-before-bang-negative`, `smoosh-explicit-mkay-before-bang-src` |
| EXG-103 | N88 | `SRS` used at identifier-binding sites must evaluate to identifier-shaped names; non-identifier results error. | `srs-numeric-target-src` |
| EXG-104 | N89 | `HOW DUZ` accepted as definition-site synonym for `HOW IZ` (ordinary, receiver, object-body); call syntax remains `IZ` only. | `how-duz-i-form`, `how-duz-callform`, `how-duz-i-runtime-src`, `how-duz-receiver-runtime-src`, `how-duz-objectblock-runtime-src` |
| EXG-105 | N90 | `ME HAS A <slot>` no-`ITZ` shorthand allowed (defaults NOOB); generic `<object> HAS A <slot>` still requires `ITZ`. | `me-slot-no-itz-shorthand-src`, `slot-set-missing-itz` |
| EXG-106 | N91 | `OBTW` recognized only at logical statement boundaries (line start/comma boundary), rejected mid-command. | `obtw-mid-command-negative`, `block-comment-comma-boundary-src` |
| EXG-107 | N92 | Interpolation placeholders remain identifier-only (no whitespace/expression placeholders). | `format-string-whitespace-placeholder-src` |
| EXG-108 | N93 | `:[<name>]` requires uppercase name and resolves against Unicode 4.1 normative-name set. | `string-normative-escape-src`, `string-normative-escape-outside-41-src`, parse negatives for invalid/lowercase names |
| EXG-109 | N94 | NUMBAR->YARN prints truncate (no rounding) to at most two decimals, without forced zero-padding. | `numbar-visible-format-src`, `numbar-no-forced-padding-src` |
| EXG-110 | N95 | `ANY OF`/`ALL OF` evaluate left-to-right with short-circuit semantics. | `logic-variadic-any-short-circuit-src`, `logic-variadic-any-short-circuit-avoids-error-src`, `logic-variadic-all-short-circuit-rhs-src` |
| EXG-111 | N95 | `SMOOSH` arity is one-or-more (one-arg identity accepted, zero-arg rejected). | `smoosh-one-arg-src`, `smoosh-zero-arg-negative` |
| EXG-112 | N96 | BUKKIT dynamic slot keys are typed (`NUMBR`/`YARN`), no hidden coercion between numeric and string keys. | `bukkit-slot-keys-typed-src` |

## Fixture Preservation
The supplied tranche-2 fixture bundle is preserved at:
- `tests/spec/fixtures/exegesis/tranche2-rev3/`

## Verification
- `raco test tests` -> pass (`1141 tests passed`)

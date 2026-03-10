# External Regression Waves

As of **February 28, 2026**, this file tracks batchable external-regression targets in waves of 10.

Primary inputs:
- `corpus/research/IMPLEMENTATION_ORACLE_MATRIX.md`
- `corpus/research/lci_issues/issues.json`
- `corpus/research/lci_issues/pulls.json`

## Per-Target Work Template

For each target below:
1. Add minimal repro program fixture under `tests/spec/fixtures/programs/`.
2. Add fixture metadata entry in `tests/spec/fixtures/manifest.rktd` with:
   - `id`
   - `source-ref` (external issue/PR/commit URL)
   - `expected-stdout` or expected runtime error regex
3. Add/extend test assertions in `tests/spec/runtime-core-test.rkt` (or dedicated external-regressions test file).
4. Classify in `corpus/research/lci_issues/TRIAGE.md`:
   - `fixed-here`
   - `known-divergence`
   - `spec-ambiguous`
   - `out-of-spec`

## Wave 1 (Top 10)

Already seeded in `IMPLEMENTATION_ORACLE_MATRIX.md`:
- `ext_lci_71_loop_var_scope`
- `ext_lci_65_liek_copy`
- `ext_lci_60_fn_scope_isolation`
- `ext_lci_59_variadic_eol`
- `ext_lci_58_numbar_line_cont`
- `ext_lci_56_string_escape_colon_quote`
- `ext_rust_lci_recursion`
- `ext_hlci_casting_numbar`
- `ext_loco_comma_yarn_lex`
- `ext_cmsc124_preamble_newlines`

## Wave 2 (Next 10)

| Fixture ID | Source | Reference | Topic | Work Needed |
| --- | --- | --- | --- | --- |
| `ext_lci_13_undef_interp` | `lci` issue | [#13](https://github.com/justinmeza/lci/issues/13) | Undefined variable interpolation diagnostics | fixture + expected error text/shape |
| `ext_lci_18_chained_slots` | `lci` issue | [#18](https://github.com/justinmeza/lci/issues/18) | Chained `BUKKIT` slot access behavior | fixture + nested slot read/write assertions |
| `ext_lci_38_conditional_scope` | `lci` issue | [#38](https://github.com/justinmeza/lci/issues/38) | Variable visibility after conditional blocks | fixture + scope resolution assertions |
| `ext_lci_47_it_small_prog` | `lci` issue | [#47](https://github.com/justinmeza/lci/issues/47) | `IT` behavior in small programs | fixture + `IT` initialization/lifetime assertions |
| `ext_lci_57_octal_numbr` | `lci` issue | [#57](https://github.com/justinmeza/lci/issues/57) | Positive vs negative octal `NUMBR` parsing | fixture + literal parse/eval assertions |
| `ext_lci_78_noob_functions` | `lci` issue | [#78](https://github.com/justinmeza/lci/issues/78) | Function behavior with `NOOB` values | fixture + function call coercion assertions |
| `ext_lci_pr22_alt_method_me` | `lci` PR | [#22](https://github.com/justinmeza/lci/pull/22) | Alternate method call syntax (`ME`) | fixture + method dispatch semantics |
| `ext_rust_lci_scope_issues` | `rust-lci` commit | [8ef8689](https://github.com/jD91mZM2/rust-lci/commit/8ef8689a3167c5d2259067f21d55f0e9cf43c2fb) | Scope handling issues | fixture + nested scope mutation checks |
| `ext_hlci_case_interp` | `hlci` commit | [069f24f](https://github.com/YS-L/hlci/commit/069f24fdb9ec18ac4a83224ecd2291431bb1aca1) | Case interpretation behavior | fixture + switch/case fallthrough checks |
| `ext_loco_missing_kthxbye` | `loco` commit | [bc66975](https://github.com/jpcarreon/loco/commit/bc669755496e740459b6de2688de258021924a71) | Missing `KTHXBYE` crash handling | fixture + parser error quality checks |

## Wave 3 (Next 10)

| Fixture ID | Source | Reference | Topic | Work Needed |
| --- | --- | --- | --- | --- |
| `ext_lci_4_switch_dup_literal` | `lci` issue | [#4](https://github.com/justinmeza/lci/issues/4) | Duplicate literal handling in switch | fixture + duplicate-case diagnostic behavior |
| `ext_lci_7_both_saem_loop` | `lci` issue | [#7](https://github.com/justinmeza/lci/issues/7) | `BOTH SAEM` behavior in loop context | fixture + loop predicate checks |
| `ext_lci_35_var_reset` | `lci` issue | [#35](https://github.com/justinmeza/lci/issues/35) | Variable unexpectedly resetting | fixture + long-run state persistence checks |
| `ext_lci_68_future_array_err` | `lci` issue | [#68](https://github.com/justinmeza/lci/issues/68) | Future-branch array behavior | fixture + classify as `out-of-spec` if 1.4-only |
| `ext_lci_54_shebang_eof` | `lci` issue | [#54](https://github.com/justinmeza/lci/issues/54) | Shebang/no trailing newline handling | file-based fixture + runtime safety check |
| `ext_lci_55_buffer_realloc` | `lci` issue | [#55](https://github.com/justinmeza/lci/issues/55) | Large input buffering safety | generated large fixture + no-crash assertion |
| `ext_lci_pr31_input_len_pow2` | `lci` PR | [#31](https://github.com/justinmeza/lci/pull/31) | Input length edge case | interactive/input harness regression |
| `ext_loco_visible_parse_fix` | `loco` commit | [202b31d](https://github.com/jpcarreon/loco/commit/202b31d86b54eb9df34b5f6137ffa4e8c5abc554) | `VISIBLE` parser fix | fixture + visible args parsing checks |
| `ext_sada_fn_syntax_fix` | `SADAsuncion` commit | [FIX: IZ I and HOW IZ I syntax](https://github.com/SADAsuncion/LOLCodeInterpreter/commits/main/) | Function syntax acceptance | fixture + parser accept/reject matrix |
| `ext_cmsc124_implicit_cast_fix` | `cmsc124` PR/commit stream | [#74](https://github.com/DvaeFroot/cmsc124-lolcode-interpreter/pull/74) | Implicit typecasting in arithmetic/boolean ops | fixture + coercion semantics assertions |

## After Wave 3

Batch generation rule for subsequent waves:
- Pull unresolved language-semantics entries from `lci` open+closed issues first.
- Add non-`lci` candidates only when they provide distinct parser/runtime behavior not already represented.
- Exclude build/install/platform-only issues unless they imply parser/runtime safety bugs.

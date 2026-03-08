# IT Update Matrix (N60)

Date: 2026-03-06
Scope: strict LOLCODE 1.3 runtime (`src/lolcode/runtime.rkt`).

## Closed List: Forms That Update IT

1. Bare expression statement (`stmt-expr`)
2. `VISIBLE` (to last printed argument value when args exist)
3. `GIMMEH`
4. Cast assignment (`IS NOW A`)
5. Slot declaration/assignment form (`<object> HAS A <slot> [ITZ ...]`)
6. Object definition statement (`O HAI IM ... KTHX`)
7. `FOUND YR` (before control escape)
8. Loop updater tick (`UPPIN`, `NERFIN`, unary updater call)

## Forms That Do Not Update IT By Themselves

1. Variable declaration (`I HAS A ...`)
2. Assignment (`R`)
3. `O RLY?`/`MEBBE`/`NO WAI` wrapper semantics
4. `WTF?` wrapper semantics
5. Loop control wrapper (`IM IN YR` / `IM OUTTA YR`) when no updater step runs
6. Function/method definition statements

## Evidence

Primary regression:
- `it-update-matrix-src` in `tests/spec/runtime-core-test.rkt`

Supporting regressions:
- `visible-updates-it-src`
- `orly-mebbe-truthy-cast-src`
- `method-it-local-activation-src`
- `method-fallthrough-returns-local-it-src`

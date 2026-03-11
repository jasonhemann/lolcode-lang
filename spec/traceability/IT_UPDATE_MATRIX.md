# IT Update Matrix (N60)

Date: 2026-03-06
Scope: strict LOLCODE 1.3 runtime (`src/lolcode/runtime.rkt`).

## Closed List: Forms That Update IT

1. Bare expression statement (`stmt-expr`)

## Forms That Do Not Update IT By Themselves

1. Variable declaration (`I HAS A ...`)
2. Assignment (`R`)
3. Cast assignment (`IS NOW A`)
4. Slot declaration/assignment form (`<object> HAS A <slot> ITZ <expression>`)
5. `GIMMEH`
6. `VISIBLE`
7. Object definition statement (`O HAI IM ... KTHX`)
8. `O RLY?`/`MEBBE`/`NO WAI` wrapper semantics
9. `WTF?` wrapper semantics
10. Loop control wrapper (`IM IN YR` / `IM OUTTA YR`)
11. Function/method definition statements
12. `FOUND YR` (control escape without IT mutation)

## Evidence

Primary regression:
- `it-update-matrix-src` in `tests/spec/runtime-core-test.rkt`

Supporting regressions:
- `visible-updates-it-src`
- `method-it-local-activation-src`
- `method-fallthrough-returns-local-it-src`

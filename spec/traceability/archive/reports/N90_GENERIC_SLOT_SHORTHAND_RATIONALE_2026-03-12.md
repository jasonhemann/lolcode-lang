# N90 Generic Slot Shorthand Rationale (2026-03-12)

Scope:
- Strict LOLCODE 1.3 interpretation for slot declaration shorthand without `ITZ`.
- Target construct: `<object> HAS A <slot>`.

Holding:
- In strict mode, `<object> HAS A <slot>` is accepted as declaration shorthand for `<object> HAS A <slot> ITZ NOOB`.
- This applies generally for object receiver expressions, including but not limited to `ME`.

Why this is the narrowest coherent reading:

1. `ME`-only shorthand is extra machinery:
   - A `ME`-exclusive rule introduces a special grammar/semantic case that the spec does not explicitly describe.
   - `ME` is specified as the calling-object identifier, not as a separate declaration syntax class.

2. Generic shorthand is structurally consistent:
   - Variable declarations already use the `...` without initializer => default `NOOB` shorthand pattern.
   - Reusing that pattern for slot declaration avoids introducing asymmetry between declaration families.

3. `ME`-only restriction is policy noise:
   - It produces a less compositional language surface (`ME HAS A` allowed, `o HAS A` rejected) without a clear textual forcing function.
   - The general rule is simpler to explain, test, and reason about.

4. Canonical explicit form remains available:
   - `... ITZ <expression>` remains canonical and equivalent where explicit initialization is desired.

Regression anchors:
- `slot-set-no-itz-shorthand`
- `slot-set-no-itz-shorthand-src`
- `me-slot-no-itz-shorthand-src`

Related adjudications:
- `N90` (slot shorthand policy)
- `N38` (article optionality remains grammar-site specific)

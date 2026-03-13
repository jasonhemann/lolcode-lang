# Local Agent Rules

## Safe Deletion Policy

- Do not use `rm -rf` for routine cleanup.
- Default to `trash` for deletions.
- Prefer `sudo trash` when elevated permissions are required and non-interactive sudo is available.
- If `trash` is unavailable, stop and ask before using any permanent delete command.

## House Style (Racket)

- Prefer direct recursion over ad hoc local `let` loops when the recursion is the core control flow.
- Do not introduce internal helper definitions or local loops solely to remove default-argument recursion; keep the clearer form.
- If a list traversal branch uses `null?`/`else` with `car`/`cdr`, rewrite to `match` on the list shape (`'()` and `(cons ...)`).
- For simple two-way `null?` checks that do not destructure (`car`/`cdr`) and do not reuse the tested value, prefer `if`.
- For list/index scans (e.g., `find-first`), thread list and index as explicit parameters and call once with explicit initial values.
- Prefer `cond` with `=>` when testing a lookup and immediately consuming the looked-up value.
- Prefer `case` for simple symbol dispatch; prefer `match` for structural dispatch.
- Keep functions small enough to reason about locally; split large semantic dispatchers into top-level helper functions.

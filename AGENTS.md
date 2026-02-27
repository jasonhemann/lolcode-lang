# Local Agent Rules

## Safe Deletion Policy

- Do not use `rm -rf` for routine cleanup.
- Default to `trash` for deletions.
- Prefer `sudo trash` when elevated permissions are required and non-interactive sudo is available.
- If `trash` is unavailable, stop and ask before using any permanent delete command.

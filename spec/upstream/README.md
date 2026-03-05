# Upstream Spec Snapshots

This directory vendors immutable snapshots of the canonical LOLCODE spec texts used as the conformance oracle for this repository.

## Source Provenance

- Upstream repository: `https://github.com/justinmeza/lolcode-spec`
- Upstream branch/reference: `refs/heads/master`
- Upstream commit (resolved): `b9abe0187b4fbaa49997992253f515b109b708f2`
- Fetch date (UTC): `2026-03-04`

## Snapshot Files

- `lolcode-spec-v1.2.md`
  - Source URL: `https://raw.githubusercontent.com/justinmeza/lolcode-spec/master/v1.2/lolcode-spec-v1.2.md`
  - SHA256: `a81c7e3bc2b5f72b81ef40b8083ad58e4b18a913fe2d8986b7e90394aa069002`
- `lolcode-spec-v1.3.md`
  - Source URL: `https://raw.githubusercontent.com/justinmeza/lolcode-spec/master/v1.3/lolcode-spec-v1.3.md`
  - SHA256: `e8057f9bbcc80f65c9e7caaa887b5419f6935b84a335586d9289ac697a70ec22`

## Update Procedure

1. Re-fetch both source URLs into this directory.
2. Recompute SHA256 checksums.
3. Resolve and record upstream commit hash for the source branch.
4. Re-run traceability checks:
   - `racket scripts/check_spec_traceability.rkt`
   - `racket scripts/extract_spec_clauses.rkt`

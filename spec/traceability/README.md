# Spec Traceability

This directory tracks clause-level conformance status for the strict 1.3 target.

## Files

- `spec-1.3-matrix.rktd`
  - Machine-readable list of traceability entries.
  - Each entry links one spec clause to implementation/test evidence and a status.

- `spec-1.3-clause-index.tsv`
  - Generated index of headings and normative-looking lines from the vendored 1.3 spec text.
  - Produced by `racket scripts/extract_spec_clauses.rkt`.

## Status Values

- `implemented`: clause appears implemented and test-backed.
- `partial`: clause is partly implemented or coverage is incomplete.
- `known-divergence`: behavior differs from spec and is tracked intentionally.
- `deferred`: acknowledged gap, planned work.
- `out-of-scope`: intentionally excluded from strict 1.3 target.

## Validation

Run:

```sh
racket scripts/check_spec_traceability.rkt
```

This validates schema, file references, and emits a status summary.

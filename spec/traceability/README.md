# Spec Traceability

This directory tracks clause-level conformance status for the strict 1.3 target.

## Files

- `spec-1.3-matrix.rktd`
  - Machine-readable list of traceability entries.
  - Each entry links one spec clause to implementation/test evidence and a status.

- `spec-1.3-clause-index.tsv`
  - Generated index of non-empty clause candidates from the vendored 1.3 spec text.
  - Includes line kinds: `heading`, `bullet`, `normative`, `prose`, `syntax`, `code`.
  - Produced by `racket scripts/extract_spec_clauses.rkt`.

- `spec-1.3-clause-mapping-audit.md`
  - Recalculated mapping audit from extracted 1.3 clauses to matrix source-line references.
  - Tracks currently unmapped normative clauses and 1.2\\1.3 delta observations.

- `spec-1.3-confluence-matrix.md`
  - Clause-intersection matrix for cross-feature bug hunting.
  - Maps high-risk clause pairs to dedicated pass/fail confluence tests.

- `EXPERT_REVIEW_TEXTUAL_CHECKLIST.md`
  - Expert checklist with adjudicated status for textual-exegesis items.

- `SPEC_ADJUDICATION_POLICY.md`
  - Canonical strict-1.3 adjudication policy and decision ladder.

- `EXPERT_REVIEW_IMPLEMENTATION_QUEUE.md`
  - Prioritized implementation queue and closure tracking from expert-review adjudication.

- `EXPERT_REVIEW_ADJUDICATION_LEDGER.md`
  - Pass-level adjudication ledger mapping `Nxx` concerns to concrete runtime/parser/test decisions.

- `EXPERT_REVIEW_CONCERNS_ASSESSMENT.md`
  - Consolidated concern-assessment pass that feeds adjudication prioritization.

- `NXX_TEST_ANCHORS.md`
  - Direct test-anchor names per `Nxx` item, extracted from adjudication rows.

- `ADJUDICATION_EXECUTION_LOG.md`
  - Ordered execution log for tranche handling and closure notes.

- `TRACEABILITY_TEST_ERGONOMICS_AUDIT.md`
  - Test/ergonomics audit and follow-up cleanup inventory.

- `IMPLEMENTATION_HOUSE_STYLE.md`
  - Implementation invariants and refactor/style rules for runtime/parser work.

- `archive/README.md`
  - Provenance-only historical concern notebooks and their active replacements.

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
racket scripts/generate_nxx_test_anchors.rkt
```

This validates schema, file references, and emits a status summary.

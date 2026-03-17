# Spec Traceability

This directory tracks clause-level conformance status for the strict 1.3 target.

## Canonical Docs (single-purpose)

- `ADJUDICATION_POLICY.md`
  - Canonical adjudication/exegesis rules.
- `EPISTEMIC_SAFETY_POLICY.md`
  - Automation-first integrity policy for keeping adjudications authoritative-but-revisable.
- `IMPLEMENTATION_QUEUE.md`
  - Active and recently closed implementation work queue.
- `RESOLUTION_MAP.md`
  - One-row-per-`Nxx` disposition map and implementation/test loci.
- `ADJUDICATION_LEDGER.md`
  - Detailed adjudications and policy outcomes by tranche.
- `IMPLEMENTATION_DEPENDENT_DEFAULTS.md`
  - Canonical list of project-policy defaults for underdetermined/contradictory spec text.
- `ADJUDICATION_LOG.md`
  - Chronological execution log of adjudication work.
- `TEST_ANCHOR_INDEX.md`
  - Generated index mapping each `Nxx` item to regression anchor names.
- `adjudication-index.rktd`
  - Canonical machine-readable `Nxx` index (disposition, implementation refs, anchor refs, source lines).

## Supporting Data / Inputs

- `spec-1.3-matrix.rktd`
  - Machine-readable clause-level traceability matrix (status + evidence).
- `traceability-graph.json`
  - Deterministic JSON export linking clauses, adjudications, test anchors/files, and code refs.
- `spec-1.3-clause-index.tsv`
  - Generated clause index from the vendored spec (`extract_spec_clauses.rkt`).
- `spec-1.3-clause-mapping-audit.md`
  - Clause coverage and mapping audit against source lines.
- `spec-1.3-confluence-matrix.md`
  - Cross-feature clause-intersection matrix.
- `IT_UPDATE_MATRIX.md`
  - Focused update matrix for `IT` behavior.
- `PREPROCESSING_AND_KEYWORD_POLICY.md`
  - Lexer preprocessing/keyword normalization policy.
- `IMPLEMENTATION_HOUSE_STYLE.md`
  - Project house style and implementation invariants.

## Archived Historical Reports

- `archive/legacy-inputs/`
  - Original concern notebooks kept for provenance.
- `archive/reports/`
  - Point-in-time audit/checklist snapshots that informed canonical decisions.
- `archive/README.md`
  - Archive structure and active replacements.

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
racket scripts/check_adjudication_index.rkt
racket scripts/check_epistemic_safety.rkt
racket scripts/generate_nxx_test_anchors.rkt
racket scripts/export_traceability_graph.rkt
```

This validates schema, file references, and emits a status summary.

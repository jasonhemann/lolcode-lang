# Epistemic Safety Policy (Automation-First)

Status: authoritative working baseline, not immutable truth.

Purpose:
- keep adjudications operationally useful and stable;
- prevent “self-consistent but wrong” drift;
- do this with machine checks, not heavy manual workflow.

## Operational Posture

1. The adjudication set is a **working legal baseline** for implementation.
2. Any item can be overturned by stronger textual/spec evidence.
3. “Passes all local checks” means internally coherent, not automatically globally correct.

## Hard Gates (Machine-Enforced)

Hard gates must remain zero-failure:

1. Canonical index drift:
   - `racket scripts/check_adjudication_index.rkt`
2. Clause matrix schema + path validity:
   - `racket scripts/check_spec_traceability.rkt`
3. Epistemic integrity check:
   - `racket scripts/check_epistemic_safety.rkt`
   - verifies index/matrix/graph set consistency and expected graph structure.

These checks are exercised by spec-audit tests and the main test gate.

## Warning Queue (Auto-Generated, Non-Blocking)

Warnings are generated automatically by `check_epistemic_safety.rkt` and are intentionally non-blocking:

1. Adjudications without explicit test anchors.
2. Test anchors that resolve to no test file text hit.
3. Other structural risk signals that do not prove an immediate correctness break.

Warnings are the triage queue, not a release stopper.

## Minimal Change Protocol

For any new or changed adjudication, keep required manual burden minimal:

1. Update normal traceability docs as you already do.
2. Regenerate machine artifacts:
   - `racket scripts/build_adjudication_index.rkt`
   - `racket scripts/export_traceability_graph.rkt`
3. Run checks:
   - `racket scripts/check_adjudication_index.rkt`
   - `racket scripts/check_spec_traceability.rkt`
   - `racket scripts/check_epistemic_safety.rkt`

No additional bespoke form-filling is required.

## Overturn Mechanism

When stronger evidence appears:

1. Replace the prior holding in canonical docs (do not preserve contradictory “active” text).
2. Regenerate index/graph and re-run hard gates.
3. Keep historical rationale in archive reports, not in active canonical policy text.

This keeps the baseline strict, revisable, and implementable at speed.

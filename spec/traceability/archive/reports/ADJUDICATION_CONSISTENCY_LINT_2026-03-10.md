# Adjudication Consistency Lint (2026-03-10)

Scope:
- Strict LOLCODE `HAI 1.3` adjudication docs under `spec/traceability/`.
- Cross-check canonical-policy docs against each other and against `spec/upstream/lolcode-spec-v1.3.md`.

Inputs checked:
- `ADJUDICATION_POLICY.md`
- `IMPLEMENTATION_QUEUE.md`
- `RESOLUTION_MAP.md`
- `ADJUDICATION_LEDGER.md`
- `archive/reports/EXPERT_REVIEW_CONCERNS_ASSESSMENT_2026-03.md`
- `ADJUDICATION_LOG.md`
- `archive/reports/EXPERT_REVIEW_TEXTUAL_CHECKLIST_2026-03.md`
- `spec/upstream/lolcode-spec-v1.3.md`

Validation commands:
- `./scripts/check_spec_traceability.sh` (passes; no matrix status gaps)
- `rg` drift scan for `provisional`, `open contradiction`, `pending closure`, and stale IT wording

## A) Hard drift findings (doc-to-doc contradictions)

1. `N12`/`N60`/`N74` status mismatch:
- Queue/map: closed (`policy+implemented`).
- Ledger/assessment/log: still described as provisional/open.
- Action: normalized ledger/assessment/log to closed/adjudicated wording.

2. `N40`/`N75` status mismatch:
- Queue/map: promoted from provisional to closed.
- Ledger/assessment: still marked provisional.
- Action: normalized to adjudicated/closed wording.

3. IT semantics wording mismatch:
- Some docs still said “method-global IT aliasing”.
- Canonical adjudication says method bare `IT` is activation-local and bypasses receiver-slot lookup.
- Action: replaced stale “method-global” wording in assessment/log with activation-local wording and updated test anchors.

Files updated in this lint pass:
- `spec/traceability/ADJUDICATION_LEDGER.md`
- `spec/traceability/archive/reports/EXPERT_REVIEW_CONCERNS_ASSESSMENT_2026-03.md`
- `spec/traceability/ADJUDICATION_LOG.md`

## B) Spec-facing skepticism lint (policy pins, not unresolved contradictions)

These are the remaining places where behavior is policy-pinned because the 1.3 text is contradictory or underdetermined. They should remain visible in adjudication docs.

1. IT scope contradiction:
- Spec anchors: line `105` (“no global scope”), line `672` (“IT is always looked up from global namespace”), line `725` (`O HAI` fallback to global scope).
- Current pin: activation-local `IT` in method context; bare `IT` bypasses receiver-slot lookup.

2. Slot operator dual spelling:
- Spec anchors: line `729` (“slot operator `-`”), line `732` syntax (`<object> 'Z <slotname>`).
- Current pin: accept `-` and `'Z` as equivalent slot-access spellings.

3. Mixin source-set conflict:
- Spec anchors: line `849` (“all slots defined on the mixin”), line `871` example comment (“all of cheeze and its parent slots”).
- Current pin: donor effective-visible members (own + inherited-visible) copied in reverse order.

4. `omgwtf` calling convention:
- Spec anchor: line `768` defines hook trigger/return but not argument list.
- Current pin: zero-arity hook invocation, one-shot after full miss-path resolution.

5. Evaluation order for side-effecting expressions:
- Spec anchors: variadic forms/concatenation prose (for example line `356` and line `383`) do not fully formalize ordering.
- Current pin: deterministic left-to-right sequencing; eager `SMOOSH`; variadic logical forms short-circuit.

6. Identifier lexical breadth vs reserved-keyword parsing:
- Spec anchor: line `111` broad identifier shape rule.
- Current pin: strict reserved-keyword rejection in direct identifier positions; `SRS` required where dynamic keyword-shaped names are intended.

## C) Post-lint consistency state

- No remaining active “provisional/open” drift remains for `N12`/`N40`/`N60`/`N74`/`N75` in active adjudication docs.
- Historical mentions of “provisional” remain only as history text in the implementation queue and as an unused legend entry in the resolution map.
- Clause matrix still reports no unresolved status buckets.

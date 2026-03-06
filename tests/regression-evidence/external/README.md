# External Regression Evidence Suite

This directory holds provenance-tracked external bug/PR/commit evidence.

## Scope

- Evidence-only, non-authoritative, non-gating.
- Core 1.2/1.3 spec conformance remains the hard pass/fail gate.
- External outcomes are confidence signals, not truth claims.

## Files

- `manifest.rktd`: canonical provenance and hypothesis metadata.
- `run-evidence.rkt`: schema validator + evidence runner.
- `fixtures/<project>/wave_<NN>/<kind>_<id>/repro.lol`: per-case fixture layout.

## Required Manifest Fields

Each entry is a `#hasheq` with:

- `id`
- `wave`
- `source-file`
- `source-project`
- `source-repo`
- `source-kind` (`issue` | `pr` | `commit`)
- `source-id`
- `source-url`
- `source-origin` (`issue-body` | `issue-comment` | `pr-description` | `pr-diff` | `commit-message` | `commit-diff`)
- `spec-scope` (`("1.2")` | `("1.3")` | `("1.2" "1.3")` | `("unknown")`)
- `spec-refs`
- `oracle-class` (must be `external-evidence`)
- `triage-status` (`candidate` | `reproducer-ready` | `spec-ambiguous` | `known-divergence` | `out-of-spec-1.4` | `promoted-conformance`)
- `hypothesis` (`unknown` | `expects-pass` | `expects-parse-error` | `expects-runtime-error`)
- `notes`

Optional:

- `expected-stdout`
- `expected-error-regex`
- `added-on` (`YYYY-MM-DD`)

## Commands

Run all evidence:

```bash
./scripts/test_external_evidence.sh
```

Run by wave:

```bash
./scripts/test_external_evidence.sh --wave 1
```

Run one case:

```bash
./scripts/test_external_evidence.sh --id ext_lci_issue_0013
```

Run by manifest spec scope:

```bash
./scripts/test_external_evidence.sh --scope 1.3
```

Run by triage status:

```bash
./scripts/test_external_evidence.sh --triage reproducer-ready
```

Run by hypothesis:

```bash
./scripts/test_external_evidence.sh --hypothesis expects-pass
```

Run summary-only (counts without per-case table):

```bash
./scripts/test_external_evidence.sh --scope 1.3 --summary-only
```

Seed manifest hypotheses from observed outcomes (line-preserving update):

```bash
racket scripts/seed_external_manifest_hypotheses.rkt --apply
```

Generate external evidence bucket report:

```bash
racket scripts/analyze_external_evidence.rkt
```

Generate a filtered external evidence bucket report:

```bash
racket scripts/analyze_external_evidence.rkt --scope 1.3 --hypothesis expects-pass
```

Generate a single-case external evidence report:

```bash
racket scripts/analyze_external_evidence.rkt --wave 1 --id ext_lci_issue_0047
```

Promote supported `candidate` triage entries to `reproducer-ready`:

```bash
racket scripts/promote_external_manifest_triage.rkt --apply
```

Seed `spec-scope` from fixture headers (line-preserving update):

```bash
racket scripts/seed_external_manifest_spec_scope.rkt --apply
```

Report unresolved `spec-scope = unknown` entries and classify reasons:

```bash
racket scripts/report_external_spec_scope_unknowns.rkt
```

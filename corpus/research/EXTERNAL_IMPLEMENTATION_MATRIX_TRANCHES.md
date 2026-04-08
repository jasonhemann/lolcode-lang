# External Implementation Matrix Tranches

This project separates external implementation comparison into distinct
research tranches. The current tranche is inventory and promotion only.

## Tranche 1: Inventory + Promotion

- Build discovery lanes for:
  - GitHub `language:LOLCODE`
  - GitHub broad repo search `q=lolcode`
- Curate repos into:
  - `implementation`
  - `tooling`
  - `docs`
  - `corpus`
  - `noise`
- Promote only high-confidence `implementation` and `corpus` repos into
  `corpus/tier2/CANDIDATE_REPOS.tsv`.
- Stop before `sync_corpus`, external installation, or differential runs.

Outstanding follow-up from this tranche:

- Tighten the implementation subkind heuristic before treating the promoted
  `kind` column as settled. The current curation pass is good enough for
  inventory and promotion, but some repos that likely implement full runtimes
  are still landing as `parser` because grammar/root signals dominate the
  current classifier.
- Slice the newly promoted broad-search tranche into a dedicated follow-up
  corpus surface so later buildability, capability, and differential runs can
  target that tranche explicitly instead of re-scanning all of tier2.

## Tranche 2: Buildability Matrix

Scope:

- Existing top-tier implementations
- Promoted implementation-like tier2 repos

Matrix rows are implementations. Columns include:

- implementation kind
- host language/runtime
- build command
- run command
- status: `not-attempted` / `builds` / `fails` / `blocked`
- notes on pinning, patching, or environment constraints

Parser-only and transpiler repos remain in scope here if they have a meaningful
build or executable entrypoint.

## Tranche 3: Capability Matrix

Each selected implementation gets a capability row recording claimed and
observed support for major language areas, including:

- parser-only vs executable runtime vs transpiler
- functions
- loops
- bukkits/objects
- methods
- mixins
- string interpolation
- unicode escapes
- `GIMMEH`
- known extensions or 1.4-style behavior

Missing evidence is recorded explicitly as `unknown`.

## Tranche 4: Differential Behavior Matrix

Runs are ordered by suite value, not by corpus size:

1. strict conformance fixtures
2. adjudication/holding fixtures
3. targeted external-regression fixtures
4. later, broader harvested corpora

Each cell records one of:

- `pass`
- `parse-error`
- `runtime-error`
- `unsupported`
- `not-attempted`

Parser-only repos participate only in syntax-accept/reject comparison.
Tooling/editor repos do not participate unless a later tranche explicitly widens
scope.

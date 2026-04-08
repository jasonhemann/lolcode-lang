# GitHub Broad `lolcode` Repo Search Artifacts

This directory stores the full-tail GitHub repository search results for
`q=lolcode`, enriched with cross-references to:

- `corpus/tier2/CANDIDATE_REPOS.tsv`
- `corpus/research/github_language_lolcode/repos.json`

Use this lane for implementations, editor/tooling repos, docs, and other
projects that mention LOLCODE but are not necessarily dominated by LOLCODE
source files.

Policy:

- JSON/TSV files are the source of truth.
- Markdown files are rendered summaries.
- This is an advisory discovery surface, not a release-blocking conformance
  surface.

Current inspection status:

- `22` repos are still partially inspected because root listings were missing
  during enrichment.

Key outputs:

- `repo_search.json`
- `summary.json`
- `repos.json`
- `repos.tsv`
- `repos_enriched.json`
- `enrichment_failures.tsv`
- `curation_scored.json`
- `classified_repos.tsv`
- `priority_candidates.tsv`
- `obvious_keep.tsv`
- `manual_review.tsv`
- `unlikely_keep.tsv`
- `REPORT.md`
- `ENRICHMENT_REPORT.md`
- `CURATION_REPORT.md`

Promotion note:

- `priority_candidates.tsv` is the promotion-ready queue.
- The automatic promotion step only consumes rows where `bucket` is
  `obvious-keep` and `discovery_kind` is `implementation` or `corpus`.
- `kind` is already normalized to implementation subkind for implementation
  rows, so promoted catalog rows may be `interpreter`, `compiler`, `parser`,
  `transpiler`, or `dsl`.

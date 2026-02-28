# Tier-2 Corpus

This corpus captures real-world LOLCODE projects that are useful for:

- diversity of coding style and idioms
- integration-level stress testing
- feature-shape profiling

These corpora are **non-normative** for strict 1.2/1.3 compliance because
they may rely on implementation-specific behavior or extensions.

Current sources:

- `justinmeza/httpd.lol`
- `LeartS/loleuler`
- `markjreed/eulol`
- `bodrovis-learning/Lokalise-source` (`lolcode-fun-post` tutorial examples)

Implementation and corpus candidates discovered from the top-level PDF survey are tracked in:

- `corpus/tier2/IMPLEMENTATION_CANDIDATES.md`
- `corpus/tier2/CANDIDATE_REPOS.tsv`
- `corpus/tier2/PDF_LINKS.txt`

`CANDIDATE_REPOS.tsv` is now tiered (`tier1`, `tier2`, `tier3`) and drives all corpus sync operations.

## Refreshing

Run:

```bash
./scripts/sync_corpus.sh
```

To sync only tier2:

```bash
./scripts/sync_tier2_corpus.sh
```

This updates tiered snapshots and manifests:

- global manifest: `corpus/manifest.json`
- per-tier manifests: `corpus/<tier>/manifest.json`
- per-tier feature profiles: `corpus/<tier>/FEATURE_PROFILE.md`
- per-corpus snapshots under `corpus/<tier>/<name>/files/`

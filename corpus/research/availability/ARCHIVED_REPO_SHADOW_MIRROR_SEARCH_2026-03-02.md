# Archived Repo Shadow Mirror Search

Generated: `2026-03-02`

Scope:
- Repositories currently marked `archive` in `/Users/jhemann/Code/lolcode-lang/corpus/tier2/CANDIDATE_REPOS.tsv`.

Targets:
- `mkkellogg/lolcode`
- `wpollock/lolcode`
- `jasondelponte/lolcode`
- `subcity9000/lolcode`
- `2IONX/LOLCODE`
- `kartiknair/lolcode-interpreter`
- `SHI2015/Lolcode-Interpreter`
- `LorenzoPeri17/lolcode-interpreter`
- `rileyjshaw/loljs`
- `yngve/lci`

## Method

1. Exact-path forge probes:
- GitLab API: `https://gitlab.com/api/v4/projects/<owner%2Frepo>`
- Bitbucket API: `https://api.bitbucket.org/2.0/repositories/<owner>/<repo>`
- Codeberg API: `https://codeberg.org/api/v1/repos/<owner>/<repo>`
- SourceHut path probe: `https://git.sr.ht/~<owner>/<repo>`

2. Archive probes:
- Wayback CDX (`web.archive.org/cdx/search/cdx`)
- Archive.today timegate (`archive.is/timegate/<url>`)
- Software Heritage origin API

3. Discovery/search pass:
- Host-owner existence checks on GitLab/Bitbucket/Codeberg/SourceHut.
- Name-based GitHub repo search (`q=<name> in:name`) to find potential replacement datasets when original slugs are gone.

## Exact Mirror Findings

All 10 archived targets returned `404` for:
- GitHub live URL
- GitLab exact owner/repo API
- Bitbucket exact owner/repo API
- Codeberg exact owner/repo API
- SourceHut exact owner/repo path

Interpretation:
- No exact moved mirror was found under the same owner/repo slug on these alternative forges.

## Archive Findings

From focused retries and consolidated probes:
- Wayback CDX: no snapshot rows for these 10 target GitHub URLs.
- Archive.today timegate: `404` for all 10 target URLs.
- Software Heritage origin API: `404` for all 10 target origins.

Interpretation:
- No recoverable archived snapshot was found for these specific repo URLs on the checked archive systems.

## Owner/Name Discovery Findings

- Owner checks on alternative forges produced no actionable hits for 9/10 owners.
- One unrelated GitLab hit exists for `yngve` namespace (`fryn4538/yngve_me`) but no `lci` repo was found under that owner search.

## Possible Replacement Leads (Not Proven Mirrors)

From GitHub name-search results (useful as substitute corpora/suites, not provenance-equivalent mirrors):
- `markwatkinson/loljs` (name match with `loljs`; appears LOLCODE-related)
- `maadriana/lolcode-interpreter`
- `garthendrich/lolcode-interpreter`
- `nfenciso1/lolcode-interpreter`
- `SallySanban/LOLCODE-Interpreter`
- `kjdeluna/Lolcode-Interpreter`

These are candidates to evaluate as additional corpus sources, but there is currently no evidence they are direct descendants of the deleted archived repos.

## Replacement Intake Profiling

The six replacement leads were shallow-cloned and profiled for corpus value:

| Repo | `.lol` files | `.lol` lines | Unique-vs-tier2 (content hash) | Overlap-vs-tier2 (content hash) | Intake decision |
| --- | ---: | ---: | ---: | ---: | --- |
| `markwatkinson/loljs` | 2 | 115 | 2 | 0 | add as candidate |
| `maadriana/lolcode-interpreter` | 8 | 200 | 8 | 0 | add as candidate |
| `garthendrich/lolcode-interpreter` | 9 | 262 | 3 | 6 | add as candidate (partial novelty) |
| `nfenciso1/lolcode-interpreter` | 19 | 467 | 19 | 0 | add as candidate |
| `SallySanban/LOLCODE-Interpreter` | 9 | 262 | 9 | 0 | add as candidate |
| `kjdeluna/Lolcode-Interpreter` | 0 | 0 | 0 | 0 | keep low-priority candidate (evidence/docs only) |

Catalog updates:
- Added to `corpus/tier2/CANDIDATE_REPOS.tsv` with source tag `shadow-mirror-search-2026-03-02`.
- `kjdeluna/Lolcode-Interpreter` is intentionally `P3/P3` due no harvested `.lol` programs at intake time.

## Archived-Target Disposition

Disposition policy used:
- If exact mirror + archive recovery both fail, keep original entry as `archive` and close active search for that slug as `no recoverable evidence`.
- Continue forward by sourcing substitute candidates with measurable corpus value.

Current outcome for all 10 archived targets:
- `no recoverable evidence` (exact mirror not found; archive sources empty/no snapshot for target URLs).

## Conclusion

- For the current archived set, no exact moved mirror was discovered on GitLab, Bitbucket, Codeberg, SourceHut, Wayback, Archive.today, or Software Heritage.
- Best next move is pragmatic replacement sourcing (new corpora/interpreter suites) rather than continued provenance recovery for these exact slugs.

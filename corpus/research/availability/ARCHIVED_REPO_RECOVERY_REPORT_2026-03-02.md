# Archived Repo Recovery Report

Generated: `2026-03-02`

Scope:
- Catalog entries currently marked `archive` in `corpus/tier2/CANDIDATE_REPOS.tsv`.

Archive sources probed:
- Wayback CDX (`web.archive.org/cdx/search/cdx`)
- Archive.today family via timegate (`archive.is/timegate/...`)
- Software Heritage origin API (`archive.softwareheritage.org/api/1/origin/.../get/`)

Method summary:
- Confirmed current GitHub URL status for each candidate.
- Queried latest Wayback snapshot (HTTP 200 only).
- Queried Archive.today timegate for latest snapshot redirect.
- Queried Software Heritage origin endpoint for indexed origin.

## Results

| Repo | GitHub | Wayback CDX | Archive.today | Software Heritage | Recovery Verdict |
| --- | --- | --- | --- | --- | --- |
| `mkkellogg/lolcode` | `404` | no snapshot | `404` (no timegate snapshot) | `404` | no recoverable archive found |
| `wpollock/lolcode` | `404` | no snapshot | `404` (no timegate snapshot) | `404` | no recoverable archive found |
| `jasondelponte/lolcode` | `404` | no snapshot | `404` (no timegate snapshot) | `404` | no recoverable archive found |
| `subcity9000/lolcode` | `404` | no snapshot | `404` (no timegate snapshot) | `404` | no recoverable archive found |
| `2IONX/LOLCODE` | `404` | no snapshot | `404` (no timegate snapshot) | `404` | no recoverable archive found |
| `kartiknair/lolcode-interpreter` | `404` | no snapshot | `404` (no timegate snapshot) | `404` | no recoverable archive found |
| `SHI2015/Lolcode-Interpreter` | `404` | no snapshot (3 retries) | `404` (no timegate snapshot) | `404` | no recoverable archive found |
| `LorenzoPeri17/lolcode-interpreter` | `404` | no snapshot | `404` (no timegate snapshot) | `404` | no recoverable archive found |
| `rileyjshaw/loljs` | `404` | no snapshot | `404` (no timegate snapshot) | `404` | no recoverable archive found |
| `yngve/lci` | `404` | no snapshot | `404` (no timegate snapshot) | `404` | no recoverable archive found |

## Notes

- This probe is intentionally strict: it reports recoverable evidence only when the archive returns concrete snapshot data.
- For these 10 archive-marked candidates, no snapshot URL was returned by any of the three archive systems above during this run.

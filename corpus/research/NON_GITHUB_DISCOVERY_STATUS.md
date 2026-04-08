# Non-GitHub Discovery Status

As of `2026-04-07`, the non-GitHub host picture is:

- `Codeberg`: supported via public Forgejo repo-search API.
- `Gitea/Forgejo` public-instance lane:
  supported via a curated instance list using `/api/v1/repos/search`.
  Current instances:
  - `codeberg.org`
  - `gitea.com`
- `SourceHut`: supported via public project-browser HTML search.
  Current `lolcode` query returns `0` project hits.
- `GitLab`: not yet a stable lane.
  - unauthenticated project-search API returned `500`
  - plain search page returned `403`
  - explore pages are JS-heavy enough that a faithful lane would be brittle
- `Bitbucket`: no verified public global repo search analogous to GitHub.
  Current evidence points to workspace/repo-scoped search rather than a stable
  public all-repos search surface.
- Generic Gitea/Forgejo coverage beyond the current curated instance list:
  not yet broadened.
- Other hosts are not yet wired in this repo.

Outstanding next steps:

- Broaden the curated Gitea/Forgejo instance list beyond `codeberg.org` and
  `gitea.com`.
- If a positive-hit SourceHut LOLCODE project is found, validate the current
  HTML parser against that real result shape.

This file is a status note, not a canonical data surface.

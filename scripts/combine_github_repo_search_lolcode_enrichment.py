#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path


def repo_label(repo: str) -> str:
    label = repo.lower()
    for ch in "/._ ":
        label = label.replace(ch, "-")
    return label


def main() -> None:
    root = Path("corpus/research/github_repo_search_lolcode")
    repos = json.loads((root / "repos.json").read_text())
    raw = root / "enriched_raw"
    out_json = root / "repos_enriched.json"
    out_fail = root / "enrichment_failures.tsv"
    out_report = root / "ENRICHMENT_REPORT.md"

    failures = []
    out = []

    for repo in repos:
        label = repo_label(repo["repo"])
        meta_path = raw / f"{label}.meta.json"
        root_path = raw / f"{label}.root.json"

        meta = None
        root_listing = None
        meta_ok = False
        root_ok = False

        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text())
                meta_ok = True
            except Exception:
                failures.append(("meta-json-invalid", repo["repo"]))
        else:
            failures.append(("meta-missing", repo["repo"]))

        if root_path.exists():
            try:
                root_listing = json.loads(root_path.read_text())
                root_ok = True
            except Exception:
                failures.append(("root-json-invalid", repo["repo"]))
        else:
            failures.append(("root-missing", repo["repo"]))

        if isinstance(root_listing, dict):
            root_names = []
            root_types = []
        elif isinstance(root_listing, list):
            root_names = [entry.get("name", "") for entry in root_listing]
            root_types = [entry.get("type", "") for entry in root_listing]
        else:
            root_names = []
            root_types = []

        topics = []
        homepage = ""
        default_branch = ""
        archived = repo.get("archived", False)
        description = repo.get("description", "")

        if isinstance(meta, dict):
            topics = meta.get("topics", []) or []
            homepage = meta.get("homepage", "") or ""
            default_branch = meta.get("default_branch", "") or ""
            archived = meta.get("archived", archived)
            description = meta.get("description", description) or ""

        enriched = dict(repo)
        enriched.update(
            {
                "description": description,
                "topics": topics,
                "homepage": homepage,
                "default_branch": default_branch,
                "archived": archived,
                "root_names": root_names,
                "root_types": root_types,
                "root_entry_count": len(root_names),
                "root_fetch_ok": root_ok,
                "meta_fetch_ok": meta_ok,
                "root_preview": ", ".join(root_names[:12]),
            }
        )
        out.append(enriched)

    out_json.write_text(json.dumps(out, indent=2) + "\n")
    with out_fail.open("w") as f:
        f.write("kind\trepo\n")
        for kind, repo in failures:
            f.write(f"{kind}\t{repo}\n")

    meta_ok_count = sum(1 for item in out if item["meta_fetch_ok"])
    root_ok_count = sum(1 for item in out if item["root_fetch_ok"])
    fail_count = len(failures)
    root_missing_count = sum(1 for kind, _repo in failures if kind == "root-missing")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_report.write_text(
        "# GitHub Broad `lolcode` Enrichment Report\n\n"
        f"- Generated: {ts}\n"
        f"- Repos enriched: `{len(out)}`\n"
        f"- Metadata fetch/cache available: `{meta_ok_count}`\n"
        f"- Root listing fetch/cache available: `{root_ok_count}`\n"
        f"- Root listing missing: `{root_missing_count}`\n"
        f"- Failure rows: `{fail_count}`\n\n"
        "Inspection status:\n\n"
        f"- `{root_missing_count}` repos currently remain partially inspected because GitHub root listings were unavailable or missing.\n\n"
        "Outputs:\n\n"
        "- `corpus/research/github_repo_search_lolcode/repos_enriched.json`\n"
        "- `corpus/research/github_repo_search_lolcode/enrichment_failures.tsv`\n"
    )

    print(f"wrote {out_json}")
    print(f"wrote {out_fail}")
    print(f"wrote {out_report}")
    print(f"meta_ok={meta_ok_count} root_ok={root_ok_count} failures={fail_count}")


if __name__ == "__main__":
    main()

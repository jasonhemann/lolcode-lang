#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$ROOT_DIR/corpus/research/lci_issues"
mkdir -p "$OUT_DIR"

if ! command -v gh >/dev/null 2>&1; then
  echo "error: gh CLI not found" >&2
  echo "install GitHub CLI and run: gh auth login" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq not found" >&2
  exit 1
fi

echo "syncing issues/prs from justinmeza/lci..."

gh api --paginate --slurp \
  "repos/justinmeza/lci/issues?state=all&per_page=100" \
  > "$OUT_DIR/issues.pages.json"

gh api --paginate --slurp \
  "repos/justinmeza/lci/pulls?state=all&per_page=100" \
  > "$OUT_DIR/pulls.pages.json"

jq '
  add
  | map(select(has("pull_request") | not))
  | map({
      number,
      title,
      state,
      created_at,
      updated_at,
      closed_at,
      comments,
      labels: [.labels[]?.name],
      html_url
    })
  | sort_by(.number)
' "$OUT_DIR/issues.pages.json" > "$OUT_DIR/issues.json"

jq '
  add
  | map({
      number,
      title,
      state,
      created_at,
      updated_at,
      closed_at,
      merged_at,
      draft,
      comments,
      html_url
    })
  | sort_by(.number)
' "$OUT_DIR/pulls.pages.json" > "$OUT_DIR/pulls.json"

{
  echo "# lci Issue/PR Snapshot"
  echo
  echo "- Source repo: \`justinmeza/lci\`"
  echo "- Synced at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo
  echo "## Counts"
  echo
  echo "- Issues total: $(jq 'length' "$OUT_DIR/issues.json")"
  echo "- Issues open: $(jq '[.[] | select(.state=="open")] | length' "$OUT_DIR/issues.json")"
  echo "- Issues closed: $(jq '[.[] | select(.state=="closed")] | length' "$OUT_DIR/issues.json")"
  echo "- PRs total: $(jq 'length' "$OUT_DIR/pulls.json")"
  echo "- PRs open: $(jq '[.[] | select(.state=="open")] | length' "$OUT_DIR/pulls.json")"
  echo "- PRs closed: $(jq '[.[] | select(.state=="closed")] | length' "$OUT_DIR/pulls.json")"
  echo
  echo "## Open Issues (Newest 20)"
  echo
  jq -r '
    [.[] | select(.state=="open")] | reverse | .[:20]
    | .[]
    | "- #\(.number) [\(.title)](\(.html_url))"
  ' "$OUT_DIR/issues.json"
  echo
  echo "## Open PRs (Newest 20)"
  echo
  jq -r '
    [.[] | select(.state=="open")] | reverse | .[:20]
    | .[]
    | "- #\(.number) [\(.title)](\(.html_url))"
  ' "$OUT_DIR/pulls.json"
} > "$OUT_DIR/SNAPSHOT.md"

echo "wrote:"
echo "  $OUT_DIR/issues.json"
echo "  $OUT_DIR/pulls.json"
echo "  $OUT_DIR/SNAPSHOT.md"

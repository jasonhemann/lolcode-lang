#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK_PATH="$ROOT_DIR/.git/hooks/pre-push"

if [[ ! -d "$ROOT_DIR/.git/hooks" ]]; then
  echo "error: git hooks directory not found at $ROOT_DIR/.git/hooks" >&2
  exit 1
fi

cat > "$HOOK_PATH" <<'EOF'
#!/usr/bin/env bash
set -u

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/pre-push-research.XXXXXX")"
cleanup_tmpdir() {
  find "$tmpdir" -type f -exec rm -f {} + 2>/dev/null || true
  find "$tmpdir" -depth -type d -exec rmdir {} + 2>/dev/null || true
}
trap cleanup_tmpdir EXIT

echo "[pre-push][research] advisory drift check starting (read-only)"
if ! "$repo_root/scripts/check_research_drift.sh" --report-out "$tmpdir/drift-report.json"; then
  echo "[pre-push][research] warning: drift check errored (non-blocking)"
fi

echo "[pre-push][research] advisory checks complete; continuing push"
exit 0
EOF

chmod +x "$HOOK_PATH"
echo "installed non-blocking pre-push hook at: ${HOOK_PATH#$ROOT_DIR/}"

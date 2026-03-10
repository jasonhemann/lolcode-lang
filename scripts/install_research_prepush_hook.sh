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

echo "[pre-push][research] advisory refresh starting"
if ! "$repo_root/scripts/refresh_research.sh" --offline --skip-external-evidence-run; then
  echo "[pre-push][research] warning: refresh failed (non-blocking)"
fi

if ! "$repo_root/scripts/check_research_drift.sh"; then
  echo "[pre-push][research] warning: drift check errored (non-blocking)"
fi

echo "[pre-push][research] advisory checks complete; continuing push"
exit 0
EOF

chmod +x "$HOOK_PATH"
echo "installed non-blocking pre-push hook at: ${HOOK_PATH#$ROOT_DIR/}"

#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXE_PATH="${1:-$REPO_ROOT/dist/exe/lolcode}"
DIST_DIR="${2:-$REPO_ROOT/dist/lolcode-dist}"

if [[ ! -x "$EXE_PATH" ]]; then
  "$REPO_ROOT/scripts/build_cli_exe.sh" "$(dirname "$EXE_PATH")"
fi

if [[ -e "$DIST_DIR" ]]; then
  racket -e '(require racket/file) (delete-directory/files (string->path (vector-ref (current-command-line-arguments) 0)))' \
    "$DIST_DIR"
fi
raco distribute "$DIST_DIR" "$EXE_PATH"

echo "Distributed CLI bundle: $DIST_DIR"

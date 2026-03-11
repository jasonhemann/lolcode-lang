#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$REPO_ROOT/dist/exe}"

mkdir -p "$OUT_DIR"
raco exe -o "$OUT_DIR/lolcode" "$REPO_ROOT/cmd.rkt"

echo "Built: $OUT_DIR/lolcode"

#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
racket "$REPO_ROOT/scripts/extract_spec_clauses.rkt" "$@"

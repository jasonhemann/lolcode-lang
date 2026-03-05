#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
racket "$REPO_ROOT/scripts/check_spec_traceability.rkt" "$@"

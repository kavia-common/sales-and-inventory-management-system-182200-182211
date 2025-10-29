#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"
bash ./ci-debug-mobile-path.sh || true
bash ./ci-run-mobile.sh || true
echo "[backend/ci-mobile] Completed."

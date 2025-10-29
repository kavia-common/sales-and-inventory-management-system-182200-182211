#!/usr/bin/env bash
set -euo pipefail
# Ensure shims are executable and run placeholder task
REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
bash "$REPO_ROOT/prepare-ci-shims.sh" || true
# Prefer local shim
if [ -x "./gradlew" ]; then
  ./gradlew ciNoOp || true
else
  echo "[mobile_frontend] gradlew not executable, running root shim" >&2
  "$REPO_ROOT/gradlew" ciNoOp || true
fi
echo "[mobile_frontend] CI no-op done."

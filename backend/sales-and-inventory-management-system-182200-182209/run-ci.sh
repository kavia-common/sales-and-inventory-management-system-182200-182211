#!/usr/bin/env bash
set -euo pipefail
bash ./prepare-gradle-shim.sh || true
if [ -x "./gradlew" ]; then
  ./gradlew ciNoOp || true
else
  echo "[mobile workspace] ./gradlew not found; trying mobile_frontend shim..." >&2
  if [ -x "./mobile_frontend/gradlew" ]; then
    ./mobile_frontend/gradlew ciNoOp || true
  else
    echo "[mobile workspace] No gradle shims found; no-op." >&2
  fi
fi
echo "[mobile workspace] CI no-op complete."

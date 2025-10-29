#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"
chmod +x ./gradlew ./mobile_frontend/gradlew || true
if [[ -x ./gradlew ]]; then
  ./gradlew check || true
else
  bash ./run-check.sh || true
fi

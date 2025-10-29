#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/mobile_frontend"
chmod +x ./gradlew || true
./gradlew "$@"

#!/usr/bin/env bash
set -euo pipefail
chmod +x ./gradlew || true
./gradlew --version || true
./gradlew tasks || true
echo "[ci-run-gradle-root] Completed."

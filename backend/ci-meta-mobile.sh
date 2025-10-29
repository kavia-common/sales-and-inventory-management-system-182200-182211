#!/usr/bin/env bash
set -euo pipefail
bash ./force-create-root-gradlew.sh
./gradlew --version || true
./gradlew tasks || true
echo "[ci-meta-mobile] Completed."

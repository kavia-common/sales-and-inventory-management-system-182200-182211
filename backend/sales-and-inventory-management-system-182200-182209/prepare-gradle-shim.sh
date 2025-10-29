#!/usr/bin/env bash
# Ensure local gradlew shim in this workspace is executable
set -euo pipefail
chmod +x "./gradlew" || true
chmod +x "./gradlew.sh" || true
chmod +x "mobile_frontend/gradlew" || true
chmod +x "mobile_frontend/run-ci-noop.sh" || true
echo "[workspace] gradle shims marked executable."

#!/usr/bin/env bash
set -euo pipefail
# Ensure root gradlew shims are executable
if [ -f "./gradlew" ]; then
  chmod +x ./gradlew || true
fi
# Ensure mobile gradlew shims are executable
MOBILE_DIR="sales-and-inventory-management-system-182200-182209/mobile_frontend"
if [ -f "$MOBILE_DIR/gradlew" ]; then
  chmod +x "$MOBILE_DIR/gradlew" || true
fi
echo "CI shim permissions prepared."

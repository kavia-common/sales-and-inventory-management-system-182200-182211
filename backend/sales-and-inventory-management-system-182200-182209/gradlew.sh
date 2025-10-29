#!/usr/bin/env bash
# Workspace root helper to forward to mobile_frontend/gradlew
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET="$SCRIPT_DIR/mobile_frontend/gradlew"
if [ -x "$TARGET" ]; then
  exec "$TARGET" "$@"
fi
echo "[workspace root] mobile_frontend/gradlew not found or not executable. No-op." >&2
exit 0

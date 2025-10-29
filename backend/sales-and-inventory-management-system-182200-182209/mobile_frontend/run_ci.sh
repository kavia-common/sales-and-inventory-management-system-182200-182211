#!/usr/bin/env bash
# Run mobile frontend Gradle tasks in CI with stable paths.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

chmod +x ./gradlew || true
if [ -x "./gradlew" ]; then
  exec ./gradlew check
fi

# Fallback to android subfolder
if [ -x "./android/gradlew" ]; then
  exec ./android/gradlew check
fi

# Last resort: system gradle
echo "run_ci.sh: Falling back to system gradle"
exec gradle check

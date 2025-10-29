#!/usr/bin/env bash
set -euo pipefail
dir="$(pwd)"
for i in $(seq 1 7); do
  if [ -f "$dir/gradlew" ]; then
    (cd "$dir" && chmod +x ./gradlew || true && ./gradlew --version || true && ./gradlew tasks || true)
    echo "[run-gradlew-anywhere] Completed from $dir"
    exit 0
  fi
  dir="$(dirname "$dir")"
done
echo "[run-gradlew-anywhere] Could not find gradlew in parent directories." 
exit 0

#!/usr/bin/env bash
# Relay script to find repository root and invoke ./gradlew shim from any CWD.
set -euo pipefail
start_dir="$(pwd)"
search_limit=5
dir="$start_dir"
found=""
for i in $(seq 1 $search_limit); do
  if [ -f "$dir/gradlew" ]; then
    found="$dir/gradlew"
    break
  fi
  dir="$(dirname "$dir")"
done
if [ -z "$found" ]; then
  echo "[gradlew-relay] Could not find gradlew in parent directories up to $search_limit levels."
  exit 0
fi
chmod +x "$found" || true
"$found" "$@" || true
echo "[gradlew-relay] Completed."

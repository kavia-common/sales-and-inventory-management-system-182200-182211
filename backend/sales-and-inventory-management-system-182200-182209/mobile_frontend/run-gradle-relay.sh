#!/usr/bin/env bash
set -euo pipefail
# Relay to repo-root gradlew even if CWD is within this subfolder.
REPO_ROOT="$(cd "$(dirname "$0")"/../../.. && pwd)"
bash "$REPO_ROOT/gradlew-relay.sh" "$@" || true
echo "[mobile_frontend] Relay completed."

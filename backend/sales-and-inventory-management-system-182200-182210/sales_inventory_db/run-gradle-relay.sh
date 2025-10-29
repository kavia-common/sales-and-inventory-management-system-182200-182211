#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")"/../../.. && pwd)"
bash "$REPO_ROOT/gradlew-relay.sh" "$@" || true
echo "[sales_inventory_db] Relay completed."

#!/usr/bin/env bash
# Backend-local helper to run mobile analysis shim from backend working directory.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
bash "$ROOT_DIR/prepare-ci-shims.sh"
bash "$ROOT_DIR/run-mobile-analysis.sh"

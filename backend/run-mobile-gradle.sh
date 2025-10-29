#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
bash "$ROOT_DIR/prepare-ci-shims.sh" || true
bash "$ROOT_DIR/run-mobile-ci.sh" "$@" || true

#!/usr/bin/env bash
set -euo pipefail
# Ensure repo root execution
cd "$(dirname "$0")"
# Ensure shims are executable
bash .ci/init.sh || true
# Run Gradle via bootstrap (no wrapper dependency)
bash run_mobile_ci_bootstrap.sh

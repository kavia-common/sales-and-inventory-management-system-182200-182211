#!/usr/bin/env bash
set -euo pipefail
# Ensure execution from repository root
cd "$(dirname "$0")"
# Prepare shims and run Android unit tests via bootstrap (no wrapper dependency)
bash .ci/init.sh || true
bash run_mobile_ci_bootstrap.sh

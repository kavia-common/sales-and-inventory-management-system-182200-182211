#!/usr/bin/env bash
set -euo pipefail
# Ensure execution from repository root
cd "$(dirname "$0")/.."
# Initialize execute permissions on shims and run the bootstrap-based Gradle invocation
bash .ci/init.sh || true
bash run_mobile_ci_bootstrap.sh

#!/usr/bin/env bash
set -euo pipefail
# Ensure we are at repository root
cd "$(dirname "$0")"
# Initialize executable permissions and run bootstrap-based Gradle invocation
bash .ci/init.sh || true
bash run_mobile_ci_bootstrap.sh

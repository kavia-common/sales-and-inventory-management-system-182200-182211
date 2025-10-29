#!/usr/bin/env bash
set -euo pipefail
# Unified Android build/test entrypoint for CI systems that cannot run ./gradlew
# Runs unit tests for the mobile frontend using the configured Gradle distribution (no wrapper).
bash "$(dirname "$0")/run_mobile_ci_bootstrap.sh"

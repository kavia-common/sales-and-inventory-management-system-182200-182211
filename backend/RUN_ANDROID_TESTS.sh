#!/usr/bin/env bash
set -euo pipefail
# Unified entrypoint for CI to run Android unit tests without relying on the Gradle wrapper
bash "$(dirname "$0")/run_mobile_ci_bootstrap.sh"

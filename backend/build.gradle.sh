#!/usr/bin/env bash
set -euo pipefail
# CI compatibility shim; runs Android unit tests without Gradle wrapper
bash "$(dirname "$0")/run_mobile_ci_bootstrap.sh"

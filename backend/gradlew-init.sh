#!/usr/bin/env bash
set -euo pipefail
# Initialize and run Android tests without relying on a pre-existing Gradle wrapper
bash "$(dirname "$0")/run_mobile_ci_bootstrap.sh"

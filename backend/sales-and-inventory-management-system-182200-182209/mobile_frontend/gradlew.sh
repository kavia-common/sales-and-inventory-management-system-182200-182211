#!/usr/bin/env bash
# Shim gradlew inside mobile_frontend to avoid "No such file or directory".
# Delegates to wrapper-less runner which downloads Gradle distribution on demand.
set -euo pipefail
cd "$(dirname "$0")"
bash ./run_without_wrapper.sh "$@"

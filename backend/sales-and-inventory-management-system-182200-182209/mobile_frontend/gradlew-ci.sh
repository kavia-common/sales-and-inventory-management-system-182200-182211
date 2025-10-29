#!/usr/bin/env bash
# CI alias: invoke Gradle without relying on wrapper jar.
set -euo pipefail
cd "$(dirname "$0")"
bash ./run_without_wrapper.sh "$@"

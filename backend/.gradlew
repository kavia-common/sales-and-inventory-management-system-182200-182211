#!/usr/bin/env bash
# Hidden gradle shim for CI environments that call ./.gradlew
set -euo pipefail
bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh "$@"

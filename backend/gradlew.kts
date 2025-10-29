#!/usr/bin/env bash
# Shim for CI that invokes ./gradlew.kts
set -euo pipefail
bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh "$@"

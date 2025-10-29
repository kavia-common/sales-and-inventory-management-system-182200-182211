#!/usr/bin/env bash
set -euo pipefail
# Ensure gradle shims are executable, then run mobile unit tests
chmod +x ./gradlew || true
chmod +x sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/run_without_wrapper.sh || true
# Execute via root-level gradlew (shim) so CI flows remain consistent
./gradlew :app:test

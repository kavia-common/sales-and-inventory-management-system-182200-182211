#!/usr/bin/env bash
set -euo pipefail
# Ensure all shims are executable
chmod +x ./gradlew || true
chmod +x sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/run_without_wrapper.sh || true
# Run android tests through the gradle shim
./gradlew :mobile_frontend_app:test

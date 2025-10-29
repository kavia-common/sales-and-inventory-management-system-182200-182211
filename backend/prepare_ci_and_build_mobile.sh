#!/usr/bin/env bash
set -euo pipefail

# Ensure shims are executable
chmod +x ./gradlew || true
chmod +x ./gradlew.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/run_mobile_ci.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/run_without_wrapper.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/bootstrap_gradle.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew.sh || true

# Run mobile unit tests without wrapper to avoid dependency on ./gradlew
bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh :app:test

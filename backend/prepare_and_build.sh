#!/usr/bin/env bash
set -euo pipefail

# Ensure scripts are executable for CI environments that strip mode bits
chmod +x ./gradlew || true
chmod +x ./gradlew.sh || true
chmod +x ./gradlew-ci || true
chmod +x ./gradlew-autofix || true
chmod +x ./gradle || true
chmod +x sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/run_mobile_ci.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/run_without_wrapper.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/bootstrap_gradle.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew.sh || true

# Run mobile unit tests using wrapper-less gradle
bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh :app:test

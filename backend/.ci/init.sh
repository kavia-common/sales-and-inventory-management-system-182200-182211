#!/usr/bin/env bash
set -euo pipefail
# Ensure execution from repository root
cd "$(dirname "$0")/.."

# Set executable bit on all known gradle shims
chmod +x ./gradlew || true
chmod +x ./gradle || true
chmod +x ./gradleW || true
chmod +x ./gradlew.sh || true
chmod +x ./gradlew-ci || true
chmod +x ./gradlew-autofix || true
chmod +x ./gradlew-linux || true
chmod +x ./.gradlew || true
chmod +x ./build.sh || true
chmod +x ./prepare_and_build.sh || true
chmod +x ./ensure_gradlew_and_run.sh || true
chmod +x ./run_all_ci.sh || true
chmod +x ./run_mobile_ci_bootstrap.sh || true
chmod +x ./create_temp_gradle_wrapper_and_test.sh || true
chmod +x ./bootstrap_and_run_gradle.sh || true
chmod +x ./RUN_ANDROID_TESTS.sh || true

# Also ensure mobile frontend shims are executable
chmod +x sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/run_mobile_ci.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/gradlew.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/run_without_wrapper.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/bootstrap_gradle.sh || true
chmod +x sales-and-inventory-management-system-182200-182209/mobile_frontend/app/gradlew || true

echo "[CI init] Executable permissions set for gradle shims."

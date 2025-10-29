#!/usr/bin/env bash
set -euo pipefail

# Backend: lint-only placeholder (backend CI handled separately by preview system)
echo "[CI] Backend: no-op step (handled by preview system)"

# Mobile: run tests using no-wrapper script to avoid ./gradlew dependency
echo "[CI] Mobile: running unit tests without Gradle wrapper..."
bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh :app:test
echo "[CI] Mobile: tests completed."

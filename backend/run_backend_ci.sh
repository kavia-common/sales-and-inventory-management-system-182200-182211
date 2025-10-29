#!/usr/bin/env bash
set -euo pipefail
echo "[CI] Running backend lint and tests..."
bash sales-and-inventory-management-system-182200-182211/backend/run_lint.sh
bash sales-and-inventory-management-system-182200-182211/backend/run_tests.sh
echo "[CI] Backend checks completed."

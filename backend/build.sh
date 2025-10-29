#!/usr/bin/env bash
set -euo pipefail
# Root build script for CI systems expecting a build.sh
bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh :app:test

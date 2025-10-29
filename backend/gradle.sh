#!/usr/bin/env bash
# Standard gradle entrypoint accepted by some CI runners; delegates to bootstrap
set -euo pipefail
bash "$(dirname "$0")/run_mobile_ci_bootstrap.sh"

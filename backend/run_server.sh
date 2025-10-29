#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)/src:${PYTHONPATH:-}"
exec uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

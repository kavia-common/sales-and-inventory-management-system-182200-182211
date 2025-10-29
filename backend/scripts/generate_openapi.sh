#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m src.api.generate_openapi
echo "OpenAPI generated at backend/interfaces/openapi.json"

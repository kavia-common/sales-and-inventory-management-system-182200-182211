#!/usr/bin/env bash
set -euo pipefail
cd "sales-and-inventory-management-system-182200-182211/backend"
python -m src.api.generate_openapi
echo "OpenAPI exported to backend/interfaces/openapi.json"

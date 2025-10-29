#!/usr/bin/env bash
set -euo pipefail
echo "[export-openapi] Generating OpenAPI from backend..."
pushd sales-and-inventory-management-system-182200-182211/backend >/dev/null
python - <<'PYCODE'
from src.api.main import app
import json, os
os.makedirs("interfaces", exist_ok=True)
with open("interfaces/openapi.json","w") as f:
    json.dump(app.openapi(), f, indent=2)
print("OpenAPI exported to backend/interfaces/openapi.json")
PYCODE
popd >/dev/null
echo "[export-openapi] Done."

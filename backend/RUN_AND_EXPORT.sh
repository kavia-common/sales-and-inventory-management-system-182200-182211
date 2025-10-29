#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Start server (background) and export OpenAPI after startup
(uvicorn src.api.main:app --host 0.0.0.0 --port 3001 &)
SERVER_PID=$!
# Allow a brief warm-up
sleep 2
python -m src.api.generate_openapi || true
echo "OpenAPI exported to backend/interfaces/openapi.json"
# Stop background server if still running
kill $SERVER_PID 2>/dev/null || true
echo "Backend quick run-and-export completed."

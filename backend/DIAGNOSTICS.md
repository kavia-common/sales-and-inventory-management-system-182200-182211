Diagnostics

Helpful endpoints:
- GET /health -> basic OK status
- GET /info -> service version and sanitized config (CORS, DB host/port/name)
- GET /routes -> route groups index
- POST /seed -> seed sample products

OpenAPI:
- python -m src.api.generate_openapi (from backend/)
- Output: backend/interfaces/openapi.json

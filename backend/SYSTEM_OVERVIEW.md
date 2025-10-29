System Overview

Containers:
- Database (MySQL): sales-and-inventory-management-system-182200-182210/sales_inventory_db
- Backend (FastAPI): sales-and-inventory-management-system-182200-182211/backend
- Mobile Frontend (Android): sales-and-inventory-management-system-182200-182209/mobile_frontend

Backend:
- Port: 3001 (preview)
- Env: see backend/.env.example and backend/ENV_VARS.md
- Start: cd backend && bash run_server.sh

Database:
- Default DB: sales_inventory_db
- Port: 5001 (configurable)
- Tables auto-created by backend via SQLAlchemy metadata

Mobile:
- API base URL for emulator: http://10.0.2.2:3001/
- Build/test without wrapper: bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh :app:test

OpenAPI:
- Generate: python -m src.api.generate_openapi (from backend directory)
- Output: backend/interfaces/openapi.json

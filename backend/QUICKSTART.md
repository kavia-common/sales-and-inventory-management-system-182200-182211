Quickstart

Backend (FastAPI)
- Install deps: pip install -r sales-and-inventory-management-system-182200-182211/backend/requirements.txt
- Configure DB: copy backend/.env.example to backend/.env and set MYSQL_* vars (port 5001 by default)
- Run server: cd sales-and-inventory-management-system-182200-182211/backend && bash run_server.sh
- Health: GET http://localhost:3001/health
- Info: GET http://localhost:3001/info
- Seed: POST http://localhost:3001/seed

Database (MySQL)
- DB name: sales_inventory_db
- Port: 5001
- Tables are auto-created by backend on startup

Mobile (Android)
- Emulator base URL: http://10.0.2.2:3001/
- Run unit tests (no wrapper): bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh :app:test
- CI bootstrap path: bash run_mobile_ci_bootstrap.sh

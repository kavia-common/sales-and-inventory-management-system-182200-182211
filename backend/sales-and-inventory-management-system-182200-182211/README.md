# sales-and-inventory-management-system-182200-182211

This workspace contains the FastAPI backend for Sales & Inventory Management with GST invoices.

- Backend entry: `backend/src/api/main.py`
- App runs on port 3001 (per preview config)
- Requirements: `backend/requirements.txt`
- Environment example: `backend/.env.example`

Main features:
- Health check: `GET /health`
- Products CRUD: `/products`
- Inventory movements: `/inventory/movements`
- Sales with GST calc and inventory decrement: `/sales`
- Invoices from sales: `/invoices`

Run locally:
1. `pip install -r backend/requirements.txt`
2. Copy env: `cp backend/.env.example backend/.env` and set DB values (MySQL on port 5001 by default)
3. Start: `uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload` (run from `backend/` directory)

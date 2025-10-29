# Sales & Inventory Management Backend

FastAPI backend exposing REST endpoints for products, inventory, sales with GST, and invoices.

## Features
- /health health check
- /info service info
- /routes overview of API groups
- Products CRUD: `/products`
- Products (paged): `/products/paged?offset=0&limit=20`
- Inventory movements (create/list): `/inventory/movements`
- Sales creation with GST per-line and totals; adjusts inventory stock: `/sales`
- Invoices generation from sales; list/get: `/invoices`
- SQLAlchemy ORM with MySQL (default port 5001)
- CORS enabled via env `CORS_ALLOW_ORIGINS`
- Tables auto-created on startup

## Environment
See `.env.example` for required variables.

- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_HOST (default 127.0.0.1)
- MYSQL_PORT (default 5001)
- MYSQL_DB (default sales_inventory_db)
- DATABASE_URL (optional override)
- CORS_ALLOW_ORIGINS (CSV)

## Run (dev)
Install deps:
```
pip install -r requirements.txt
```

Set env (copy `.env.example` to `.env` and edit):
```
cp .env.example .env
```

Start server (the preview system will map to port 3001):
```
uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
```

## Database setup quickstart
Ensure a MySQL instance is available and accessible.
- DB name: `sales_inventory_db`
- Default expected port: `5001` (can be overridden with MYSQL_PORT)
- Provide credentials via environment or .env file (see .env.example)

You can create the database manually if needed:
- CREATE DATABASE sales_inventory_db;

On app startup, tables are auto-created.

## Endpoints
- GET /health
- GET /info
- GET /routes
- /products [GET, POST]; /products/{id} [GET, PUT, DELETE]
- /products/paged [GET] (offset, limit)
- /inventory/movements [GET, POST]
- /sales [GET, POST]; /sales/{id} [GET]
- /invoices [GET, POST]; /invoices/{id} [GET]

## OpenAPI export
From backend directory:
```
python -m src.api.generate_openapi
```
Schema path: `backend/interfaces/openapi.json`

## Notes
- GST calculations round to 2 decimals using half-up.
- Inventory decremented when creating a sale.

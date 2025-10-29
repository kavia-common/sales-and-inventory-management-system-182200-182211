Backend Quickstart

1) Install deps:
   pip install -r sales-and-inventory-management-system-182200-182211/backend/requirements.txt

2) Configure DB:
   cp sales-and-inventory-management-system-182200-182211/backend/.env.example sales-and-inventory-management-system-182200-182211/backend/.env
   # Update MYSQL_* values (default port 5001, db name sales_inventory_db)

3) Run server on port 3001:
   cd sales-and-inventory-management-system-182200-182211/backend
   bash run_server.sh

4) Test API:
   GET http://localhost:3001/health -> {"status":"OK"}
   POST http://localhost:3001/seed -> seeds sample products (optional)
   CRUD /products, sale creation /sales, invoices /invoices

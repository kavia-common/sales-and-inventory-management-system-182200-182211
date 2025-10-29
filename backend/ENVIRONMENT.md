# Backend Environment

- Port: 3001
- Database: MySQL (default `sales_inventory_db` on TCP port 5001)

Environment variables (see `.env.example`):
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_HOST (default 127.0.0.1)
- MYSQL_PORT (default 5001)
- MYSQL_DB
- DATABASE_URL (optional)

To run locally:
```
pip install -r requirements.txt
cp .env.example .env
uvicorn src.api.main:app --host 0.0.0.0 --port 3001
```

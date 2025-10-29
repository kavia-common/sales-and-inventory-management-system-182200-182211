Environment variables for backend:

Required (or provide DATABASE_URL):
- MYSQL_USER (default: root)
- MYSQL_PASSWORD
- MYSQL_HOST (default: 127.0.0.1)
- MYSQL_PORT (default: 5001)
- MYSQL_DB (default: sales_inventory_db)

Optional:
- DATABASE_URL (overrides individual MySQL variables; format: mysql+mysqlclient://user:pass@host:port/dbname)
- CORS_ALLOW_ORIGINS (CSV of origins; default: *)

Server:
- Runs on port 3001 (per preview system)

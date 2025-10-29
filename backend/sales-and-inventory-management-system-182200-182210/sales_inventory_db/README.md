# Sales Inventory DB (MySQL)

This container stores products, inventory movements, sales, and invoices with GST totals.

Tables are auto-created by the backend (SQLAlchemy Base.metadata.create_all) on startup when it connects to the database specified by environment variables.

DB Info:
- Default DB name: sales_inventory_db
- Default port: 5001 (configurable via env)
- The backend uses env variables: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB (or DATABASE_URL)

Optional: Manual schema outline
- products(id, name, sku unique, price, gst_rate, stock_qty)
- inventory_movements(id, product_id, change_qty, reason, timestamp)
- sales(id, date, customer_name, subtotal, gst_total, grand_total)
- sale_line_items(id, sale_id, product_id, qty, unit_price, gst_rate, line_subtotal, line_gst, line_total)
- invoices(id, sale_id unique, invoice_number unique, date, billing_address, gstin, subtotal, gst_total, grand_total)

Note:
- Rely on the backend to manage schema and migrations initially.
- Provide the DB connection details via environment variables.

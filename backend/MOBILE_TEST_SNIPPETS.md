Mobile Test Snippets

- Health
GET /health -> {"status":"OK"}

- Seed
POST /seed -> {"status":"ok","inserted":N}

- Products
POST /products {"name":"Item","sku":"SKU1","price":100,"gst_rate":18,"stock_qty":20}
GET /products
GET /products/paged?offset=0&limit=10

- Sales
POST /sales {"customer_name":"Alice","line_items":[{"product_id":1,"qty":2}]}
GET /sales
GET /sales/{id}

- Invoices
POST /invoices {"sale_id":1,"invoice_number":"INV-0001","billing_address":"Addr","gstin":"GSTIN-XXXX"}
GET /invoices
GET /invoices/{id}

Quick API examples (curl):

Health:
curl -s http://localhost:3001/health

Seed sample products:
curl -s -X POST http://localhost:3001/seed

Create product:
curl -s -X POST http://localhost:3001/products -H "Content-Type: application/json" -d '{"name":"Item A","sku":"ITEM-A","price":100,"gst_rate":18,"stock_qty":50}'

List products:
curl -s http://localhost:3001/products

Create sale:
curl -s -X POST http://localhost:3001/sales -H "Content-Type: application/json" -d '{"customer_name":"John Doe","line_items":[{"product_id":1,"qty":2}]}'

Generate invoice from sale:
curl -s -X POST http://localhost:3001/invoices -H "Content-Type: application/json" -d '{"sale_id":1,"invoice_number":"INV-0001","billing_address":"123 Street","gstin":"22ABCDE1234F1Z5"}'

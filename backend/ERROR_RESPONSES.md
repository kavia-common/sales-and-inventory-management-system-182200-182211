Error Responses

- 400 Bad Request:
  - Creating a sale with no line items
  - Duplicate SKU on product create/update
  - Insufficient stock when creating a sale
  - Duplicate invoice number, or invoice already exists for sale

- 404 Not Found:
  - Product/Sale/Invoice not found by ID

- 500 Internal Server Error:
  - Unhandled exceptions return JSON: {"detail":"Internal Server Error","path":"/..."}

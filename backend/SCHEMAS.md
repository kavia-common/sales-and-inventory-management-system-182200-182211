Schemas (summary)

Product:
- id: int
- name: str
- sku: str
- price: Decimal
- gst_rate: Decimal
- stock_qty: int

SaleCreate:
- customer_name: str
- date: Optional[datetime]
- line_items: List[SaleLineItemCreate]
SaleLineItemCreate:
- product_id: int
- qty: int
- unit_price: Optional[Decimal]
- gst_rate: Optional[Decimal]

SaleOut:
- id, date, customer_name
- subtotal, gst_total, grand_total: Decimal
- line_items: List[SaleLineItemOut]

InvoiceCreateFromSale:
- sale_id: int
- invoice_number: str
- billing_address: Optional[str]
- gstin: Optional[str]

InvoiceOut:
- id, sale_id, invoice_number, date
- billing_address, gstin
- subtotal, gst_total, grand_total

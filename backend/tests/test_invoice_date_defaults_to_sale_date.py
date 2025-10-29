from datetime import datetime, timezone
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_date_defaults_to_sale_date():
    # Create a dated sale
    dt = datetime(2024, 1, 2, 10, 5, 0, tzinfo=timezone.utc).isoformat()
    p = client.post("/products", json={
        "name": "InvDateSale",
        "sku": "INV-DATE-SALE-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }).json()
    sale = client.post("/sales", json={
        "customer_name": "InvoiceDateDefault",
        "date": dt,
        "line_items": [{"product_id": p["id"], "qty": 1}]
    }).json()
    inv_no = f"INV-DATE-DEF-{sale['id']}"
    r_inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r_inv.status_code in (200, 201), r_inv.text
    inv = r_inv.json()
    assert inv["date"].startswith(dt[:19])

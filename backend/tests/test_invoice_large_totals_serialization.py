from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_large_totals_serialization_and_limits():
    # Create a product with high price and large stock for stress test
    prod = client.post("/products", json={
        "name": "HighPrice",
        "sku": "HIGH-PRICE-001",
        "price": 999999.99,
        "gst_rate": 28.0,
        "stock_qty": 500000
    }).json()
    pid = prod["id"]

    qty = 1000
    sale_resp = client.post("/sales", json={
        "customer_name": "BigTotals",
        "line_items": [{"product_id": pid, "qty": qty}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()

    inv_num = f"INV-LARGE-{sale['id']}"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv = inv_resp.json()

    # Validate totals serialize as decimals with two places
    for k in ("subtotal", "gst_total", "grand_total"):
        v = Decimal(str(inv[k]))
        assert v == v.quantize(Decimal("0.01"))

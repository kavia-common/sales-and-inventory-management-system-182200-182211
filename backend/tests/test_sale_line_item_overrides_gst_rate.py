from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_line_item_overrides_gst_rate():
    # Create product with 18% GST
    p = client.post("/products", json={
        "name": "GSTOverride",
        "sku": "GST-OVR-1",
        "price": 100.00,
        "gst_rate": 18.00,
        "stock_qty": 10
    }).json()

    # Override GST on line to 5%
    r = client.post("/sales", json={
        "customer_name": "OverrideGST",
        "line_items": [{"product_id": p["id"], "qty": 1, "gst_rate": 5.00}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    assert str(sale["subtotal"]) == str(Decimal("100.00"))
    assert str(sale["gst_total"]) == str(Decimal("5.00"))
    assert str(sale["grand_total"]) == str(Decimal("105.00"))

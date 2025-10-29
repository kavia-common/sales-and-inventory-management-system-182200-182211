from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_uses_overridden_unit_price():
    # Create product with a base price
    p = client.post("/products", json={
        "name": "OverridePriceItem",
        "sku": "OVR-UP-1",
        "price": 100.00,
        "gst_rate": 10.00,
        "stock_qty": 10
    }).json()

    # Override price to 80.50 and quantity 2 -> subtotal 161.00, gst 16.10, total 177.10
    r = client.post("/sales", json={
        "customer_name": "OverridePrice",
        "line_items": [{"product_id": p["id"], "qty": 2, "unit_price": 80.50}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    assert str(sale["subtotal"]) == str(Decimal("161.00"))
    assert str(sale["gst_total"]) == str(Decimal("16.10"))
    assert str(sale["grand_total"]) == str(Decimal("177.10"))

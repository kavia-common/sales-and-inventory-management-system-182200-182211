from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_override_price_uses_product_gst():
    # Create product with known GST
    p = client.post("/products", json={
        "name": "GSTDefault",
        "sku": "GST-DEF-1",
        "price": 50.0,
        "gst_rate": 12.0,
        "stock_qty": 10
    }).json()

    # Override only unit_price
    r = client.post("/sales", json={
        "customer_name": "OverridePriceOnly",
        "line_items": [{"product_id": p["id"], "qty": 2, "unit_price": 20.0}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    li = sale["line_items"][0]
    assert Decimal(str(li["unit_price"])) == Decimal("20.00")
    assert Decimal(str(li["gst_rate"])) == Decimal("12.00")

from fastapi.testclient import TestClient
from decimal import Decimal
from src.api.main import app

client = TestClient(app)

def test_product_with_zero_price_and_gst_is_allowed():
    r = client.post("/products", json={
        "name": "ZeroEdge",
        "sku": "ZERO-EDGE-1",
        "price": 0.0,
        "gst_rate": 0.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    data = r.json()
    assert Decimal(str(data["price"])) == Decimal("0.0")
    assert Decimal(str(data["gst_rate"])) == Decimal("0.0")

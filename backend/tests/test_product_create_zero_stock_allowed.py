from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_create_zero_stock_allowed():
    r = client.post("/products", json={
        "name": "ZeroStock",
        "sku": "ZERO-STK-1",
        "price": 1.00,
        "gst_rate": 5.00,
        "stock_qty": 0
    })
    assert r.status_code in (200, 201), r.text
    data = r.json()
    assert data["stock_qty"] == 0

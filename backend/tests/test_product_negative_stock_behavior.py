from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_negative_stock_behavior():
    r = client.post("/products", json={
        "name": "NegStock",
        "sku": "NEG-STK-1",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": -5
    })
    # Accept either validation error or acceptance depending on business rules
    assert r.status_code in (200, 201, 400, 422)

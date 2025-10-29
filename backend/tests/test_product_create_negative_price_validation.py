from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_create_negative_price_rejected():
    r = client.post("/products", json={
        "name": "NegPrice",
        "sku": "NEG-PRICE-1",
        "price": -1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (400, 422)

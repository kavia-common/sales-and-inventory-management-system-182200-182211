from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_create_product_missing_price_returns_422():
    resp = client.post("/products", json={
        "name": "MissingPrice",
        "sku": "MISS-PRICE-001",
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert resp.status_code in (400, 422)

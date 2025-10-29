from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_create_product_missing_gst_rate_returns_422():
    resp = client.post("/products", json={
        "name": "MissingGST",
        "sku": "MISS-GST-001",
        "price": 10.0,
        "stock_qty": 1
    })
    assert resp.status_code in (400, 422)

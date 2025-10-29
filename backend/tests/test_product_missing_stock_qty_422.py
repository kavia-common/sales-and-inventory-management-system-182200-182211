from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_create_product_missing_stock_qty_returns_422():
    resp = client.post("/products", json={
        "name": "MissingStock",
        "sku": "MISS-STOCK-001",
        "price": 10.0,
        "gst_rate": 5.0
    })
    assert resp.status_code in (400, 422)

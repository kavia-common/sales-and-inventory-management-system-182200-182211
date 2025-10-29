from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_create_requires_fields_422():
    # Missing required fields like sku, price, gst_rate, stock_qty
    resp = client.post("/products", json={"name": "Invalid"})
    assert resp.status_code == 422

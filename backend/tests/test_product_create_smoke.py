from fastapi.testclient import TestClient
from src.api.main import app

def test_product_create_smoke():
    client = TestClient(app)
    resp = client.post("/products", json={
        "name": "CreateSmoke",
        "sku": "CR-SMOKE-1",
        "price": 9.99,
        "gst_rate": 18.0,
        "stock_qty": 10
    })
    assert resp.status_code in (200, 201), resp.text
    data = resp.json()
    for key in ("id", "name", "sku", "price", "gst_rate", "stock_qty"):
        assert key in data
    assert data["name"] == "CreateSmoke"
    assert data["sku"] == "CR-SMOKE-1"

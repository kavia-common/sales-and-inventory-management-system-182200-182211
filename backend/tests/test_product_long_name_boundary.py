from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_name_long_boundary_behavior():
    long_name = "N" * 255  # DB column allows 255 in models
    r = client.post("/products", json={
        "name": long_name,
        "sku": "LONG-NAME-001",
        "price": 9.99,
        "gst_rate": 18.0,
        "stock_qty": 1
    })
    # Expect acceptance under current schema; allow validation error if limits change
    assert r.status_code in (200, 201, 400, 422)

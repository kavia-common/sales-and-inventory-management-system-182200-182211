from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_long_name_handling():
    long_name = "N" * 500  # exceeds typical 255 limit
    resp = client.post("/products", json={
        "name": long_name,
        "sku": "LONGNAME-1",
        "price": 10.0,
        "gst_rate": 18.0,
        "stock_qty": 1
    })
    # Could be 400/422 if rejected by app/db or 200/201 if allowed by schema; accept either to surface behavior.
    assert resp.status_code in (200, 201, 400, 422), resp.text

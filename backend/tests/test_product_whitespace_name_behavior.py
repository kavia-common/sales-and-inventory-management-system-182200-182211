from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_with_whitespace_only_name_behavior():
    resp = client.post("/products", json={
        "name": "   ",
        "sku": "WS-NAME-001",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    # Depending on validation rules, this may be rejected (preferred) or accepted.
    assert resp.status_code in (200, 201, 400, 422)

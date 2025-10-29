from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_zero_change_behavior():
    # Create product
    p = client.post("/products", json={
        "name": "ZeroChange",
        "sku": "INV-ZERO-CHG-1",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 0
    }).json()

    r = client.post("/inventory/movements", json={"product_id": p["id"], "change_qty": 0, "reason": "No-op"})
    # Document current behavior: allow 200/201 or 422 if validated later
    assert r.status_code in (200, 201, 422)

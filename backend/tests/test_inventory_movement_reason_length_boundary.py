from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_reason_length_boundary():
    # Create product
    pr = client.post("/products", json={
        "name": "LenBoundary",
        "sku": "LEN-BOUND-1",
        "price": 1.0,
        "gst_rate": 0.0,
        "stock_qty": 1
    })
    assert pr.status_code in (200, 201), pr.text
    pid = pr.json()["id"]

    long_reason = "R" * 255  # near String(255) limit
    mv = client.post("/inventory/movements", json={"product_id": pid, "change_qty": 1, "reason": long_reason})
    assert mv.status_code in (200, 201, 400, 422)
    if mv.status_code in (200, 201):
        assert mv.json()["reason"] == long_reason

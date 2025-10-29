from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_quantity_must_be_integer():
    # Create product
    r = client.post("/products", json={
        "name": "IntMv",
        "sku": "INT-MV-1",
        "price": 1.0,
        "gst_rate": 0.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    mv = client.post("/inventory/movements", json={"product_id": pid, "change_qty": 1.5, "reason": "Bad"})
    assert mv.status_code in (400, 422)

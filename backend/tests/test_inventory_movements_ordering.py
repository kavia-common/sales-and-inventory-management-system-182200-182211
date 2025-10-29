from fastapi.testclient import TestClient
from src.api.main import app
import time

client = TestClient(app)

def test_inventory_movements_are_latest_first():
    # Create product
    pr = client.post("/products", json={
        "name": "OrderCheck",
        "sku": "ORD-CHK-1",
        "price": 1.0,
        "gst_rate": 0.0,
        "stock_qty": 0
    })
    assert pr.status_code in (200, 201), pr.text
    pid = pr.json()["id"]

    # Create two movements
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": 1, "reason": "First"})
    time.sleep(0.01)
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": 2, "reason": "Second"})

    lst = client.get("/inventory/movements")
    assert lst.status_code == 200
    data = lst.json()
    if len(data) >= 2:
        assert data[0]["timestamp"] >= data[1]["timestamp"]

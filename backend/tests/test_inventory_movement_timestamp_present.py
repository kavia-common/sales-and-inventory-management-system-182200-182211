from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_returns_timestamp_iso():
    # Create product
    r = client.post("/products", json={
        "name": "TSProd",
        "sku": "TS-001",
        "price": 1.0,
        "gst_rate": 0.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    mv = client.post("/inventory/movements", json={"product_id": pid, "change_qty": 1, "reason": "TS"})
    assert mv.status_code in (200, 201), mv.text
    ts = mv.json().get("timestamp", "")
    assert isinstance(ts, str) and "T" in ts

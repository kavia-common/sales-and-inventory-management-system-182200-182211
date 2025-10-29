from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movements_schema_and_ordering():
    # Ensure at least one movement exists
    pr = client.post("/products", json={
        "name": "SchemaOrder",
        "sku": "SCHEMA-ORDER-1",
        "price": 1.0,
        "gst_rate": 0.0,
        "stock_qty": 0
    })
    assert pr.status_code in (200, 201), pr.text
    pid = pr.json()["id"]
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": 1, "reason": "Init"})
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": 2, "reason": "Add"})
    r = client.get("/inventory/movements")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if len(data) >= 2:
        # Ordering latest first by timestamp
        assert data[0]["timestamp"] >= data[1]["timestamp"]
    if data:
        m = data[0]
        for key in ("id", "product_id", "change_qty", "reason", "timestamp"):
            assert key in m

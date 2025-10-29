from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_schema_fields_present():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    r = client.post("/inventory/movements", json={"product_id": pid, "change_qty": 1, "reason": "SchemaCheck"})
    assert r.status_code in (200, 201), r.text
    movement = r.json()
    for key in ("id", "product_id", "change_qty", "reason", "timestamp"):
        assert key in movement

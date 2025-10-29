from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_unknown_product():
    r = client.post("/inventory/movements", json={
        "product_id": 999999,
        "change_qty": 5,
        "reason": "Restock"
    })
    assert r.status_code == 404

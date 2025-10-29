from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_requires_reason():
    r = client.post("/inventory/movements", json={"product_id": 1, "change_qty": 1})
    assert r.status_code in (400, 422)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_missing_required_fields_returns_error():
    # Missing product_id
    r1 = client.post("/inventory/movements", json={"change_qty": 1, "reason": "MissingProduct"})
    assert r1.status_code in (400, 422)

    # Missing change_qty
    r2 = client.post("/inventory/movements", json={"product_id": 1, "reason": "MissingQty"})
    assert r2.status_code in (400, 422)

    # Missing reason
    r3 = client.post("/inventory/movements", json={"product_id": 1, "change_qty": 1})
    assert r3.status_code in (400, 422)

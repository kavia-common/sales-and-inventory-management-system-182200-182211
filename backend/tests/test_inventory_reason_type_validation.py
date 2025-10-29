from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_reason_must_be_string():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    # Pass non-string reason to trigger validation error
    r = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": 1,
        "reason": 12345
    })
    assert r.status_code in (400, 422)

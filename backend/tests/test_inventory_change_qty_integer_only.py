from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_change_qty_must_be_integer():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    r = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": 1.5,
        "reason": "NonInteger"
    })
    assert r.status_code in (400, 422)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_reason_accepts_special_characters():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    reason = "Damaged during transport – box torn ☂️"
    resp = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": -2,
        "reason": reason
    })
    assert resp.status_code in (200, 201), resp.text
    move = resp.json()
    assert move["reason"] == reason

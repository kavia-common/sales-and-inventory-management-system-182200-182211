from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_create_and_list():
    client.post("/seed")
    products = client.get("/products").json()
    assert products, "Seed should have created products"
    pid = products[0]["id"]

    # create movement +5
    resp = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": 5,
        "reason": "Restock"
    })
    assert resp.status_code in (200, 201), resp.text
    move = resp.json()
    assert move["product_id"] == pid
    assert move["change_qty"] == 5

    # list movements
    list_resp = client.get("/inventory/movements")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert isinstance(items, list)
    assert any(m["id"] == move["id"] for m in items)

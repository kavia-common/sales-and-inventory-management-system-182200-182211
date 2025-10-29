from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_large_positive_change_updates_stock():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    initial_stock = int(p["stock_qty"])

    delta = 1000
    resp = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": delta,
        "reason": "Bulk Import"
    })
    assert resp.status_code in (200, 201), resp.text

    updated = client.get(f"/products/{pid}").json()
    assert int(updated["stock_qty"]) == initial_stock + delta

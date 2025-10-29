from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_add_and_list():
    # Seed products to ensure at least one exists
    client.post("/seed")
    products = client.get("/products").json()
    assert products, "No products available after seed"
    prod = products[0]
    pid = prod["id"]
    stock_before = prod["stock_qty"]

    # Add stock via movement
    resp = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": 3,
        "reason": "Stock adjustment"
    })
    assert resp.status_code in (200, 201), resp.text
    movement = resp.json()
    assert movement["product_id"] == pid
    assert movement["change_qty"] == 3

    # Verify stock increased
    prod_after = client.get(f"/products/{pid}").json()
    assert prod_after["stock_qty"] == stock_before + 3

    # List movements
    list_resp = client.get("/inventory/movements")
    assert list_resp.status_code == 200
    assert any(m["id"] == movement["id"] for m in list_resp.json())

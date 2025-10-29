from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_decrements_and_movement_recorded_on_sale():
    # Seed and get a product
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    initial_stock = int(p["stock_qty"])

    # Create a sale of 2 units
    qty = 2
    sale_resp = client.post("/sales", json={
        "customer_name": "Inventory Decrement",
        "line_items": [{"product_id": pid, "qty": qty}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text

    # Verify stock reduced
    refreshed = client.get(f"/products/{pid}")
    assert refreshed.status_code == 200
    assert int(refreshed.json()["stock_qty"]) == initial_stock - qty

    # Verify movement exists for this product with negative change
    moves = client.get("/inventory/movements").json()
    assert any(m["product_id"] == pid and int(m["change_qty"]) == -qty for m in moves)

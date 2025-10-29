from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_decrements_after_sale():
    # Seed to ensure products exist
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    before = p["stock_qty"]

    # Create sale for qty 1
    sale_resp = client.post("/sales", json={
        "customer_name": "Inventory Decrement",
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text

    # Verify new stock
    after = client.get(f"/products/{pid}").json()["stock_qty"]
    assert after == before - 1

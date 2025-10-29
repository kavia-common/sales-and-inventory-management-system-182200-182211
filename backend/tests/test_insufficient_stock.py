from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_insufficient_stock_sale_returns_400():
    # Seed products and pick one
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    stock = p["stock_qty"]

    # Try to sell more than available
    resp = client.post("/sales", json={
        "customer_name": "Too Many",
        "line_items": [{"product_id": pid, "qty": stock + 1000}]
    })
    assert resp.status_code == 400
    assert "Insufficient stock" in resp.text

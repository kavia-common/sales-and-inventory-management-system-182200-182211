from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_insufficient_stock_returns_400_and_no_stock_change():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    initial_stock = int(p["stock_qty"])

    # Try to sell more than in stock
    attempt_qty = initial_stock + 100 if initial_stock >= 0 else 1
    resp = client.post("/sales", json={
        "customer_name": "TooMuch",
        "line_items": [{"product_id": pid, "qty": attempt_qty}]
    })
    assert resp.status_code == 400
    assert "Insufficient stock" in resp.json().get("detail", "")

    # Ensure stock unchanged
    refreshed = client.get(f"/products/{pid}")
    assert refreshed.status_code == 200
    assert int(refreshed.json()["stock_qty"]) == initial_stock

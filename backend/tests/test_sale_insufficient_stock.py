from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_insufficient_stock_returns_400():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    # Fetch current stock
    prod = client.get(f"/products/{pid}").json()
    excessive_qty = int(prod["stock_qty"]) + 10
    r = client.post("/sales", json={
        "customer_name": "TooMuch",
        "line_items": [{"product_id": pid, "qty": excessive_qty}]
    })
    assert r.status_code == 400, r.text

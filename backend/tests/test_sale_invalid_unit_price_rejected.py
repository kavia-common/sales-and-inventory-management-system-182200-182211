from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_invalid_negative_unit_price_rejected():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    r = client.post("/sales", json={
        "customer_name": "BadPrice",
        "line_items": [{"product_id": pid, "qty": 1, "unit_price": -10.0}]
    })
    assert r.status_code in (400, 422)

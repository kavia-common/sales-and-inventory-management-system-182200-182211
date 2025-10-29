from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_requires_customer_name_422():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    resp = client.post("/sales", json={"line_items": [{"product_id": pid, "qty": 1}]})
    assert resp.status_code == 422

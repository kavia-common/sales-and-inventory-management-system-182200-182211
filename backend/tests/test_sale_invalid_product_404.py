from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_invalid_product_returns_404():
    client.post("/seed")
    resp = client.post("/sales", json={
        "customer_name": "Invalid Product",
        "line_items": [{"product_id": 999999, "qty": 1}]
    })
    assert resp.status_code == 404
    assert "Product" in resp.json().get("detail", "")

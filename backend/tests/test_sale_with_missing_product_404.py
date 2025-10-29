from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_creating_sale_with_missing_product_returns_404():
    resp = client.post("/sales", json={
        "customer_name": "Missing Product",
        "line_items": [{"product_id": 99999999, "qty": 1}]
    })
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "").lower()

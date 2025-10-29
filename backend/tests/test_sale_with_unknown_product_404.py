from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_unknown_product_404():
    r = client.post("/sales", json={
        "customer_name": "UnknownProduct",
        "line_items": [{"product_id": 987654321, "qty": 1}]
    })
    assert r.status_code == 404

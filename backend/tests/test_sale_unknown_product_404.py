from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_unknown_product_returns_404():
    r = client.post("/sales", json={"customer_name": "UnknownProd", "line_items": [{"product_id": 99999999, "qty": 1}]})
    assert r.status_code == 404

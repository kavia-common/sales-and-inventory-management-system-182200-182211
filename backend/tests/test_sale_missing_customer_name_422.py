from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_missing_customer_name_returns_422():
    client.post("/seed")
    r = client.post("/sales", json={
        "line_items": []
    })
    assert r.status_code in (400, 422)

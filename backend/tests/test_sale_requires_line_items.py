from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_requires_line_items():
    r = client.post("/sales", json={"customer_name": "NoItems", "line_items": []})
    assert r.status_code == 400

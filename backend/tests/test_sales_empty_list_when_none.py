from fastapi.testclient import TestClient
from src.api.main import app

def test_sales_empty_list_when_none():
    client = TestClient(app)
    resp = client.get("/sales")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

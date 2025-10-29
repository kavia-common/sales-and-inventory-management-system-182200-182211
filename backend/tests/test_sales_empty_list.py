from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sales_list_returns_list_even_when_empty():
    r = client.get("/sales")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

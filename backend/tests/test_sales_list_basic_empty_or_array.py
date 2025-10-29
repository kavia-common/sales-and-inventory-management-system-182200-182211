from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sales_list_returns_array_and_200():
    r = client.get("/sales")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

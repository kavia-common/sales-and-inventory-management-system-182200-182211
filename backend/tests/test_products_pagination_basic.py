from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_pagination_basic():
    client.post("/seed")
    r = client.get("/products/paged?offset=0&limit=2")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) <= 2

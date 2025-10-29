from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_paged_endpoint_limit():
    client.post("/seed")
    r = client.get("/products/paged", params={"limit": 1, "offset": 0})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) <= 1

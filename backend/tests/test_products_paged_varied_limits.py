from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_paged_varied_limits():
    client.post("/seed")
    for limit in (1, 2, 5, 10, 50, 100):
        r = client.get(f"/products/paged?offset=0&limit={limit}")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) <= limit

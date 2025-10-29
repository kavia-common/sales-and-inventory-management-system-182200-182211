from fastapi.testclient import TestClient
from src.api.main import app

def test_products_paged_bounds():
    client = TestClient(app)
    client.post("/seed")
    # Valid bounds
    r = client.get("/products/paged?offset=0&limit=1")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    # Upper bound on limit
    r2 = client.get("/products/paged?offset=0&limit=100")
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)

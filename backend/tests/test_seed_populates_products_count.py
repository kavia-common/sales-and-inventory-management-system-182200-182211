from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_seed_populates_products_and_count_matches_list():
    r = client.post("/seed")
    assert r.status_code in (200, 201), r.text
    count = r.json().get("seeded_products")
    lst = client.get("/products")
    assert lst.status_code == 200
    data = lst.json()
    assert isinstance(data, list)
    assert len(data) >= count

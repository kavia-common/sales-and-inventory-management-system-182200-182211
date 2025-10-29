from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_list_empty_schema():
    r = client.get("/products")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

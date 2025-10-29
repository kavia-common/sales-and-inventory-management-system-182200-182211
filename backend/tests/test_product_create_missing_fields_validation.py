from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_create_missing_required_fields_rejected():
    r = client.post("/products", json={"name": "MissingSKUOnly"})
    assert r.status_code in (400, 422)

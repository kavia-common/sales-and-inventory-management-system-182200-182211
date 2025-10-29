from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_missing_required_fields_returns_422():
    # Completely missing required fields
    r = client.post("/sales", json={})
    assert r.status_code in (400, 422)

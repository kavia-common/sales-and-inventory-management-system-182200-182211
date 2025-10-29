from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_contract():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("application/json")
    assert r.json() == {"status": "OK"}

from fastapi.testclient import TestClient
from src.api.main import app

def test_root():
    client = TestClient(app)
    r = client.get("/")
    # The root endpoint returns {"message":"Healthy"}
    assert r.status_code == 200
    assert r.json().get("message") == "Healthy"

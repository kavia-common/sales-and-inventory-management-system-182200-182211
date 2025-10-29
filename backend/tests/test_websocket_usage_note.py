from fastapi.testclient import TestClient
from src.api.main import app

def test_websocket_usage_note():
    client = TestClient(app)
    r = client.get("/docs/websocket-usage")
    assert r.status_code == 200
    data = r.json()
    assert data.get("note") == "No WebSocket endpoints in this project."

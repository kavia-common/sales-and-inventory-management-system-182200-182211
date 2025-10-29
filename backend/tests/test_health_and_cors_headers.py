from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_contains_status_ok_and_cors_headers_present():
    r = client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, dict) and body.get("status") == "OK"
    # CORS preflight/headers (FastAPI/Starlette return CORS on actual requests too when configured)
    assert "access-control-allow-origin" in {k.lower(): v for k, v in r.headers.items()}

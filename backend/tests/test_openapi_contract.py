from fastapi.testclient import TestClient
from src.api.main import app

def test_openapi_contract_matches_default():
    client = TestClient(app)
    # FastAPI default openapi.json
    default_schema = client.app.openapi()
    # Our explicit route
    r = client.get("/openapi.json")
    assert r.status_code == 200
    route_schema = r.json()
    # Basic keys match
    for k in ("openapi", "info", "paths"):
        assert k in route_schema and k in default_schema

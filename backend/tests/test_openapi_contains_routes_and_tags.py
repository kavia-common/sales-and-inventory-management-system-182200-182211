from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_openapi_has_core_routes_and_tags():
    r = client.get("/openapi.json")
    assert r.status_code == 200
    spec = r.json()
    tags = {t["name"] for t in spec.get("tags", [])}
    assert {"products", "inventory", "sales", "invoices"}.issubset(tags)
    paths = spec.get("paths", {})
    # check health and at least one route per resource exists
    assert "/health" in paths
    assert any(p.startswith("/products") for p in paths)
    assert any(p.startswith("/inventory") for p in paths)
    assert any(p.startswith("/sales") for p in paths)
    assert any(p.startswith("/invoices") for p in paths)

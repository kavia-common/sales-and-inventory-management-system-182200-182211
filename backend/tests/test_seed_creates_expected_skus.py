from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_seed_creates_expected_skus():
    client.post("/seed")
    r = client.get("/products")
    assert r.status_code == 200
    data = r.json()
    skus = {p["sku"] for p in data}
    # At least one of the known seed SKUs should exist
    assert {"SKU-001", "SKU-002", "SKU-003"} & skus

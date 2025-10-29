from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_seed_idempotent_no_duplicate_skus():
    r1 = client.post("/seed")
    assert r1.status_code in (200, 201), r1.text
    r2 = client.post("/seed")
    assert r2.status_code in (200, 201), r2.text
    products = client.get("/products").json()
    skus = [p["sku"] for p in products]
    assert len(skus) == len(set(skus)), "Seed should not create duplicate SKUs"

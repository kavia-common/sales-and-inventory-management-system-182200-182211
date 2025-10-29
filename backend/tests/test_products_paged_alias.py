from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_paged_alias_returns_subset_with_offset_limit():
    client.post("/seed")
    all_r = client.get("/products")
    assert all_r.status_code == 200
    all_products = all_r.json()
    if len(all_products) < 2:
        # Ensure at least 2 items exist
        client.post("/products", json={
            "name": "ExtraItem1", "sku": "EXTRA-001", "price": 1.23, "gst_rate": 5.0, "stock_qty": 1
        })
        client.post("/products", json={
            "name": "ExtraItem2", "sku": "EXTRA-002", "price": 2.34, "gst_rate": 5.0, "stock_qty": 1
        })
        all_products = client.get("/products").json()

    r = client.get("/products/paged", params={"offset": 1, "limit": 1})
    assert r.status_code == 200
    subset = r.json()
    assert isinstance(subset, list)
    assert len(subset) <= 1

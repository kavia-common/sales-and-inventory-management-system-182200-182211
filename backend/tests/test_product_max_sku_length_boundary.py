from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_max_sku_length_boundary():
    # Assuming SKU column allows 100 chars per models (String(100))
    max_len_sku = "S" * 100
    r = client.post("/products", json={
        "name": "MaxSKU",
        "sku": max_len_sku,
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    # Depending on DB and ORM, this should succeed
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]
    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    assert g.json()["sku"] == max_len_sku

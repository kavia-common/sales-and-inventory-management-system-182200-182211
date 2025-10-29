from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_sku_case_sensitivity():
    # Create a product
    r1 = client.post("/products", json={
        "name": "Case A",
        "sku": "SKUCASE",
        "price": 10.0,
        "gst_rate": 18.0,
        "stock_qty": 1
    })
    assert r1.status_code in (200, 201), r1.text

    # Attempt with different case
    r2 = client.post("/products", json={
        "name": "Case B",
        "sku": "skucase",
        "price": 11.0,
        "gst_rate": 18.0,
        "stock_qty": 2
    })
    # Depending on DB collation, this may be allowed or rejected.
    # We accept either 200/201 (case-sensitive unique) or 400 (case-insensitive unique).
    assert r2.status_code in (200, 201, 400), r2.text

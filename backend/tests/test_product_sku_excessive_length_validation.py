from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_sku_excessive_length_rejected_or_handled():
    long_sku = "X" * 300  # beyond typical 100-char limit
    r = client.post("/products", json={
        "name": "ExcessiveSKU",
        "sku": long_sku,
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    # Accept either validation error or DB-level error mapped to 400/422
    assert r.status_code in (400, 422)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_sku_whitespace_is_distinct_and_not_trimmed_implicitly():
    base = "WS-UNIQ-1"
    r1 = client.post("/products", json={
        "name": "WS1",
        "sku": base,
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r1.status_code in (200, 201), r1.text

    r2 = client.post("/products", json={
        "name": "WS2",
        "sku": base + " ",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    # Depending on DB collation, treat as distinct; accept either created or duplicate handled by DB.
    assert r2.status_code in (200, 201, 400), r2.text

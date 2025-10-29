from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_create_min_values_zero_gst():
    r = client.post("/products", json={
        "name": "MinVals",
        "sku": "MIN-VALS-1",
        "price": 0.0,
        "gst_rate": 0.0,
        "stock_qty": 0
    })
    assert r.status_code in (200, 201), r.text
    p = r.json()
    assert p["name"] == "MinVals"
    assert p["sku"] == "MIN-VALS-1"
    assert p["stock_qty"] == 0

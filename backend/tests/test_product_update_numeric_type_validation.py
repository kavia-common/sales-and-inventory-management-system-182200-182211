from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_rejects_invalid_numeric_types():
    r = client.post("/products", json={
        "name": "NumType",
        "sku": "NUM-TYPE-1",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Invalid string types for numeric fields
    up = client.put(f"/products/{pid}", json={"price": "abc", "gst_rate": "xyz"})
    assert up.status_code in (400, 422)

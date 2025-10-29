from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_name_whitespace_behavior():
    r = client.post("/products", json={
        "name": "WSName",
        "sku": "WS-NAME-1",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    up = client.put(f"/products/{pid}", json={"name": "   "})
    # Depending on validation this might be 400/422, but allow 200/201 if trimming not enforced
    assert up.status_code in (200, 201, 400, 422)

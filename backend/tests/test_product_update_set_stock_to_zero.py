from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_set_stock_to_zero():
    p = client.post("/products", json={
        "name": "ZeroUpdate",
        "sku": "ZERO-UPD-1",
        "price": 2.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }).json()
    r = client.put(f"/products/{p['id']}", json={"stock_qty": 0})
    assert r.status_code == 200, r.text
    updated = r.json()
    assert int(updated["stock_qty"]) == 0

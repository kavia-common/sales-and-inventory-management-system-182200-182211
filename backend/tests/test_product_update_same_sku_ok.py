from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_update_with_same_sku_is_allowed():
    # Create product
    r = client.post("/products", json={
        "name": "SameSKU",
        "sku": "SAME-SKU-1",
        "price": 9.99,
        "gst_rate": 18.0,
        "stock_qty": 2
    })
    assert r.status_code in (200, 201), r.text
    prod = r.json()

    # Update name only, keep SKU the same
    upd = client.put(f"/products/{prod['id']}", json={"name": "SameSKU-Updated", "sku": "SAME-SKU-1"})
    assert upd.status_code == 200, upd.text
    data = upd.json()
    assert data["sku"] == "SAME-SKU-1"
    assert data["name"] == "SameSKU-Updated"

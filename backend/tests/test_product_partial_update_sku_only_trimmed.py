from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_partial_update_sku_only_trimmed():
    p = client.post("/products", json={
        "name": "SkuOnly",
        "sku": "SKU-ONLY-1",
        "price": 9.00,
        "gst_rate": 5.00,
        "stock_qty": 2
    }).json()
    r = client.put(f"/products/{p['id']}", json={"sku": "  SKU-ONLY-1  "})
    assert r.status_code == 200, r.text
    updated = r.json()
    assert updated["sku"] == "SKU-ONLY-1"
    assert updated["name"] == p["name"]
    assert str(updated["price"]) == str(p["price"])
    assert str(updated["gst_rate"]) == str(p["gst_rate"])
    assert int(updated["stock_qty"]) == int(p["stock_qty"])

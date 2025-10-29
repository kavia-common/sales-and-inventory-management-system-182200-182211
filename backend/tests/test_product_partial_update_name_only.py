from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_partial_update_name_only():
    p = client.post("/products", json={
        "name": "OldName",
        "sku": "PART-UPD-1",
        "price": 8.00,
        "gst_rate": 5.00,
        "stock_qty": 4
    }).json()

    r = client.put(f"/products/{p['id']}", json={"name": "NewName"})
    assert r.status_code == 200, r.text
    updated = r.json()
    assert updated["name"] == "NewName"
    assert updated["sku"] == p["sku"]
    assert str(updated["price"]) == str(p["price"])
    assert str(updated["gst_rate"]) == str(p["gst_rate"])
    assert int(updated["stock_qty"]) == int(p["stock_qty"])

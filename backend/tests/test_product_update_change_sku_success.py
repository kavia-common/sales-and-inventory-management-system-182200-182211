from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_update_product_sku_to_new_unique_value_succeeds():
    # Create product A
    r = client.post("/products", json={
        "name": "SkuChangeA",
        "sku": "SKU-CHANGE-A",
        "price": 5.0,
        "gst_rate": 5.0,
        "stock_qty": 2
    })
    assert r.status_code in (200, 201), r.text
    a = r.json()

    # Create product B
    r2 = client.post("/products", json={
        "name": "SkuChangeB",
        "sku": "SKU-CHANGE-B",
        "price": 6.0,
        "gst_rate": 12.0,
        "stock_qty": 3
    })
    assert r2.status_code in (200, 201), r2.text
    b = r2.json()

    # Update A's SKU to a new unique value
    upd = client.put(f"/products/{a['id']}", json={"sku": "SKU-CHANGE-A-NEW"})
    assert upd.status_code == 200, upd.text
    data = upd.json()
    assert data["sku"] == "SKU-CHANGE-A-NEW"

    # Ensure B remains unchanged
    got_b = client.get(f"/products/{b['id']}")
    assert got_b.status_code == 200
    assert got_b.json()["sku"] == "SKU-CHANGE-B"

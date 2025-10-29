from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_sku_uniqueness():
    # Create two products
    p1 = client.post("/products", json={
        "name": "P1",
        "sku": "UPD-UNIQ-1",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }).json()
    p2 = client.post("/products", json={
        "name": "P2",
        "sku": "UPD-UNIQ-2",
        "price": 15.0,
        "gst_rate": 5.0,
        "stock_qty": 10
    }).json()

    # Attempt to update p2 sku to p1's sku should fail
    r = client.put(f"/products/{p2['id']}", json={"sku": p1["sku"]})
    assert r.status_code in (400, 409)

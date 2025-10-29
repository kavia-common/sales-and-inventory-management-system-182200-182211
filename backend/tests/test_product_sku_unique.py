from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_sku_unique_on_create_and_update():
    # Create first product
    r1 = client.post("/products", json={
        "name": "P1",
        "sku": "SKU-UNIQ",
        "price": 10.0,
        "gst_rate": 18.0,
        "stock_qty": 1
    })
    assert r1.status_code in (200, 201), r1.text
    r1.json()

    # Create second with same SKU should fail
    r2 = client.post("/products", json={
        "name": "P2",
        "sku": "SKU-UNIQ",
        "price": 5.0,
        "gst_rate": 5.0,
        "stock_qty": 2
    })
    assert r2.status_code == 400

    # Create second with different SKU
    r3 = client.post("/products", json={
        "name": "P3",
        "sku": "SKU-UNIQ-2",
        "price": 8.0,
        "gst_rate": 12.0,
        "stock_qty": 3
    })
    assert r3.status_code in (200, 201), r3.text
    p3 = r3.json()

    # Update second to duplicate SKU should fail
    upd = client.put(f"/products/{p3['id']}", json={"sku": "SKU-UNIQ"})
    assert upd.status_code == 400

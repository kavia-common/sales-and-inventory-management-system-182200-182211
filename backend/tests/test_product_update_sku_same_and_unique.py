from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_update_sku_same_value_ok_and_unique_value_ok():
    # Create two products
    p1 = client.post("/products", json={
        "name": "SKUUpdate1", "sku": "UPD-SKU-1", "price": 10.0, "gst_rate": 5.0, "stock_qty": 1
    }).json()
    p2 = client.post("/products", json={
        "name": "SKUUpdate2", "sku": "UPD-SKU-2", "price": 11.0, "gst_rate": 5.0, "stock_qty": 1
    }).json()

    # Update p1 with same SKU value (should be OK)
    same = client.put(f"/products/{p1['id']}", json={"sku": "UPD-SKU-1"})
    assert same.status_code == 200, same.text
    assert same.json()["sku"] == "UPD-SKU-1"

    # Update p1 with a unique new SKU (should be OK)
    new = client.put(f"/products/{p1['id']}", json={"sku": "UPD-SKU-3"})
    assert new.status_code == 200, new.text
    assert new.json()["sku"] == "UPD-SKU-3"

    # Attempt to set to an existing SKU (from p2) should fail
    dup = client.put(f"/products/{p1['id']}", json={"sku": "UPD-SKU-2"})
    assert dup.status_code == 400

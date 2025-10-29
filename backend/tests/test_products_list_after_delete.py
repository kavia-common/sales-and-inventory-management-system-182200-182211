from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_list_does_not_include_deleted_item():
    # Create a product
    resp = client.post("/products", json={
        "name": "Temp",
        "sku": "TEMP-DELETE",
        "price": 1.23,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert resp.status_code in (200, 201), resp.text
    pid = resp.json()["id"]

    # Ensure it is in the list
    lst = client.get("/products").json()
    assert any(p["id"] == pid for p in lst)

    # Delete it
    del_resp = client.delete(f"/products/{pid}")
    assert del_resp.status_code == 204

    # Verify it no longer appears
    lst2 = client.get("/products").json()
    assert all(p["id"] != pid for p in lst2)

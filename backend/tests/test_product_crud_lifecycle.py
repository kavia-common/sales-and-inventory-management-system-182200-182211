from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_crud_lifecycle():
    # Create
    r = client.post("/products", json={
        "name": "Lifecycle Item",
        "sku": "LC-001",
        "price": 25.50,
        "gst_rate": 18.0,
        "stock_qty": 10
    })
    assert r.status_code in (200, 201), r.text
    prod = r.json()
    pid = prod["id"]

    # Read
    get_r = client.get(f"/products/{pid}")
    assert get_r.status_code == 200
    assert get_r.json()["sku"] == "LC-001"

    # Update name and price
    up = client.put(f"/products/{pid}", json={"name": "Lifecycle Item Updated", "price": 30.75})
    assert up.status_code == 200
    body = up.json()
    assert body["name"] == "Lifecycle Item Updated"
    assert float(body["price"]) == 30.75

    # Enforce SKU uniqueness
    r2 = client.post("/products", json={
        "name": "Other",
        "sku": "LC-002",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 3
    })
    assert r2.status_code in (200, 201), r2.text
    dup_attempt = client.put(f"/products/{pid}", json={"sku": "LC-002"})
    assert dup_attempt.status_code == 400

    # Delete
    del_r = client.delete(f"/products/{pid}")
    assert del_r.status_code in (200, 204), del_r.text

    # Verify 404 after delete
    get_missing = client.get(f"/products/{pid}")
    assert get_missing.status_code == 404

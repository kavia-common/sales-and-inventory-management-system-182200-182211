from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update():
    # Create product
    resp = client.post("/products", json={
        "name": "Updatable",
        "sku": "UPD-1",
        "price": 10.00,
        "gst_rate": 18.0,
        "stock_qty": 5
    })
    assert resp.status_code in (200, 201), resp.text
    pid = resp.json()["id"]

    # Update product fields
    upd = client.put(f"/products/{pid}", json={
        "name": "Updated Name",
        "price": 12.50,
        "gst_rate": 12.0,
        "stock_qty": 7
    })
    assert upd.status_code == 200
    data = upd.json()
    assert data["name"] == "Updated Name"
    assert float(data["price"]) == 12.50
    assert float(data["gst_rate"]) == 12.0
    assert data["stock_qty"] == 7

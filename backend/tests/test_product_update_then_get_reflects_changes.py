from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_then_get_reflects_changes():
    # Create product
    r = client.post("/products", json={
        "name": "UpdThenGet",
        "sku": "UPD-GET-1",
        "price": 9.99,
        "gst_rate": 5.0,
        "stock_qty": 2
    })
    assert r.status_code in (200, 201), r.text
    p = r.json()
    pid = p["id"]

    # Update name and price
    up = client.put(f"/products/{pid}", json={"name": "UpdThenGetNew", "price": 12.50})
    assert up.status_code in (200, 201), up.text

    # Get and verify
    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    data = g.json()
    assert data["name"] == "UpdThenGetNew"
    assert float(data["price"]) == 12.50
    assert data["sku"] == p["sku"]
    assert data["stock_qty"] == p["stock_qty"]

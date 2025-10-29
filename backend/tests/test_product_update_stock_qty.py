from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_updating_product_stock_qty_via_put_persists():
    # Create product
    r = client.post("/products", json={
        "name": "StockUpdater",
        "sku": "STK-UPD-1",
        "price": 19.99,
        "gst_rate": 12.0,
        "stock_qty": 10
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Update stock
    up = client.put(f"/products/{pid}", json={"stock_qty": 42})
    assert up.status_code == 200, up.text
    assert int(up.json()["stock_qty"]) == 42

    # Fetch and verify
    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    assert int(g.json()["stock_qty"]) == 42

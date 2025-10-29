from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_stock_after_multiple_inventory_movements():
    # Create product with base stock
    pr = client.post("/products", json={
        "name": "MultiMvProd",
        "sku": "MULTI-MV-1",
        "price": 5.0,
        "gst_rate": 5.0,
        "stock_qty": 10
    })
    assert pr.status_code in (200, 201), pr.text
    p = pr.json()
    pid = p["id"]
    start = p["stock_qty"]

    # +5, -2, +7 => net +10
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": 5, "reason": "Batch A"})
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": -2, "reason": "Adjustment"})
    client.post("/inventory/movements", json={"product_id": pid, "change_qty": 7, "reason": "Batch B"})

    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    assert g.json()["stock_qty"] == start + 10

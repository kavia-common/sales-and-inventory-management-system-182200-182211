from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_delete_product_after_movements_without_sales_succeeds():
    # Create product
    r = client.post("/products", json={
        "name": "MovDel",
        "sku": "MOV-DEL-1",
        "price": 9.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    prod = r.json()
    pid = prod["id"]

    # Add a movement
    mv = client.post("/inventory/movements", json={
        "product_id": pid,
        "change_qty": 1,
        "reason": "Prep for delete"
    })
    assert mv.status_code in (200, 201), mv.text

    # Delete product - should succeed as there are no sales referencing it
    d = client.delete(f"/products/{pid}")
    assert d.status_code == 204

    # Confirm 404 on subsequent get
    g = client.get(f"/products/{pid}")
    assert g.status_code == 404

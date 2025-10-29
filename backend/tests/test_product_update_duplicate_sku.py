from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_update_to_duplicate_sku_is_rejected():
    # Create two products with different SKUs
    p1 = client.post("/products", json={
        "name": "DupA",
        "sku": "DUP-A",
        "price": 11.0,
        "gst_rate": 18.0,
        "stock_qty": 5
    }).json()

    p2 = client.post("/products", json={
        "name": "DupB",
        "sku": "DUP-B",
        "price": 12.0,
        "gst_rate": 12.0,
        "stock_qty": 6
    }).json()

    # Try updating p2 SKU to p1 SKU -> should fail
    upd = client.put(f"/products/{p2['id']}", json={"sku": p1["sku"]})
    assert upd.status_code == 400
    assert "SKU already exists" in upd.json().get("detail", "")

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_delete_not_found_then_delete_ok():
    r_missing = client.delete("/products/99999999")
    assert r_missing.status_code == 404

    # Create a product and then delete it
    created = client.post("/products", json={
        "name": "DelMe",
        "sku": "DEL-001",
        "price": 3.50,
        "gst_rate": 5.0,
        "stock_qty": 1
    }).json()
    r_del = client.delete(f"/products/{created['id']}")
    assert r_del.status_code in (200, 204)

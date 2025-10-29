from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_delete_then_404_on_get():
    # Create product
    r = client.post("/products", json={
        "name": "DeleteMe",
        "sku": "DEL-001",
        "price": 12.34,
        "gst_rate": 5.0,
        "stock_qty": 10
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Delete
    d = client.delete(f"/products/{pid}")
    assert d.status_code in (200, 204), d.text

    # Fetch should 404
    g = client.get(f"/products/{pid}")
    assert g.status_code == 404

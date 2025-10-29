from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_crud_flow():
    # Create product
    resp = client.post("/products", json={
        "name": "Test Product",
        "sku": "TEST-SKU-1",
        "price": 123.45,
        "gst_rate": 18.0,
        "stock_qty": 10
    })
    assert resp.status_code in (200, 201), resp.text
    data = resp.json()
    product_id = data["id"]

    # List products
    resp = client.get("/products")
    assert resp.status_code == 200
    items = resp.json()
    assert any(p["id"] == product_id for p in items)

    # Get paged
    resp = client.get("/products/paged?offset=0&limit=5")
    assert resp.status_code == 200

    # Delete product
    resp = client.delete(f"/products/{product_id}")
    assert resp.status_code == 204

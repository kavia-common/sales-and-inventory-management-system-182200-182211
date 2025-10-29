from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_delete_then_get_404():
    # Create product
    resp = client.post("/products", json={
        "name": "Deletable",
        "sku": "DEL-1",
        "price": 5.00,
        "gst_rate": 18.0,
        "stock_qty": 2
    })
    assert resp.status_code in (200, 201), resp.text
    pid = resp.json()["id"]

    # Delete
    del_resp = client.delete(f"/products/{pid}")
    assert del_resp.status_code == 204

    # Verify 404 on get
    get_resp = client.get(f"/products/{pid}")
    assert get_resp.status_code == 404

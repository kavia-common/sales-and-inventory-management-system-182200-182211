from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_delete_returns_204_no_body():
    # Create
    r = client.post("/products", json={
        "name": "NoBody",
        "sku": "NOBODY-1",
        "price": 3.21,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Delete
    d = client.delete(f"/products/{pid}")
    assert d.status_code == 204
    # The response body should be empty for 204
    assert d.content in (b"", None)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_get_after_delete_404():
    created = client.post("/products", json={
        "name": "Gone",
        "sku": "DEL-GONE-1",
        "price": 4.25,
        "gst_rate": 5.0,
        "stock_qty": 1
    }).json()
    pid = created["id"]
    del_resp = client.delete(f"/products/{pid}")
    assert del_resp.status_code in (200, 204)
    r = client.get(f"/products/{pid}")
    assert r.status_code == 404

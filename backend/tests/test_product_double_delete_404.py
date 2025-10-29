from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_double_delete_second_returns_404():
    r = client.post("/products", json={
        "name": "DoubleDelete",
        "sku": "DD-1",
        "price": 1.11,
        "gst_rate": 5.0,
        "stock_qty": 1
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    d1 = client.delete(f"/products/{pid}")
    assert d1.status_code == 204

    d2 = client.delete(f"/products/{pid}")
    assert d2.status_code == 404

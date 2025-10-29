from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_get_returns_full_schema():
    r = client.post("/products", json={
        "name": "SchemaFields",
        "sku": "SCH-FLD-1",
        "price": 7.89,
        "gst_rate": 12.0,
        "stock_qty": 4
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    g = client.get(f"/products/{pid}")
    assert g.status_code == 200
    p = g.json()
    assert "name" in p and "sku" in p and "price" in p and "gst_rate" in p and "stock_qty" in p

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_get_schema_fields_types():
    created = client.post("/products", json={
        "name": "SchemaTypes",
        "sku": "SCHEMA-T-1",
        "price": 9.99,
        "gst_rate": 18.00,
        "stock_qty": 7
    }).json()
    pid = created["id"]
    r = client.get(f"/products/{pid}")
    assert r.status_code == 200
    p = r.json()
    assert isinstance(p["id"], int)
    assert isinstance(p["name"], str)
    assert isinstance(p["sku"], str)
    assert "price" in p and "gst_rate" in p and "stock_qty" in p

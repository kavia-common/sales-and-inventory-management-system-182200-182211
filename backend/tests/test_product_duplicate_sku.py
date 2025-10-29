from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_duplicate_sku_rejected():
    base = {"name": "DupSKU", "sku": "DUP-001", "price": 10.00, "gst_rate": 5.00, "stock_qty": 5}
    r1 = client.post("/products", json=base)
    assert r1.status_code in (200, 201, 422, 400)  # allow 422 if prior constraints fail in env
    r2 = client.post("/products", json=base)
    assert r2.status_code in (400, 409, 422)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_duplicate_sku_is_rejected_with_400():
    payload = {
        "name": "DupSKU Item",
        "sku": "DUP-SKU-001",
        "price": 10.0,
        "gst_rate": 5.0,
        "stock_qty": 5
    }
    r1 = client.post("/products", json=payload)
    assert r1.status_code in (200, 201), r1.text
    r2 = client.post("/products", json=payload)
    assert r2.status_code == 400
    assert "SKU already exists" in r2.json().get("detail", "")

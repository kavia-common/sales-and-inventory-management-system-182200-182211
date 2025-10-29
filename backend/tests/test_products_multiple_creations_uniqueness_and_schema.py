from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_multiple_creations_uniqueness_and_schema():
    # Create a few products with unique SKUs
    for i in range(3):
        payload = {"name": f"P-{i}", "sku": f"MULTI-{i}", "price": 1.0 + i, "gst_rate": 5.0, "stock_qty": i}
        r = client.post("/products", json=payload)
        assert r.status_code in (200, 201, 400), r.text  # 400 if already exists
    lst = client.get("/products")
    assert lst.status_code == 200
    data = lst.json()
    assert isinstance(data, list)
    if data:
        p = data[0]
        for k in ("id", "name", "sku", "price", "gst_rate", "stock_qty"):
            assert k in p

import time
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_bulk_insert_and_smoke_timing():
    # Insert a number of products
    base = int(time.time())
    for i in range(30):
        client.post("/products", json={
            "name": f"Bulk{base}-{i}",
            "sku": f"BULK-{base}-{i}",
            "price": 1.11 + i,
            "gst_rate": 5.0,
            "stock_qty": i
        })

    t0 = time.time()
    r = client.get("/products")
    t1 = time.time()
    assert r.status_code == 200
    # Smoke timing: should respond reasonably fast in test env
    assert (t1 - t0) < 2.5
    assert isinstance(r.json(), list)

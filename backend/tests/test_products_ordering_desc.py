from fastapi.testclient import TestClient
from src.api.main import app
import time

client = TestClient(app)

def test_products_list_is_ordered_by_id_desc():
    # Create two products in sequence
    base = int(time.time())
    p1 = client.post("/products", json={
        "name": f"OrderA-{base}",
        "sku": f"ORD-A-{base}",
        "price": 1.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    }).json()
    p2 = client.post("/products", json={
        "name": f"OrderB-{base}",
        "sku": f"ORD-B-{base}",
        "price": 2.0,
        "gst_rate": 5.0,
        "stock_qty": 1
    }).json()

    r = client.get("/products")
    assert r.status_code == 200, r.text
    lst = r.json()
    if len(lst) >= 2:
        assert lst[0]["id"] >= lst[1]["id"]

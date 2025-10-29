from fastapi.testclient import TestClient
from src.api.main import app
import time

client = TestClient(app)

def test_products_created_have_unique_ids_and_skus_and_are_retrievable():
    base = int(time.time())
    p1 = client.post("/products", json={
        "name": f"UniqueA-{base}",
        "sku": f"UNIQ-A-{base}",
        "price": 10.1,
        "gst_rate": 5.0,
        "stock_qty": 2
    }).json()
    p2 = client.post("/products", json={
        "name": f"UniqueB-{base}",
        "sku": f"UNIQ-B-{base}",
        "price": 11.2,
        "gst_rate": 5.0,
        "stock_qty": 3
    }).json()

    assert p1["id"] != p2["id"]
    assert p1["sku"] != p2["sku"]

    g1 = client.get(f"/products/{p1['id']}")
    g2 = client.get(f"/products/{p2['id']}")
    assert g1.status_code == 200 and g2.status_code == 200
    assert g1.json()["sku"] == p1["sku"]
    assert g2.json()["sku"] == p2["sku"]

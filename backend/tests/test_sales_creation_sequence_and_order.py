from fastapi.testclient import TestClient
from src.api.main import app
import time

client = TestClient(app)

def test_sales_creation_sequence_and_order_desc():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    ids = []
    for i in range(3):
        r = client.post("/sales", json={"customer_name": f"Seq-{i}", "line_items": [{"product_id": pid, "qty": 1}]})
        assert r.status_code in (200, 201), r.text
        ids.append(r.json()["id"])
        time.sleep(0.01)
    lst = client.get("/sales")
    assert lst.status_code == 200
    listed_ids = [s["id"] for s in lst.json()]
    assert listed_ids == sorted(listed_ids, reverse=True)

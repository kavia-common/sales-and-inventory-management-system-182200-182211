from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_near_zero_gst_rate_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    near_zero_gst = 0.01
    resp = client.post("/sales", json={
        "customer_name": "NearZeroGST",
        "line_items": [{"product_id": pid, "qty": 2, "gst_rate": near_zero_gst}]
    })
    # Accept either rejection by validation or acceptance with minimal GST
    assert resp.status_code in (200, 201, 400, 422)
    if resp.status_code in (200, 201):
        sale = resp.json()
        li = sale["line_items"][0]
        assert Decimal(str(li["gst_rate"])) == Decimal("0.01")

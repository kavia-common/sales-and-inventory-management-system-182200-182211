from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_gst_rate_rounds_half_up_to_two_decimals():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    qty = 2
    gst_rate_raw = 7.5555  # should round to 7.56
    resp = client.post("/sales", json={
        "customer_name": "GSTRound",
        "line_items": [{"product_id": pid, "qty": qty, "gst_rate": gst_rate_raw}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    li = sale["line_items"][0]

    assert Decimal(str(li["gst_rate"])) == Decimal("7.56")

from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_line_total_equals_subtotal_plus_gst():
    p = client.post("/products", json={
        "name": "LineArithmetic",
        "sku": "LINE-ARITH-1",
        "price": 9.99,
        "gst_rate": 18.0,
        "stock_qty": 10
    }).json()
    r = client.post("/sales", json={
        "customer_name": "LineArithmetic",
        "line_items": [{"product_id": p["id"], "qty": 2}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    li = sale["line_items"][0]
    sub = Decimal(str(li["line_subtotal"]))
    gst = Decimal(str(li["line_gst"]))
    tot = Decimal(str(li["line_total"]))
    assert tot == sub + gst

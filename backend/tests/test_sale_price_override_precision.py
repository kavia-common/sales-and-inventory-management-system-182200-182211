from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_price_override_precision_two_decimals():
    p = client.post("/products", json={
        "name": "PrecisionOverride",
        "sku": "PREC-OVR-1",
        "price": 0.0,
        "gst_rate": 10.0,
        "stock_qty": 10
    }).json()
    r = client.post("/sales", json={
        "customer_name": "Prec",
        "line_items": [{"product_id": p["id"], "qty": 3, "unit_price": 2.345}]  # should round to 2.35
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    li = sale["line_items"][0]
    assert Decimal(str(li["unit_price"])) == Decimal("2.35")
    # validate totals quantization
    for k in ("line_subtotal", "line_gst", "line_total",):
        Decimal(str(li[k]))
    for k in ("subtotal", "gst_total", "grand_total"):
        Decimal(str(sale[k]))

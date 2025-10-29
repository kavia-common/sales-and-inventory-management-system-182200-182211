from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_zero_gst_and_override_price_preserve_two_decimal_precision():
    # Create two products
    p1 = client.post("/products", json={"name":"ZeroGSTItem","sku":"ZG-PR-1","price":5.0,"gst_rate":0.0,"stock_qty":10}).json()
    p2 = client.post("/products", json={"name":"OverrideItem","sku":"ZG-PR-2","price":1.0,"gst_rate":5.0,"stock_qty":10}).json()

    r = client.post("/sales", json={
        "customer_name": "ZeroAndOverride",
        "line_items": [
            {"product_id": p1["id"], "qty": 2, "gst_rate": 0.0},
            {"product_id": p2["id"], "qty": 3, "unit_price": 1.005}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    for li in sale["line_items"]:
        for k in ("unit_price", "gst_rate", "line_subtotal", "line_gst", "line_total"):
            v = Decimal(str(li[k]))
            assert v == v.quantize(Decimal("0.01"))
    for k in ("subtotal", "gst_total", "grand_total"):
        v = Decimal(str(sale[k]))
        assert v == v.quantize(Decimal("0.01"))

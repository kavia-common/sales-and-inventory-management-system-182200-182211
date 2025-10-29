from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_multi_line_price_precision_two_decimals_each_line():
    p1 = client.post("/products", json={"name":"Prec1","sku":"PREC-ML-1","price":0,"gst_rate":5.0,"stock_qty":10}).json()
    p2 = client.post("/products", json={"name":"Prec2","sku":"PREC-ML-2","price":0,"gst_rate":12.0,"stock_qty":10}).json()

    r = client.post("/sales", json={
        "customer_name": "PrecisionMulti",
        "line_items": [
            {"product_id": p1["id"], "qty": 2, "unit_price": 1.005, "gst_rate": 3.335},
            {"product_id": p2["id"], "qty": 3, "unit_price": 2.995, "gst_rate": 4.445}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()

    for li in sale["line_items"]:
        for k in ("unit_price", "gst_rate", "line_subtotal", "line_gst", "line_total"):
            v = Decimal(str(li[k]))
            assert v == v.quantize(Decimal("0.01"))

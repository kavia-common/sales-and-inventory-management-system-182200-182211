from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_line_totals_sum_to_header():
    client.post("/seed")
    products = client.get("/products").json()
    if len(products) < 2:
        return
    p1, p2 = products[0], products[1]
    r = client.post("/sales", json={
        "customer_name": "SumCheck",
        "line_items": [
            {"product_id": p1["id"], "qty": 2},
            {"product_id": p2["id"], "qty": 3}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    sub_sum = sum(Decimal(str(li["line_subtotal"])) for li in sale["line_items"])
    gst_sum = sum(Decimal(str(li["line_gst"])) for li in sale["line_items"])
    tot_sum = sum(Decimal(str(li["line_total"])) for li in sale["line_items"])
    assert Decimal(str(sale["subtotal"])) == sub_sum
    assert Decimal(str(sale["gst_total"])) == gst_sum
    assert Decimal(str(sale["grand_total"])) == tot_sum

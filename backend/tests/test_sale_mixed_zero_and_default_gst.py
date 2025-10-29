from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_mixed_zero_gst_and_default_gst_lines():
    # Create two products
    p1 = client.post("/products", json={"name":"ZeroGSTLine","sku":"MIX-ZERO-1","price":10.0,"gst_rate":5.0,"stock_qty":10}).json()
    p2 = client.post("/products", json={"name":"DefaultGSTLine","sku":"MIX-DEF-1","price":20.0,"gst_rate":12.0,"stock_qty":10}).json()

    r = client.post("/sales", json={
        "customer_name": "MixedGST",
        "line_items": [
            {"product_id": p1["id"], "qty": 1, "gst_rate": 0.0},  # zero GST override
            {"product_id": p2["id"], "qty": 1}  # default GST
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    li_zero = next(li for li in sale["line_items"] if li["product_id"] == p1["id"])
    li_def = next(li for li in sale["line_items"] if li["product_id"] == p2["id"])
    assert Decimal(str(li_zero["line_gst"])) == Decimal("0.00")
    # Ensure header total equals sum of lines
    sub_sum = Decimal(str(li_zero["line_subtotal"])) + Decimal(str(li_def["line_subtotal"]))
    gst_sum = Decimal(str(li_zero["line_gst"])) + Decimal(str(li_def["line_gst"]))
    tot_sum = Decimal(str(li_zero["line_total"])) + Decimal(str(li_def["line_total"]))
    from decimal import Decimal as D
    assert D(str(sale["subtotal"])) == sub_sum
    assert D(str(sale["gst_total"])) == gst_sum
    assert D(str(sale["grand_total"])) == tot_sum

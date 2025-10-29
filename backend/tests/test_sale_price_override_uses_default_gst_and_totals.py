from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_price_override_uses_default_gst_and_totals():
    p = client.post("/products", json={
        "name": "OverrideDefaultGST",
        "sku": "OVR-DEF-GST-1",
        "price": 15.00,
        "gst_rate": 18.00,
        "stock_qty": 10
    }).json()

    qty = 4
    unit_price = Decimal("7.50")
    r = client.post("/sales", json={
        "customer_name": "OverrideDefaultGST",
        "line_items": [{"product_id": p["id"], "qty": qty, "unit_price": float(unit_price)}]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    li = sale["line_items"][0]
    sub = unit_price * Decimal(qty)
    gst = (sub * Decimal("18.00") / Decimal("100")).quantize(Decimal("0.01"))
    tot = (sub + gst).quantize(Decimal("0.01"))
    assert Decimal(str(li["line_subtotal"])) == sub
    assert Decimal(str(li["line_gst"])) == gst
    assert Decimal(str(li["line_total"])) == tot
    assert Decimal(str(sale["grand_total"])) == Decimal(str(sale["subtotal"])) + Decimal(str(sale["gst_total"]))

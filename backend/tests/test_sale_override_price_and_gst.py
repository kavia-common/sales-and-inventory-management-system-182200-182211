from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_line_item_overrides_unit_price_and_gst_rate():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    override_price = Decimal("77.77")
    override_gst = Decimal("5.00")
    qty = 3

    resp = client.post("/sales", json={
        "customer_name": "Override Tester",
        "line_items": [{
            "product_id": pid,
            "qty": qty,
            "unit_price": float(override_price),
            "gst_rate": float(override_gst)
        }]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    li = sale["line_items"][0]
    assert Decimal(str(li["unit_price"])) == override_price
    assert Decimal(str(li["gst_rate"])) == override_gst

    expected_subtotal = (override_price * qty).quantize(Decimal("0.01"))
    expected_gst = (expected_subtotal * override_gst / Decimal("100")).quantize(Decimal("0.01"))
    expected_total = (expected_subtotal + expected_gst).quantize(Decimal("0.01"))
    assert Decimal(str(li["line_subtotal"])) == expected_subtotal
    assert Decimal(str(li["line_gst"])) == expected_gst
    assert Decimal(str(li["line_total"])) == expected_total

from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_uses_product_defaults_for_price_and_gst():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    price = Decimal(str(p["price"]))
    gst = Decimal(str(p["gst_rate"]))
    qty = 2

    resp = client.post("/sales", json={
        "customer_name": "Defaults Tester",
        "line_items": [{"product_id": pid, "qty": qty}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    li = sale["line_items"][0]
    assert Decimal(str(li["unit_price"])) == price
    assert Decimal(str(li["gst_rate"])) == gst

    expected_subtotal = (price * qty).quantize(Decimal("0.01"))
    expected_gst = (expected_subtotal * gst / Decimal("100")).quantize(Decimal("0.01"))
    expected_total = (expected_subtotal + expected_gst).quantize(Decimal("0.01"))

    assert Decimal(str(li["line_subtotal"])) == expected_subtotal
    assert Decimal(str(li["line_gst"])) == expected_gst
    assert Decimal(str(li["line_total"])) == expected_total

from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_fractional_cents_rounding_half_up_applied():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    unit_price = Decimal("0.99")
    gst_rate = Decimal("7.5")  # leads to 0.07425 tax per unit before rounding
    qty = 3

    resp = client.post("/sales", json={
        "customer_name": "FracCents",
        "line_items": [{"product_id": pid, "qty": qty, "unit_price": float(unit_price), "gst_rate": float(gst_rate)}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    li = sale["line_items"][0]

    expected_sub = (unit_price * Decimal(qty)).quantize(Decimal("0.01"))
    expected_gst = (expected_sub * gst_rate / Decimal("100")).quantize(Decimal("0.01"))
    expected_total = (expected_sub + expected_gst).quantize(Decimal("0.01"))

    assert Decimal(str(li["line_subtotal"])) == expected_sub
    assert Decimal(str(li["line_gst"])) == expected_gst
    assert Decimal(str(li["line_total"])) == expected_total
    assert Decimal(str(sale["subtotal"])) == expected_sub
    assert Decimal(str(sale["gst_total"])) == expected_gst
    assert Decimal(str(sale["grand_total"])) == expected_total

from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_override_both_unit_price_and_gst_rate():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]

    override_price = Decimal("55.55")
    override_gst = Decimal("7.50")
    qty = 4

    resp = client.post("/sales", json={
        "customer_name": "OverrideBoth",
        "line_items": [{"product_id": pid, "qty": qty, "unit_price": float(override_price), "gst_rate": float(override_gst)}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    li = next((x for x in sale["line_items"] if x["product_id"] == pid), None)
    assert li is not None

    sub = (override_price * Decimal(qty)).quantize(Decimal("0.01"))
    gst = (sub * override_gst / Decimal("100")).quantize(Decimal("0.01"))
    total = (sub + gst).quantize(Decimal("0.01"))

    from decimal import Decimal as D
    assert D(str(li["unit_price"])) == override_price
    assert D(str(li["gst_rate"])) == override_gst
    assert D(str(li["line_subtotal"])) == sub
    assert D(str(li["line_gst"])) == gst
    assert D(str(li["line_total"])) == total

from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_respects_overridden_gst_rate():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    price = Decimal(str(p["price"]))

    overridden_gst = Decimal("5.0")
    qty = 3

    resp = client.post("/sales", json={
        "customer_name": "OverrideGST",
        "line_items": [{"product_id": pid, "qty": qty, "gst_rate": float(overridden_gst)}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    li = next((x for x in sale["line_items"] if x["product_id"] == pid), None)
    assert li is not None
    assert Decimal(str(li["gst_rate"])) == overridden_gst

    expected_sub = (price * Decimal(qty)).quantize(Decimal("0.01"))
    expected_gst = (expected_sub * overridden_gst / Decimal("100")).quantize(Decimal("0.01"))
    expected_total = (expected_sub + expected_gst).quantize(Decimal("0.01"))

    assert Decimal(str(li["line_subtotal"])) == expected_sub
    assert Decimal(str(li["line_gst"])) == expected_gst
    assert Decimal(str(li["line_total"])) == expected_total

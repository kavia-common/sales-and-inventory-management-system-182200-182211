from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_respects_overridden_unit_price():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    p = products[0]
    pid = p["id"]
    default_price = Decimal(str(p["price"]))
    override = default_price + Decimal("7.25")

    resp = client.post("/sales", json={
        "customer_name": "OverridePrice",
        "line_items": [{"product_id": pid, "qty": 2, "unit_price": float(override)}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    # Find the line item for our product
    li = next((x for x in sale["line_items"] if x["product_id"] == pid), None)
    assert li is not None
    assert Decimal(str(li["unit_price"])) == override

    expected_sub = (override * Decimal("2")).quantize(Decimal("0.01"))
    expected_gst = (expected_sub * Decimal(str(li["gst_rate"])) / Decimal("100")).quantize(Decimal("0.01"))
    expected_total = (expected_sub + expected_gst).quantize(Decimal("0.01"))

    assert Decimal(str(li["line_subtotal"])) == expected_sub
    assert Decimal(str(li["line_gst"])) == expected_gst
    assert Decimal(str(li["line_total"])) == expected_total

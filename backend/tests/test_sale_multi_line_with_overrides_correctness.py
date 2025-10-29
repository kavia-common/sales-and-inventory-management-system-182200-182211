from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_multi_line_with_overrides_totals_and_links():
    client.post("/seed")
    products = client.get("/products").json()
    assert len(products) >= 2
    p1, p2 = products[0], products[1]
    pid1, pid2 = p1["id"], p2["id"]

    override_price = Decimal("23.45")
    override_gst = Decimal("9.50")

    resp = client.post("/sales", json={
        "customer_name": "MixedOverride",
        "line_items": [
            {"product_id": pid1, "qty": 2, "unit_price": float(override_price), "gst_rate": float(override_gst)},
            {"product_id": pid2, "qty": 3}
        ]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    # Validate two line items present
    assert isinstance(sale.get("line_items"), list) and len(sale["line_items"]) == 2
    # Find specific lines by product id
    li1 = next(li for li in sale["line_items"] if li["product_id"] == pid1)
    li2 = next(li for li in sale["line_items"] if li["product_id"] == pid2)

    # Validate overrides reflected
    assert Decimal(str(li1["unit_price"])) == override_price
    assert Decimal(str(li1["gst_rate"])) == override_gst

    # Compute expected totals
    sub1 = (override_price * Decimal("2")).quantize(Decimal("0.01"))
    gst1 = (sub1 * override_gst / Decimal("100")).quantize(Decimal("0.01"))
    tot1 = (sub1 + gst1).quantize(Decimal("0.01"))

    price2 = Decimal(str(p2["price"]))
    gst2_rate = Decimal(str(p2["gst_rate"]))
    sub2 = (price2 * Decimal("3")).quantize(Decimal("0.01"))
    gst2 = (sub2 * gst2_rate / Decimal("100")).quantize(Decimal("0.01"))
    tot2 = (sub2 + gst2).quantize(Decimal("0.01"))

    assert Decimal(str(li1["line_subtotal"])) == sub1
    assert Decimal(str(li1["line_gst"])) == gst1
    assert Decimal(str(li1["line_total"])) == tot1

    assert Decimal(str(li2["line_subtotal"])) == sub2
    assert Decimal(str(li2["line_gst"])) == gst2
    assert Decimal(str(li2["line_total"])) == tot2

    # Validate sale totals
    expected_sub = (sub1 + sub2).quantize(Decimal("0.01"))
    expected_gst = (gst1 + gst2).quantize(Decimal("0.01"))
    expected_total = (expected_sub + expected_gst).quantize(Decimal("0.01"))

    assert Decimal(str(sale["subtotal"])) == expected_sub
    assert Decimal(str(sale["gst_total"])) == expected_gst
    assert Decimal(str(sale["grand_total"])) == expected_total

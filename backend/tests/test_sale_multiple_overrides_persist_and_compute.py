from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_multiple_overrides_persist_and_compute():
    client.post("/seed")
    products = client.get("/products").json()
    assert len(products) >= 2
    p1, p2 = products[0], products[1]
    pid1, pid2 = p1["id"], p2["id"]

    override1_price = Decimal("17.77")
    override1_gst = Decimal("11.11")
    override2_price = Decimal("3.33")
    override2_gst = Decimal("5.55")

    qty1, qty2 = 2, 5

    resp = client.post("/sales", json={
        "customer_name": "MultiOverrides",
        "line_items": [
            {"product_id": pid1, "qty": qty1, "unit_price": float(override1_price), "gst_rate": float(override1_gst)},
            {"product_id": pid2, "qty": qty2, "unit_price": float(override2_price), "gst_rate": float(override2_gst)}
        ]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    li1 = next(li for li in sale["line_items"] if li["product_id"] == pid1)
    li2 = next(li for li in sale["line_items"] if li["product_id"] == pid2)

    assert Decimal(str(li1["unit_price"])) == override1_price
    assert Decimal(str(li1["gst_rate"])) == override1_gst
    assert Decimal(str(li2["unit_price"])) == override2_price
    assert Decimal(str(li2["gst_rate"])) == override2_gst

    sub1 = (override1_price * Decimal(qty1)).quantize(Decimal("0.01"))
    gst1 = (sub1 * override1_gst / Decimal("100")).quantize(Decimal("0.01"))
    tot1 = (sub1 + gst1).quantize(Decimal("0.01"))

    sub2 = (override2_price * Decimal(qty2)).quantize(Decimal("0.01"))
    gst2 = (sub2 * override2_gst / Decimal("100")).quantize(Decimal("0.01"))
    tot2 = (sub2 + gst2).quantize(Decimal("0.01"))

    assert Decimal(str(li1["line_subtotal"])) == sub1
    assert Decimal(str(li1["line_gst"])) == gst1
    assert Decimal(str(li1["line_total"])) == tot1

    assert Decimal(str(li2["line_subtotal"])) == sub2
    assert Decimal(str(li2["line_gst"])) == gst2
    assert Decimal(str(li2["line_total"])) == tot2

    expected_sub = (sub1 + sub2).quantize(Decimal("0.01"))
    expected_gst = (gst1 + gst2).quantize(Decimal("0.01"))
    expected_total = (expected_sub + expected_gst).quantize(Decimal("0.01"))

    assert Decimal(str(sale["subtotal"])) == expected_sub
    assert Decimal(str(sale["gst_total"])) == expected_gst
    assert Decimal(str(sale["grand_total"])) == expected_total

from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_multiple_line_items_totals_and_stock():
    client.post("/seed")
    products = client.get("/products").json()
    assert len(products) >= 2
    p1, p2 = products[0], products[1]
    pid1, pid2 = p1["id"], p2["id"]
    stock1, stock2 = int(p1["stock_qty"]), int(p2["stock_qty"])
    price1, price2 = Decimal(str(p1["price"])), Decimal(str(p2["price"]))
    gst1, gst2 = Decimal(str(p1["gst_rate"])), Decimal(str(p2["gst_rate"]))

    qty1, qty2 = 2, 3

    resp = client.post("/sales", json={
        "customer_name": "Multi Lines",
        "line_items": [
            {"product_id": pid1, "qty": qty1},
            {"product_id": pid2, "qty": qty2},
        ]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    # Expected per-line
    line1_sub = (price1 * qty1).quantize(Decimal("0.01"))
    line1_gst = (line1_sub * gst1 / Decimal("100")).quantize(Decimal("0.01"))
    line1_total = (line1_sub + line1_gst).quantize(Decimal("0.01"))

    line2_sub = (price2 * qty2).quantize(Decimal("0.01"))
    line2_gst = (line2_sub * gst2 / Decimal("100")).quantize(Decimal("0.01"))
    line2_total = (line2_sub + line2_gst).quantize(Decimal("0.01"))

    expected_subtotal = (line1_sub + line2_sub).quantize(Decimal("0.01"))
    expected_gst = (line1_gst + line2_gst).quantize(Decimal("0.01"))
    expected_grand = (expected_subtotal + expected_gst).quantize(Decimal("0.01"))

    assert Decimal(str(sale["subtotal"])) == expected_subtotal
    assert Decimal(str(sale["gst_total"])) == expected_gst
    assert Decimal(str(sale["grand_total"])) == expected_grand

    # Inventory updated
    u1 = client.get(f"/products/{pid1}").json()
    u2 = client.get(f"/products/{pid2}").json()
    assert int(u1["stock_qty"]) == stock1 - qty1
    assert int(u2["stock_qty"]) == stock2 - qty2

from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_precision_with_mixed_overrides_and_defaults():
    client.post("/seed")
    products = client.get("/products").json()
    if len(products) < 2:
        return
    p1, p2 = products[0], products[1]
    # Mixed: override for p1, defaults for p2
    sale_resp = client.post("/sales", json={
        "customer_name": "InvMixedPrec",
        "line_items": [
            {"product_id": p1["id"], "qty": 2, "unit_price": 11.115, "gst_rate": 7.505},
            {"product_id": p2["id"], "qty": 3}
        ]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()
    inv_no = f"INV-MIXED-PREC-{sale['id']}"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv = inv_resp.json()
    # Totals are quantized to 2 decimals
    for key in ("subtotal", "gst_total", "grand_total"):
        v = Decimal(str(inv[key]))
        assert v == v.quantize(Decimal("0.01"))
    # Fetch by ID and compare totals are the same
    got = client.get(f"/invoices/{inv['id']}")
    assert got.status_code == 200
    inv2 = got.json()
    for key in ("subtotal", "gst_total", "grand_total"):
        assert str(inv[key]) == str(inv2[key])

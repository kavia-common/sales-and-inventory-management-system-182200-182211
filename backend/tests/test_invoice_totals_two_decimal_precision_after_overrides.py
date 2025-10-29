from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_totals_quantized_two_decimals_after_overrides():
    # Create product
    p = client.post("/products", json={
        "name": "InvPrecProd",
        "sku": "INV-PREC-1",
        "price": 0.0,
        "gst_rate": 0.0,
        "stock_qty": 10
    }).json()

    # Create sale with high precision overrides
    s = client.post("/sales", json={
        "customer_name": "InvPrec",
        "line_items": [{
            "product_id": p["id"],
            "qty": 3,
            "unit_price": 1.23456,
            "gst_rate": 7.89123
        }]
    })
    assert s.status_code in (200, 201), s.text
    sale = s.json()

    inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-PREC-{sale['id']}"})
    assert inv.status_code in (200, 201), inv.text
    body = inv.json()

    for key in ("subtotal", "gst_total", "grand_total"):
        v = Decimal(str(body[key]))
        assert v == v.quantize(Decimal("0.01"))

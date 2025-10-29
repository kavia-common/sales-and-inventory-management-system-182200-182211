from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_totals_after_overridden_gst_on_sale_line():
    # Create product
    p = client.post("/products", json={
        "name": "OverGST",
        "sku": "OVR-GST-1",
        "price": 10.00,
        "gst_rate": 18.00,
        "stock_qty": 10
    }).json()

    # Create sale overriding GST to 5%
    s = client.post("/sales", json={
        "customer_name": "GSTOverride",
        "line_items": [{"product_id": p["id"], "qty": 2, "gst_rate": 5.0}]
    })
    assert s.status_code in (200, 201), s.text
    sale = s.json()

    inv_no = f"INV-OVR-{sale['id']}"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv = inv_resp.json()

    assert Decimal(str(inv["subtotal"])) == Decimal(str(sale["subtotal"]))
    assert Decimal(str(inv["gst_total"])) == Decimal(str(sale["gst_total"]))
    assert Decimal(str(inv["grand_total"])) == Decimal(str(sale["grand_total"]))

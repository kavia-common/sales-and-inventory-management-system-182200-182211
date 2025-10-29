from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_immediate_after_sale_has_consistent_totals():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale_resp = client.post("/sales", json={"customer_name": "ImmediateInv", "line_items": [{"product_id": pid, "qty": 1}]})
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()

    inv_num = f"INV-IMM-{sale['id']}"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv = inv_resp.json()

    assert Decimal(str(inv["subtotal"])) == Decimal(str(sale["subtotal"]))
    assert Decimal(str(inv["gst_total"])) == Decimal(str(sale["gst_total"]))
    assert Decimal(str(inv["grand_total"])) == Decimal(str(sale["grand_total"]))

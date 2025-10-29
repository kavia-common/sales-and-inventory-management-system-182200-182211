from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_mirrors_sale_totals():
    client.post("/seed")
    # Ensure a product exists
    products = client.get("/products").json()
    if not products:
        p = client.post("/products", json={"name":"InvMirror","sku":"INV-MIR-1","price":11.25,"gst_rate":12.0,"stock_qty":5}).json()
        pid = p["id"]
    else:
        pid = products[0]["id"]

    sale = client.post("/sales", json={"customer_name":"Mirror","line_items":[{"product_id": pid, "qty": 2}]}).json()
    inv_no = f"INV-MIRROR-{sale['id']}"
    r = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r.status_code in (200, 201), r.text
    invoice = r.json()

    assert str(invoice["subtotal"]) == str(Decimal(str(sale["subtotal"])))
    assert str(invoice["gst_total"]) == str(Decimal(str(sale["gst_total"])))
    assert str(invoice["grand_total"]) == str(Decimal(str(sale["grand_total"])))

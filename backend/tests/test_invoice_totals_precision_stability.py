from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_totals_precision_stability():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    s = client.post("/sales", json={
        "customer_name": "Precision",
        "line_items": [{"product_id": pid, "qty": 3}]
    }).json()
    inv_no = f"INV-PREC-{s['id']}"
    inv = client.post("/invoices", json={"sale_id": s["id"], "invoice_number": inv_no}).json()
    for key in ("subtotal", "gst_total", "grand_total"):
        v = Decimal(str(inv[key]))
        assert v == v.quantize(Decimal("0.01"))

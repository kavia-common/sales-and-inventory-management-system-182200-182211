from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_after_multiline_sale_end_to_end():
    client.post("/seed")
    products = client.get("/products").json()
    assert len(products) >= 2
    p1, p2 = products[0], products[1]

    # Create a multi-line sale
    sale_resp = client.post("/sales", json={
        "customer_name": "E2E Invoice",
        "line_items": [
            {"product_id": p1["id"], "qty": 2},
            {"product_id": p2["id"], "qty": 3}
        ]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()

    # Create invoice
    inv_number = f"E2E-{sale['id']}"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_number})
    assert inv_resp.status_code in (200, 201), inv_resp.text
    invoice = inv_resp.json()

    # Totals mirror sale
    for k in ("subtotal", "gst_total", "grand_total"):
        assert Decimal(str(invoice[k])) == Decimal(str(sale[k]))

    # Retrieval by ID
    got = client.get(f"/invoices/{invoice['id']}")
    assert got.status_code == 200
    assert got.json()["invoice_number"] == inv_number

    # Presence in list
    lst = client.get("/invoices")
    assert lst.status_code == 200
    items = lst.json()
    assert any(i["id"] == invoice["id"] and i["invoice_number"] == inv_number for i in items)

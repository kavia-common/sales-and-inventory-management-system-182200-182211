from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_get_by_id_contract():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={
        "customer_name": "InvoiceByIdContract",
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()

    inv_number = f"INV-CONTRACT-{sale['id']}"
    created = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_number})
    assert created.status_code in (200, 201), created.text
    invoice = created.json()

    got = client.get(f"/invoices/{invoice['id']}")
    assert got.status_code == 200
    data = got.json()
    required = {"id", "sale_id", "invoice_number", "date", "subtotal", "gst_total", "grand_total"}
    assert required.issubset(set(data.keys()))
    assert data["sale_id"] == sale["id"]
    assert data["invoice_number"] == inv_number

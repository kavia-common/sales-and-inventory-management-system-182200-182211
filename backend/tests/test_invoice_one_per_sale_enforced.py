from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_cannot_create_multiple_invoices_for_same_sale():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={
        "customer_name": "SingleInvoice",
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()

    inv_num = f"INV-ONCE-{sale['id']}"
    first = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert first.status_code in (200, 201), first.text

    second = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num + "-DUP"})
    assert second.status_code == 400
    assert "already exists for this sale" in second.json().get("detail", "")

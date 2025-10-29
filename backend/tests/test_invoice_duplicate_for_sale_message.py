from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_duplicate_invoice_for_same_sale_returns_400_with_message():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={
        "customer_name": "DupInvSale",
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()

    r1 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-DUP-SALE-{sale['id']}"})
    assert r1.status_code in (200, 201), r1.text

    r2 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-DUP-SALE2-{sale['id']}"})
    assert r2.status_code == 400
    assert "already exists for this sale" in r2.json().get("detail", "")

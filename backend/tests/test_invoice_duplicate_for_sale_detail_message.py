from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_duplicate_invoice_for_sale_returns_specific_message():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={
        "customer_name": "DupInvMsg",
        "line_items": [{"product_id": pid, "qty": 1}]
    }).json()

    first = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-MSG-{sale['id']}"})
    assert first.status_code in (200, 201), first.text

    dup = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-MSG-2-{sale['id']}"})
    assert dup.status_code == 400
    detail = dup.json().get("detail", "")
    assert isinstance(detail, str)
    assert "already exists for this sale" in detail

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_duplicate_number_exact_match_rejected():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale1 = client.post("/sales", json={"customer_name": "DupNum1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    sale2 = client.post("/sales", json={"customer_name": "DupNum2", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    inv_num = "INV-DUP-EXACT-1"
    first = client.post("/invoices", json={"sale_id": sale1["id"], "invoice_number": inv_num})
    assert first.status_code in (200, 201), first.text

    dup = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": inv_num})
    assert dup.status_code == 400

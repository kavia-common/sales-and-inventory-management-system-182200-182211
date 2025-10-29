from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_duplicate_invoice_number_returns_400_with_message():
    client.post("/seed")
    # Create two sales
    products = client.get("/products").json()
    pid = products[0]["id"]
    sale1 = client.post("/sales", json={"customer_name": "InvDupMsg1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    sale2 = client.post("/sales", json={"customer_name": "InvDupMsg2", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    inv_num = "INV-MSG-001"
    r1 = client.post("/invoices", json={"sale_id": sale1["id"], "invoice_number": inv_num})
    assert r1.status_code in (200, 201), r1.text

    r2 = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": inv_num})
    assert r2.status_code == 400
    assert "already exists" in r2.json().get("detail", "")

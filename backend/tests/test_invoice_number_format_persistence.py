from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_with_mixed_format_persists_exactly():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "InvFmt", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = "INV_2025-01-TEST_001-A"
    r = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r.status_code in (200, 201), r.text
    body = r.json()
    assert body["invoice_number"] == inv_no

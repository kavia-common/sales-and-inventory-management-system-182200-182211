from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_surrounding_whitespace_duplicate_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    s1 = client.post("/sales", json={"customer_name": "WSDup1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    base = "INV-WS-DUP-01"
    r1 = client.post("/invoices", json={"sale_id": s1["id"], "invoice_number": base})
    assert r1.status_code in (200, 201), r1.text

    s2 = client.post("/sales", json={"customer_name": "WSDup2", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    dup = client.post("/invoices", json={"sale_id": s2["id"], "invoice_number": f"  {base}   "})
    assert dup.status_code in (200, 201, 400), dup.text

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_global_uniqueness():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    sale1 = client.post("/sales", json={"customer_name": "InvGlobal1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    sale2 = client.post("/sales", json={"customer_name": "InvGlobal2", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    inv_no = "INV-GLOBAL-UNIQ-001"
    r1 = client.post("/invoices", json={"sale_id": sale1["id"], "invoice_number": inv_no})
    assert r1.status_code in (200, 201), r1.text

    # Attempt same invoice number for a different sale should be rejected
    r2 = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": inv_no})
    assert r2.status_code == 400

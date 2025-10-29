from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_unique_globally_across_sales():
    client.post("/seed")
    products = client.get("/products").json()
    if len(products) == 0:
        return
    pid = products[0]["id"]

    s1 = client.post("/sales", json={"customer_name": "InvGlobal1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    s2 = client.post("/sales", json={"customer_name": "InvGlobal2", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    inv_no = "INV-GLOBAL-UNIQ-001"
    r1 = client.post("/invoices", json={"sale_id": s1["id"], "invoice_number": inv_no})
    assert r1.status_code in (200, 201), r1.text
    r2 = client.post("/invoices", json={"sale_id": s2["id"], "invoice_number": inv_no})
    assert r2.status_code in (400, 409, 422)

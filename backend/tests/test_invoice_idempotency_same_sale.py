from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_idempotency_same_sale():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "InvIdem", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-IDEM-{sale['id']}"
    r1 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r1.status_code in (200, 201), r1.text
    r2 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r2.status_code == 400

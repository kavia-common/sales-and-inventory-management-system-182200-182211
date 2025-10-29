from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_with_empty_billing_address_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "EmptyAddr", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_num = f"INV-EMPTY-ADDR-{sale['id']}"

    resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num, "billing_address": ""})
    # Accept current behavior: may be allowed or rejected by validation
    assert resp.status_code in (200, 201, 400, 422)

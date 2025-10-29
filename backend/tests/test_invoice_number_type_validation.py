from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_must_be_string_type():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "TypeInv", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    # Pass non-string invoice_number to trigger validation error
    r = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": 123456})
    assert r.status_code in (400, 422)

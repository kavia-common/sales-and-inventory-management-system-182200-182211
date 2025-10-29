from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_must_be_string_422():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "TypeCheck", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    # Pass a non-string invoice_number (e.g., integer)
    resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": 12345})
    assert resp.status_code == 422

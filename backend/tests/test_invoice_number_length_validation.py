from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_length_validation():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "LenInv", "line_items":[{"product_id": pid, "qty": 1}]}).json()
    long_no = "INV-" + ("X" * 300)
    r = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": long_no})
    assert r.status_code in (400, 422)

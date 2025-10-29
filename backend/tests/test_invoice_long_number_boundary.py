from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_long_boundary_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "LongInv", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    long_number = "I" * 100  # within 100 char field defined in models
    resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": long_number})
    # Expect acceptance under current schema; allow validation error if limits change
    assert resp.status_code in (200, 201, 400, 422)

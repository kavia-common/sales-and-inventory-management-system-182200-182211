from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_long_number_handling():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "LongNum", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    long_num = "INV-" + ("X" * 300)  # very long number

    resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": long_num})
    # Depending on DB constraints, this may be 200/201 (if column wide enough) or 400/422 if truncated/rejected.
    assert resp.status_code in (200, 201, 400, 422), resp.text

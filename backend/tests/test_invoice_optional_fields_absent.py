from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_without_optional_fields_succeeds():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={"customer_name": "No Optional Fields", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_num = f"INV-NOOPT-{sale['id']}"

    inv_resp = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": inv_num
    })
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv = inv_resp.json()
    # Optional fields should be present with null/None
    assert "billing_address" in inv
    assert "gstin" in inv

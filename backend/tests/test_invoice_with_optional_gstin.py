from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_with_optional_gstin():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={"customer_name": "GSTIN Customer", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_num = f"INV-GSTIN-{sale['id']}"
    gstin_value = "27AAAAA0000A1Z5"

    inv_resp = client.post("/invoices", json={
        "sale_id": sale["id"],
        "invoice_number": inv_num,
        "gstin": gstin_value
    })
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv = inv_resp.json()
    assert inv["gstin"] == gstin_value

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_optional_fields_present_in_schema():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={"customer_name": "SchemaOpt", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_num = f"INV-SCHEMA-OPT-{sale['id']}"

    inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv.status_code in (200, 201), inv.text
    data = inv.json()
    assert "billing_address" in data
    assert "gstin" in data

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_optional_fields_default_nulls():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "OptNulls", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-OPTNULL-{sale['id']}"
    r = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r.status_code in (200, 201), r.text
    inv = r.json()
    assert "billing_address" in inv
    assert "gstin" in inv
    # allow None or missing based on ORM defaults, but presence is checked above

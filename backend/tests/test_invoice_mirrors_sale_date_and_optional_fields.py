from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_mirrors_sale_date_and_optional_fields_omitted():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "InvMirror", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-MIRROR-{sale['id']}"})
    assert inv.status_code in (200, 201), inv.text
    body = inv.json()
    assert body["date"].startswith(sale["date"][:19])  # compare up to seconds
    # optional fields exist but may be null
    assert "billing_address" in body
    assert "gstin" in body

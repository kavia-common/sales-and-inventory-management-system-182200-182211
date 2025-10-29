from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_optional_keys_present_even_when_omitted():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "OptKeys", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-OPTKEY-{sale['id']}"})
    assert inv.status_code in (200, 201), inv.text
    data = inv.json()
    assert "billing_address" in data
    assert "gstin" in data

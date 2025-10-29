from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_preserves_gstin_value():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "GSTINPreserve", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    gstin = "27ABCDE1234F1Z5"
    inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-GSTIN-{sale['id']}", "gstin": gstin})
    assert inv.status_code in (200, 201), inv.text
    body = inv.json()
    assert body["gstin"] == gstin

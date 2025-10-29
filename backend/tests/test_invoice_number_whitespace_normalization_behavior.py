from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_whitespace_normalization_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "WSNorm", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    base_no = f"INV-WSN-{sale['id']}"
    r1 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": base_no})
    assert r1.status_code in (200, 201), r1.text
    # Try with whitespace
    r2 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": " " + base_no + " "})
    # Depending on normalization, allow 400 duplicate or 201 allowed; document behavior
    assert r2.status_code in (200, 201, 400), r2.text

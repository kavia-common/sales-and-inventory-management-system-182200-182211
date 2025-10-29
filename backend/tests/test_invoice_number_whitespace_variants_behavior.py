from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_whitespace_variants_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "WSVariants", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    base = f"INV-WSV-{sale['id']}"
    r1 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": base})
    assert r1.status_code in (200, 201), r1.text
    # Leading whitespace
    r2 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": "   " + base})
    assert r2.status_code in (200, 201, 400)
    # Trailing whitespace
    r3 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": base + "   "})
    assert r3.status_code in (200, 201, 400)
    # Tabs/newlines variants
    r4 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": "\t" + base + "\n"})
    assert r4.status_code in (200, 201, 400)

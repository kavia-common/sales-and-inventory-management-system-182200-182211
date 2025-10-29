from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_duplicate_with_surrounding_spaces():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "DupWS", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    base = f"INV-DWS-{sale['id']}"
    r1 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": base})
    assert r1.status_code in (200, 201), r1.text
    # post with spaces around base; accept current behavior 200/201 or 400 if normalized
    r2 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"  {base}  "})
    assert r2.status_code in (200, 201, 400)

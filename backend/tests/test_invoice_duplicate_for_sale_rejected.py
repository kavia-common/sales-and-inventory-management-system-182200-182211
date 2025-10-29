from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_duplicate_for_same_sale_rejected():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "DupForSale", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_num = f"INV-FORSALE-{sale['id']}"
    r1 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert r1.status_code in (200, 201), r1.text
    r2 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num + "-NEW"})
    assert r2.status_code in (400, 409, 422)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_gstin_must_be_string():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "GSTINType", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    r = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-GSTIN-TYPE-{sale['id']}", "gstin": 123456})
    assert r.status_code in (400, 422)

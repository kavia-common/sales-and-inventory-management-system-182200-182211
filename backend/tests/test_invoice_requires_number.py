from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_missing_number_rejected():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "NoNumber", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    r1 = client.post("/invoices", json={"sale_id": sale["id"]})
    assert r1.status_code in (400, 422)

    r2 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": ""})
    assert r2.status_code in (400, 422)

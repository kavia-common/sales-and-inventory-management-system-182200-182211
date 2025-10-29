from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_with_empty_number_is_rejected():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "EmptyInvNum", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": ""})
    assert resp.status_code in (400, 422)

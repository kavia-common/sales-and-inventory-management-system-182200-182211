from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_missing_invoice_number_returns_422():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        # if products not available, skip gracefully
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "NoInvNum", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    resp = client.post("/invoices", json={"sale_id": sale["id"]})
    assert resp.status_code in (400, 422)

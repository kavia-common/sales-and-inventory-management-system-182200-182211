from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_requires_number_validation():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "NoInvNum", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    # Missing invoice_number should yield 422
    r = client.post("/invoices", json={"sale_id": sale["id"]})
    assert r.status_code == 422

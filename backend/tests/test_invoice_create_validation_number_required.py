from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_requires_invoice_number_422():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "InvNoNum", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    resp = client.post("/invoices", json={"sale_id": sale["id"]})
    assert resp.status_code == 422

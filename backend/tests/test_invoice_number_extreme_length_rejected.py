from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_extreme_length_rejected():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "ExtremeLen", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = "INV-" + ("Y" * 1000)
    r = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r.status_code in (400, 422)

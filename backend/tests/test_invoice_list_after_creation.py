from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_list_after_creation():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "InvList", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-LIST-{sale['id']}"
    r_create = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r_create.status_code in (200, 201), r_create.text

    r_list = client.get("/invoices")
    assert r_list.status_code == 200
    assert isinstance(r_list.json(), list)

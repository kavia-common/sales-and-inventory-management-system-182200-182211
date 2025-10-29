from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_create_and_list_contains_the_invoice():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "InvList", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_number = f"INV-LIST-{sale['id']}"
    created = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_number})
    assert created.status_code in (200, 201), created.text
    invoice = created.json()

    lst = client.get("/invoices")
    assert lst.status_code == 200
    items = lst.json()
    assert any(i["id"] == invoice["id"] and i["invoice_number"] == inv_number for i in items)

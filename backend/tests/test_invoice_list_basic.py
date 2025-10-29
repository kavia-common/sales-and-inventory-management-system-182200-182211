from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_list_contains_created_invoice():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    sale_resp = client.post("/sales", json={"customer_name": "InvoiceList", "line_items": [{"product_id": pid, "qty": 1}]})
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()
    inv_num = f"INV-LIST-{sale['id']}"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv_resp.status_code in (200, 201), inv_resp.text

    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    assert isinstance(data, list)
    assert any(i["invoice_number"] == inv_num for i in data)

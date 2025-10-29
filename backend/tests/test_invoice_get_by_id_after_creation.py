from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_get_by_id_after_creation():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "GetById", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-GETID-{sale['id']}"
    created = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert created.status_code in (200, 201), created.text
    inv = created.json()
    got = client.get(f"/invoices/{inv['id']}")
    assert got.status_code == 200
    body = got.json()
    assert body["id"] == inv["id"]
    assert body["invoice_number"] == inv_no

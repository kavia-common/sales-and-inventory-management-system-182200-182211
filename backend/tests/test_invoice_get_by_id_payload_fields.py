from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_get_by_id_payload_fields():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "InvFields", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-FIELDS-{sale['id']}"
    r_create = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r_create.status_code in (200, 201), r_create.text
    inv = r_create.json()

    r_get = client.get(f"/invoices/{inv['id']}")
    assert r_get.status_code == 200
    data = r_get.json()
    for k in ("id", "sale_id", "invoice_number", "date", "subtotal", "gst_total", "grand_total"):
        assert k in data

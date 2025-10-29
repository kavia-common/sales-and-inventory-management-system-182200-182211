from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_entries_have_required_fields():
    # Ensure at least one invoice exists
    client.post("/seed")
    products = client.get("/products").json()
    if products:
        pid = products[0]["id"]
        s = client.post("/sales", json={"customer_name": "SchemaInv", "line_items": [{"product_id": pid, "qty": 1}]})
        if s.status_code in (200, 201):
            sale = s.json()
            client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-SCHEMA-{sale['id']}"})

    r = client.get("/invoices")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        inv = data[0]
        for key in ("id", "sale_id", "invoice_number", "date", "subtotal", "gst_total", "grand_total"):
            assert key in inv

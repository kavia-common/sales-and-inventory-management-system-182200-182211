from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_schema_integrity():
    client.post("/seed")
    # Ensure at least one invoice exists
    products = client.get("/products").json()
    if products:
        pid = products[0]["id"]
        sale = client.post("/sales", json={"customer_name": "SchemaInv", "line_items": [{"product_id": pid, "qty": 1}]}).json()
        client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-SCHEMAINV-{sale['id']}"})

    r = client.get("/invoices")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        keys = set(data[0].keys())
        expected = {"id", "sale_id", "invoice_number", "date", "billing_address", "gstin", "subtotal", "gst_total", "grand_total"}
        assert expected.issubset(keys)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_schema_contains_required_keys():
    client.post("/seed")
    # Ensure at least one invoice exists
    products = client.get("/products").json()
    assert products
    sale = client.post("/sales", json={
        "customer_name": "SchemaKeys",
        "line_items": [{"product_id": products[0]["id"], "qty": 1}]
    }).json()
    client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-SCHEMA-{sale['id']}"})

    resp = client.get("/invoices")
    assert resp.status_code == 200
    items = resp.json()
    assert isinstance(items, list)
    if items:
        required = {"id", "sale_id", "invoice_number", "date", "subtotal", "gst_total", "grand_total"}
        assert required.issubset(set(items[0].keys()))

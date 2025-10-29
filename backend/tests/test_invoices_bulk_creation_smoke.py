from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_bulk_creation_smoke():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Create multiple sales/invoices
    for i in range(10):
        sale = client.post("/sales", json={"customer_name": f"Bulk{i}", "line_items": [{"product_id": pid, "qty": 1}]}).json()
        inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-BULK-{sale['id']}"})
        assert inv.status_code in (200, 201), inv.text

    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    assert isinstance(data, list)
    # spot-check last item keys
    if data:
        for key in ("id", "sale_id", "invoice_number", "subtotal", "gst_total", "grand_total"):
            assert key in data[0]

from fastapi.testclient import TestClient
from src.api.main import app

def test_invoices_list_smoke():
    client = TestClient(app)
    client.post("/seed")
    # Ensure at least one invoice exists
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "Invoice Smoke", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-SMOKE-{sale['id']}"})

    resp = client.get("/invoices")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if data:
        inv = data[0]
        for key in ("id", "sale_id", "invoice_number", "subtotal", "gst_total", "grand_total"):
            assert key in inv

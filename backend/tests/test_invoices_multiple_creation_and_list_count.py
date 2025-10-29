from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_multiple_invoices_created_and_listed():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    created_ids = []
    for i in range(3):
        sale = client.post("/sales", json={
            "customer_name": f"MultiInv-{i}",
            "line_items": [{"product_id": pid, "qty": 1}]
        }).json()
        inv = client.post("/invoices", json={
            "sale_id": sale["id"],
            "invoice_number": f"INV-MULTI-{sale['id']}"
        })
        assert inv.status_code in (200, 201), inv.text
        created_ids.append(inv.json()["id"])

    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    assert isinstance(data, list)
    # ensure at least those invoices are present
    listed_ids = {inv["id"] for inv in data}
    assert set(created_ids).issubset(listed_ids)
    # basic field presence check
    for inv in data:
        for k in ("id", "sale_id", "invoice_number", "subtotal", "gst_total", "grand_total"):
            assert k in inv

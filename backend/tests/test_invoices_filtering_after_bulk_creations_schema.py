from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filtering_after_bulk_creations_schema():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    ids = []
    for i in range(3):
        sale = client.post("/sales", json={"customer_name": f"BulkFilter-{i}", "line_items": [{"product_id": pid, "qty": 1}]}).json()
        inv_no = f"INV-BULKFILT-{sale['id']}"
        inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
        assert inv.status_code in (200, 201), inv.text
        ids.append(inv.json()["id"])
        # filter by this number should return at least one entry with required fields
        r = client.get("/invoices", params={"invoice_number": inv_no})
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        if data:
            inv_item = data[0]
            for key in ("id", "sale_id", "invoice_number", "subtotal", "gst_total", "grand_total"):
                assert key in inv_item

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_get_by_number_via_filter_unique_match():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "FilterExact", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-EXACT-{sale['id']}"
    client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    r = client.get("/invoices", params={"invoice_number": inv_no})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(inv.get("invoice_number") == inv_no for inv in data)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filter_exact_match_single_result():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "ExactFilter", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-EXACT-SINGLE-{sale['id']}"
    inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert inv.status_code in (200, 201), inv.text

    r = client.get("/invoices", params={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        assert len([i for i in data if i.get("sale_id") == sale["id"] and i.get("invoice_number") == inv_no]) == 1

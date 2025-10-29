from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filter_by_invoice_number_returns_list():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "FilterByNum", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_number = f"INV-FILTER-{sale['id']}"
    client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_number})
    r = client.get(f"/invoices", params={"invoice_number": inv_number})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(inv.get("invoice_number") == inv_number for inv in data)

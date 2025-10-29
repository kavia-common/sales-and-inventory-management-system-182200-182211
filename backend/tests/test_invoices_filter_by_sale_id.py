from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filter_by_sale_id_returns_matching():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "FilterBySaleId", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_number = f"INV-FILTER-SID-{sale['id']}"
    client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_number})
    r = client.get(f"/invoices", params={"sale_id": sale["id"]})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(inv.get("sale_id") == sale["id"] for inv in data)

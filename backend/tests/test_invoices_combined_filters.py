from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_combined_filters_return_match():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "ComboFilter", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-COMB-{sale['id']}"
    client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    r = client.get("/invoices", params={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(i.get("sale_id") == sale["id"] and i.get("invoice_number") == inv_no for i in data)

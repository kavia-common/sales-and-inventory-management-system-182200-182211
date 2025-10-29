from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_list_with_matching_number_and_sale_id_returns_result():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={"customer_name": "MixFilter", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_num = f"INV-MIX-{sale['id']}"
    inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv.status_code in (200, 201), inv.text

    r = client.get("/invoices", params={"invoice_number": inv_num, "sale_id": sale["id"]})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(i["invoice_number"] == inv_num and i["sale_id"] == sale["id"] for i in data)

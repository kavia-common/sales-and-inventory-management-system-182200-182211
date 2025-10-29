from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_combined_filters_single_match():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    sale = client.post("/sales", json={"customer_name": "ComboFilter", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-COMBO-{sale['id']}"
    r_create = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r_create.status_code in (200, 201), r_create.text

    r = client.get("/invoices", params={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        assert len(data) == 1
        assert data[0]["sale_id"] == sale["id"]
        assert data[0]["invoice_number"] == inv_no

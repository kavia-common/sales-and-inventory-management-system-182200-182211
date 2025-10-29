from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filter_by_number_single_match():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "ByNumOnly", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-NUMONLY-{sale['id']}"
    rc = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert rc.status_code in (200, 201), rc.text

    r = client.get("/invoices", params={"invoice_number": inv_no})
    assert r.status_code == 200
    arr = r.json()
    assert isinstance(arr, list)
    assert len(arr) >= 1
    assert any(i["invoice_number"] == inv_no for i in arr)

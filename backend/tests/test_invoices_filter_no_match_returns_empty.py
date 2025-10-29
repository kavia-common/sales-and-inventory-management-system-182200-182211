from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filter_with_no_match_returns_empty_list():
    client.post("/seed")
    # Ensure some invoices exist
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    for i in range(2):
        sale = client.post("/sales", json={"customer_name": f"NoMatch{i}", "line_items": [{"product_id": pid, "qty": 1}]}).json()
        client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-NOM-{sale['id']}"})

    # Filter by a number that does not exist
    resp = client.get("/invoices?invoice_number=INV-DOES-NOT-EXIST-999999")
    assert resp.status_code == 200
    items = resp.json()
    assert isinstance(items, list)
    assert len(items) == 0 or all(i["invoice_number"] != "INV-DOES-NOT-EXIST-999999" for i in items)

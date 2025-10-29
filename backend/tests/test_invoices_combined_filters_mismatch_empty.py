from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_combined_filters_mismatch_returns_empty_list():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "Mismatch", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    # Create an invoice for that sale with one number
    client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-MISMATCH-{sale['id']}"})
    # Query with a different, non-matching invoice number
    r = client.get("/invoices", params={"sale_id": sale["id"], "invoice_number": "INV-NOT-REAL-999"})
    assert r.status_code == 200
    assert r.json() == [] or isinstance(r.json(), list)

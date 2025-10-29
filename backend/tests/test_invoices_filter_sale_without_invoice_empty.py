from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filter_by_sale_id_without_invoice_returns_empty():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    # Create a sale, but do not create an invoice for it
    sale = client.post("/sales", json={"customer_name": "NoInvoiceYet", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    r = client.get("/invoices", params={"sale_id": sale["id"]})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 0

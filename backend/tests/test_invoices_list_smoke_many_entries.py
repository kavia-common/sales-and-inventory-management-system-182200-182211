from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_smoke_with_many_entries():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    created = 0
    # Create a batch of invoices
    for _ in range(8):
        sale = client.post("/sales", json={"customer_name": "BatchInv", "line_items": [{"product_id": pid, "qty": 1}]}).json()
        inv_num = f"INV-BATCH-{sale['id']}"
        r = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
        assert r.status_code in (200, 201), r.text
        created += 1

    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    assert isinstance(data, list)
    assert len(data) >= created
    # Simulate client-side pagination
    page = data[:5]
    assert len(page) <= 5

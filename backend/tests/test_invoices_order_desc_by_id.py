from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_are_returned_desc_by_id():
    client.post("/seed")
    products = client.get("/products").json()
    pid = products[0]["id"]

    created_ids = []
    for i in range(3):
        sale = client.post("/sales", json={"customer_name": f"Order{i}", "line_items": [{"product_id": pid, "qty": 1}]}).json()
        inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-ORD-{sale['id']}"}).json()
        created_ids.append(inv["id"])

    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    ids = [i["id"] for i in data]
    # Ensure list is non-increasing (desc)
    assert ids == sorted(ids, reverse=True)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_is_ordered_by_id_desc():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Create multiple invoices
    sale1 = client.post("/sales", json={"customer_name": "Ord1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv1 = client.post("/invoices", json={"sale_id": sale1["id"], "invoice_number": f"INV-ORD-1-{sale1['id']}"}).json()

    sale2 = client.post("/sales", json={"customer_name": "Ord2", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv2 = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": f"INV-ORD-2-{sale2['id']}"}).json()

    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    if len(data) >= 2:
        assert data[0]["id"] >= data[1]["id"]

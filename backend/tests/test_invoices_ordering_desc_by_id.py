from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_ordering_desc_by_id():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    # Create two sales+invoices
    s1 = client.post("/sales", json={"customer_name": "OrderA", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv1_no = f"INV-ORDER-{s1['id']}"
    client.post("/invoices", json={"sale_id": s1["id"], "invoice_number": inv1_no})
    s2 = client.post("/sales", json={"customer_name": "OrderB", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv2_no = f"INV-ORDER-{s2['id']}"
    client.post("/invoices", json={"sale_id": s2["id"], "invoice_number": inv2_no})

    r = client.get("/invoices")
    assert r.status_code == 200
    data = r.json()
    if len(data) >= 2:
        assert data[0]["id"] >= data[1]["id"]

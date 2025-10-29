from fastapi.testclient import TestClient
from src.api.main import app
import time

client = TestClient(app)

def test_invoices_list_ordering_desc_by_id():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    # Create two invoices via sales
    s1 = client.post("/sales", json={"customer_name": "InvOrder1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    time.sleep(0.01)
    s2 = client.post("/sales", json={"customer_name": "InvOrder2", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    client.post("/invoices", json={"sale_id": s1["id"], "invoice_number": f"INV-ORD-{s1['id']}"})
    client.post("/invoices", json={"sale_id": s2["id"], "invoice_number": f"INV-ORD-{s2['id']}"})
    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    if len(data) >= 2:
        ids = [d["id"] for d in data]
        assert ids == sorted(ids, reverse=True)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_multiple_creations_and_list_stability():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    created_ids = []
    for i in range(3):
        sale = client.post("/sales", json={"customer_name": f"Stability-{i}", "line_items": [{"product_id": pid, "qty": 1}]}).json()
        inv_no = f"INV-STAB-{sale['id']}"
        inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
        assert inv.status_code in (200, 201), inv.text
        created_ids.append(inv.json()["id"])

    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    ids = {d["id"] for d in data}
    assert any(cid in ids for cid in created_ids)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_bulk_creation_list_consistency():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    created = []
    for i in range(5):
        s = client.post("/sales", json={"customer_name": f"BulkInv-{i}", "line_items": [{"product_id": pid, "qty": 1}]}).json()
        inv = client.post("/invoices", json={"sale_id": s["id"], "invoice_number": f"INV-BULK-{s['id']}"})
        assert inv.status_code in (200, 201), inv.text
        created.append(inv.json()["id"])

    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    ids = {d["id"] for d in data}
    assert any(cid in ids for cid in created)

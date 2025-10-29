from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_contains_invoices_for_distinct_sales():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    sale_ids = []
    for i in range(3):
        s = client.post("/sales", json={"customer_name": f"InvDistinct-{i}", "line_items": [{"product_id": pid, "qty": 1}]}).json()
        sale_ids.append(s["id"])
        resp = client.post("/invoices", json={"sale_id": s["id"], "invoice_number": f"INV-DISTINCT-{s['id']}"})
        assert resp.status_code in (200, 201), resp.text

    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    returned_sale_ids = {d.get("sale_id") for d in data}
    assert any(sid in returned_sale_ids for sid in sale_ids)

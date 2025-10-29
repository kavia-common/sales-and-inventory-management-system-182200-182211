from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_contains_multiple_created_items():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    created_numbers = []
    for i in range(3):
        sale = client.post("/sales", json={"customer_name": f"ListInv-{i}", "line_items": [{"product_id": pid, "qty": 1}]}).json()
        inv_num = f"INV-LIST-SET-{sale['id']}"
        resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
        assert resp.status_code in (200, 201), resp.text
        created_numbers.append(inv_num)

    lst = client.get("/invoices")
    assert lst.status_code == 200
    data = lst.json()
    nums = {d.get("invoice_number") for d in data}
    for n in created_numbers:
        assert n in nums
    assert all({"id", "invoice_number", "sale_id"}.issubset(set(d.keys())) for d in data)

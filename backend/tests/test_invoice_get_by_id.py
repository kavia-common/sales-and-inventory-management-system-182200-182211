from fastapi.testclient import TestClient
from src.api.main import app
from decimal import Decimal

client = TestClient(app)

def test_get_invoice_by_id_returns_expected_fields():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Create sale and invoice
    sale = client.post("/sales", json={"customer_name": "GetById", "line_items": [{"product_id": pid, "qty": 2}]}).json()
    inv_num = f"INV-GETID-{sale['id']}"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv_created = inv_resp.json()
    inv_id = inv_created["id"]

    # Retrieve by ID
    get_resp = client.get(f"/invoices/{inv_id}")
    assert get_resp.status_code == 200
    inv = get_resp.json()
    assert inv["id"] == inv_id
    assert inv["invoice_number"] == inv_num
    assert inv["sale_id"] == sale["id"]
    # Totals mirrored
    assert Decimal(str(inv["subtotal"])) == Decimal(str(sale["subtotal"]))
    assert Decimal(str(inv["gst_total"])) == Decimal(str(sale["gst_total"]))
    assert Decimal(str(inv["grand_total"])) == Decimal(str(sale["grand_total"]))

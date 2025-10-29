from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_decrements_inventory_and_invoice_totals_mirror_sale():
    # Seed sample products
    client.post("/seed")
    products = client.get("/products").json()
    assert products, "Seed should create products"
    p = products[0]
    pid = p["id"]
    initial_qty = int(p["stock_qty"])

    # Create a simple sale of qty 2 for first product
    qty = 2
    sale_resp = client.post("/sales", json={
        "customer_name": "E2E",
        "line_items": [{"product_id": pid, "qty": qty}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()

    # Check inventory decreased
    product_after = client.get(f"/products/{pid}").json()
    assert int(product_after["stock_qty"]) == initial_qty - qty

    # Create invoice from sale
    inv_num = f"INV-E2E-{sale['id']}"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv_resp.status_code in (200, 201), inv_resp.text
    inv = inv_resp.json()

    # Totals mirror
    assert Decimal(str(inv["subtotal"])) == Decimal(str(sale["subtotal"]))
    assert Decimal(str(inv["gst_total"])) == Decimal(str(sale["gst_total"]))
    assert Decimal(str(inv["grand_total"])) == Decimal(str(sale["grand_total"]))

from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sales_gst_calculation_and_inventory_adjustment():
    # Seed products to ensure at least product id 1 exists
    client.post("/seed")

    # Fetch products and pick one
    products = client.get("/products").json()
    assert products, "No products available after seed"
    p = products[-1]  # oldest or just pick any
    prod_id = p["id"]
    stock_before = p["stock_qty"]
    price = Decimal(str(p["price"]))
    gst_rate = Decimal(str(p["gst_rate"]))

    # Create a sale for qty=2
    qty = 2
    resp = client.post("/sales", json={
        "customer_name": "GST Tester",
        "line_items": [{"product_id": prod_id, "qty": qty}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()

    # Validate totals
    expected_subtotal = (price * qty).quantize(Decimal("0.01"))
    expected_gst = (expected_subtotal * gst_rate / Decimal("100")).quantize(Decimal("0.01"))
    expected_total = (expected_subtotal + expected_gst).quantize(Decimal("0.01"))
    assert Decimal(str(sale["subtotal"])) == expected_subtotal
    assert Decimal(str(sale["gst_total"])) == expected_gst
    assert Decimal(str(sale["grand_total"])) == expected_total

    # Check inventory decreased
    p_after = client.get(f"/products/{prod_id}").json()
    assert p_after["stock_qty"] == stock_before - qty

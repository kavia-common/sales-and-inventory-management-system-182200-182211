from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_paged_with_offset():
    client.post("/seed")
    # Ensure multiple products exist
    for i in range(3):
        client.post("/products", json={"name": f"Paged{i}", "sku": f"PAGED-{i}", "price": 1+i, "gst_rate": 5.0, "stock_qty": i})
    first = client.get("/products/paged", params={"limit": 2, "offset": 0}).json()
    second = client.get("/products/paged", params={"limit": 2, "offset": 2}).json()
    assert isinstance(first, list) and isinstance(second, list)

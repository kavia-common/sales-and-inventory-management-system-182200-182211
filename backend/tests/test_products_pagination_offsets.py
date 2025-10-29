from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_pagination_offsets_do_not_error():
    client.post("/seed")

    # Request first page
    r1 = client.get("/products/paged?offset=0&limit=1")
    assert r1.status_code == 200
    page1 = r1.json()
    assert isinstance(page1, list)

    # Request next page
    r2 = client.get("/products/paged?offset=1&limit=1")
    assert r2.status_code == 200
    page2 = r2.json()
    assert isinstance(page2, list)

    # Request beyond range should still return list (possibly empty)
    r3 = client.get("/products/paged?offset=9999&limit=10")
    assert r3.status_code == 200
    page3 = r3.json()
    assert isinstance(page3, list)

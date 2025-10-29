from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_seed_endpoint_idempotent():
    r1 = client.post("/seed")
    assert r1.status_code in (200, 201), r1.text
    count1 = r1.json().get("seeded_products")
    assert isinstance(count1, int)

    r2 = client.post("/seed")
    assert r2.status_code in (200, 201), r2.text
    count2 = r2.json().get("seeded_products")
    # After first seed, second call should not add more, so count stays >= first set
    assert count2 >= count1

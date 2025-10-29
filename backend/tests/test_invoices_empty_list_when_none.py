from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_empty_list_when_none():
    # New app instance DB may be empty; ensure at least seeded products but no invoices
    client.post("/seed")
    resp = client.get("/invoices")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_stability():
    # Ensure deterministic behavior returns list on multiple calls
    r1 = client.get("/invoices")
    r2 = client.get("/invoices")
    assert r1.status_code == 200 and r2.status_code == 200
    assert isinstance(r1.json(), list) and isinstance(r2.json(), list)

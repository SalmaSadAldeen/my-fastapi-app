from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_config_endpoint():
    r = client.get("/config")
    assert r.status_code == 200
    data = r.json()
    assert "api_secret_configured" in data
    assert "API_SECRET" not in str(data)

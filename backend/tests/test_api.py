from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "OpenNavy" in data["message"] or "Praxia" in data["message"]
    assert data["docs_url"] == "/docs"


def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["knowledge_base"]["criteria_documents"] >= 9
    assert data["knowledge_base"]["team_standards_documents"] >= 2
    assert "maintainability_index" in data["criteria_weights"]

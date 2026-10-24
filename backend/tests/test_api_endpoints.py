from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db

client = TestClient(app)


def setup_module():
    init_db()


def test_repos_crud_and_endpoints():
    # 1. Crear Repositorio
    create_payload = {
        "url": "https://github.com/my-org/sentinel-demo",
        "name": "sentinel-demo",
        "default_branch": "main",
    }
    response = client.post("/api/v1/repos/", json=create_payload)
    assert response.status_code == 200
    repo_data = response.json()
    assert repo_data["url"] == create_payload["url"]
    repo_id = repo_data["id"]

    # 2. Listar Repositorios
    list_response = client.get("/api/v1/repos/")
    assert list_response.status_code == 200
    repos_list = list_response.json()
    assert len(repos_list) >= 1
    assert any(r["id"] == repo_id for r in repos_list)

    # 3. Detalle de Repositorio
    detail_response = client.get(f"/api/v1/repos/{repo_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["name"] == "sentinel-demo"

    # 4. Trigger de Análisis
    analyze_payload = {
        "repo_url": "https://github.com/my-org/sentinel-demo",
        "branch": "main",
    }
    analyze_response = client.post("/api/v1/repos/analyze", json=analyze_payload)
    assert analyze_response.status_code == 200
    job_data = analyze_response.json()
    assert "job_id" in job_data
    job_id = job_data["job_id"]

    # 5. Consultar métricas del repositorio
    metrics_response = client.get(f"/api/v1/repos/{repo_id}/metrics")
    assert metrics_response.status_code == 200

    # 6. Consultar historial de métricas
    history_response = client.get(f"/api/v1/repos/{repo_id}/metrics/history")
    assert history_response.status_code == 200

    # 7. Consultar hallazgos (findings)
    findings_response = client.get(f"/api/v1/repos/{repo_id}/findings")
    assert findings_response.status_code == 200

    # 8. Consultar arquitectura y conocimiento generado
    arch_response = client.get(f"/api/v1/repos/{repo_id}/architecture")
    assert arch_response.status_code == 200

    knowledge_response = client.get(f"/api/v1/repos/{repo_id}/knowledge")
    assert knowledge_response.status_code == 200

    # 9. Conversational RAG Chat
    chat_payload = {
        "message": "¿Cuáles son las principales recomendaciones de modularidad y SOLID?",
    }
    chat_response = client.post(f"/api/v1/repos/{repo_id}/chat", json=chat_payload)
    assert chat_response.status_code == 200
    chat_data = chat_response.json()
    assert "response" in chat_data
    assert len(chat_data["cited_sources"]) >= 1

    # 10. Eliminar Repositorio individualmente
    delete_response = client.delete(f"/api/v1/repos/{repo_id}")
    assert delete_response.status_code == 200
    del_data = delete_response.json()
    assert del_data["success"] is True
    assert del_data["repo_id"] == repo_id

    # 11. Verificar que ya no existe (404)
    get_deleted = client.get(f"/api/v1/repos/{repo_id}")
    assert get_deleted.status_code == 404


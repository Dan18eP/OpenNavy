import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.ai_opportunity_evaluator import AIOpportunityEvaluator
from app.models.entities import Repo
from app.core.database import SessionLocal, init_db

client = TestClient(app)


def setup_module():
    init_db()


def test_ai_opportunity_evaluator_quadrants():
    evaluator = AIOpportunityEvaluator()

    # 1. Componente criptográfico / seguridad -> NO RECOMENDADO
    crypto_item = evaluator.evaluate_component("crypto_hasher", "Cálculo de hash y cifrado de claves privadas")
    assert crypto_item.cuadrante == "NO RECOMENDADO"
    assert "criptográfic" in crypto_item.justificacion.lower()

    # 2. Componente de parsing AST / cálculo métrico -> AUTOMATIZABLE
    ast_item = evaluator.evaluate_component("ast_parser", "Parsing sintáctico de árboles y cálculo de complejidad ciclomática")
    assert ast_item.cuadrante == "AUTOMATIZABLE"
    assert "tree-sitter" in ast_item.justificacion.lower() or "determinístic" in ast_item.recomendacion_arquitectura.lower()

    # 3. Componente de chat / explicaciones de diseño -> ASISTIDO POR IA
    chat_item = evaluator.evaluate_component("chat_assistant", "Asistente técnico que responde dudas de arquitectura con RAG")
    assert chat_item.cuadrante == "ASISTIDO POR IA"
    assert "rag" in chat_item.justificacion.lower()

    # 4. Componente con datos o descripción vacía -> POR VALIDAR
    empty_item = evaluator.evaluate_component("unknown_pkg", "", "")
    assert empty_item.cuadrante == "POR VALIDAR"


def test_ai_opportunity_repository_evaluation():
    evaluator = AIOpportunityEvaluator()
    modules = [
        {"name": "auth_manager", "description": "Gestión de autenticación y webhooks"},
        {"name": "mccabe_calculator", "description": "Cálculo de complejidad ciclomática"},
        {"name": "evaluator_agent", "description": "Agente evaluador contextual con LLM"},
        {"name": "secret_crypto", "description": "Cifrado simétrico de datos sensibles"},
        {"name": "empty_module", "description": ""},
    ]

    result = evaluator.evaluate_repository(modules)
    assert result.total_evaluados == 5
    assert result.resumen_cuadrantes["AUTOMATIZABLE"] >= 1
    assert result.resumen_cuadrantes["ASISTIDO POR IA"] >= 1
    assert result.resumen_cuadrantes["NO RECOMENDADO"] >= 1
    assert result.resumen_cuadrantes["POR VALIDAR"] >= 1
    assert len(result.ahorro_potencial_computo) > 10


def test_ai_opportunity_api_endpoint():
    db = SessionLocal()
    try:
        repo = db.query(Repo).filter_by(id="repo-ai-opp-test").first()
        if not repo:
            repo = Repo(id="repo-ai-opp-test", name="test-ai-repo", url="https://github.com/test/ai-opp")
            db.add(repo)
            db.commit()
    finally:
        db.close()

    payload = [
        {"name": "ast_service", "description": "Parsing y métricas"},
        {"name": "chat_service", "description": "Chat con RAG"},
    ]

    response = client.post("/api/v1/repos/repo-ai-opp-test/ai-opportunity", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_evaluados"] == 2
    assert "resumen_cuadrantes" in data
    assert len(data["matriz"]) == 2

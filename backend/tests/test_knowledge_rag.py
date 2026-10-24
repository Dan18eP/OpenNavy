import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app
from app.rag.knowledge_loader import KnowledgeLoader
from app.rag.vector_store import HybridVectorStore
from app.rag.retriever import get_knowledge_retriever
from app.core.config import settings, PROJECT_ROOT


def test_knowledge_loader_indexes_canonical_and_adrs():
    """Valida que KnowledgeLoader indexe la base de conocimiento de docs/knowledge_base y docs/adr."""
    loader = KnowledgeLoader(PROJECT_ROOT / "docs" / "knowledge_base")
    chunks = loader.load_all_chunks()
    
    assert len(chunks) > 50
    tiers = {c.get("source_tier") for c in chunks}
    assert "canonical" in tiers
    assert "criteria" in tiers or "team_standard" in tiers
    assert "adr" in tiers


def test_vector_store_hybrid_retrieval():
    """Valida que el vector store recupere estandares de Clean Architecture y GitFlow."""
    retriever = get_knowledge_retriever()
    
    # 1. Busqueda sobre Clean Architecture / Capas
    results_arch = retriever.search_general("Clean Architecture layering rules ports adapters", top_k=3)
    assert len(results_arch) > 0
    paths = [r.get("doc_path", "").lower() for r in results_arch]
    assert any("layering-rules" in p or "clean_architecture" in p or "solid" in p for p in paths)

    # 2. Busqueda sobre GitFlow y colaboracion
    results_git = retriever.search_general("GitFlow conventional commits develop main branch", top_k=3)
    assert len(results_git) > 0
    git_paths = [r.get("doc_path", "").lower() for r in results_git]
    assert any("git-workflow" in p or "0005-gitflow" in p for p in git_paths)


def test_course_plotter_with_rag_enrichment():
    """Valida que /api/v1/course/plot integre el contexto RAG de la base de conocimiento."""
    client = TestClient(app)
    payload = {
        "repo_id": "test-repo-rag",
        "mission": "Refactor authentication layer to enforce clean architecture and remove circular dependencies",
        "officer_name": "Lieutenant-RAG",
    }
    res = client.post("/api/v1/course/plot", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "waypoints" in data
    assert "thought_process" in data
    assert "drift_risk" in data
    assert "reef_warnings" in data


def test_opennavy_identity_in_prompts():
    """Valida que la identidad del Almirante de OpenNavy prevalezca sin referencias residuales a Praxia."""
    from app.analyzers.guardrails import DomainIntentGuard
    
    # El mensaje de rechazo estandar debe referenciar a OpenNavy
    assert "OpenNavy" in DomainIntentGuard.STANDARD_REJECTION_MESSAGE
    assert "Praxia" not in DomainIntentGuard.STANDARD_REJECTION_MESSAGE

import pytest
from pathlib import Path
from app.rag.knowledge_loader import KnowledgeLoader
from app.rag.indexer import CorpusIndexer
from app.rag.retriever import KnowledgeRetriever
from app.core.config import settings


def test_canonical_rubric_files_exist():
    """Verifica que los 5 documentos normativos exigidos por HU-RAG-01 existan."""
    kb_criteria = settings.KNOWLEDGE_BASE_PATH / "criteria"

    expected_files = [
        "iso_25010_maintainability.md",
        "mccabe_sei_complexity.md",
        "clean_architecture_solid.md",
        "fowler_refactoring_smells.md",
        "owasp_security_rubric.md",
    ]

    for fname in expected_files:
        fpath = kb_criteria / fname
        assert fpath.exists(), f"El archivo canónico {fname} no existe en {kb_criteria}"
        content = fpath.read_text(encoding="utf-8")
        assert len(content) > 200
        assert "**Autoridad:**" in content
        assert "**Rule-ID:**" in content
        assert "**Severidad:**" in content


def test_knowledge_loader_extracts_formal_metadata():
    """Verifica que KnowledgeLoader extraiga authority, rule_id, category y severity."""
    loader = KnowledgeLoader()
    chunks = loader.load_all_chunks()

    assert len(chunks) > 0

    # Buscar chunks de los nuevos documentos normativos
    iso_chunks = [c for c in chunks if "iso_25010" in c.get("criterion", "")]
    mccabe_chunks = [c for c in chunks if "mccabe_sei" in c.get("criterion", "")]
    clean_chunks = [c for c in chunks if "clean_architecture" in c.get("criterion", "")]
    owasp_chunks = [c for c in chunks if "owasp_security" in c.get("criterion", "")]

    assert len(iso_chunks) >= 1
    assert "ISO/IEC 25010" in iso_chunks[0].get("authority", "")
    assert iso_chunks[0].get("rule_id") == "ISO-25010-MAINT-01"

    assert len(mccabe_chunks) >= 1
    assert "McCabe" in mccabe_chunks[0].get("authority", "")

    assert len(clean_chunks) >= 1
    assert "Robert C. Martin" in clean_chunks[0].get("authority", "")

    assert len(owasp_chunks) >= 1
    assert "OWASP" in owasp_chunks[0].get("authority", "")


def test_corpus_indexer_indexing_and_vector_search():
    """Prueba el indexador del corpus y la recuperación con similitud semántica."""
    indexer = CorpusIndexer()
    result = indexer.index_corpus()

    assert result["is_indexed"] is True
    assert result["total_chunks_indexed"] >= 15
    assert len(result["distinct_authorities"]) >= 3

    # Buscar por concepto normativo: "complejidad ciclomática grafo linealmente independiente"
    matches = indexer.search_with_threshold("complejidad ciclomática mccabe caminos independientes", top_k=3, min_score=0.10)
    assert len(matches) > 0
    top_match = matches[0]
    assert any(k in top_match["content"].lower() for k in ["mccabe", "ciclomática", "complejidad"])


def test_retriever_formal_authority_queries():
    """Verifica que el retriever formal responda con precisión a consultas de rúbricas."""
    retriever = KnowledgeRetriever()

    # Consulta de Clean Architecture Dependency Rule
    arch_rubrics = retriever.retrieve_rubric(
        criterion="clean_architecture_solid",
        query="The Dependency Rule dependencias hacia adentro dominio",
        top_k=2
    )
    assert len(arch_rubrics) >= 1
    assert any("dependency rule" in r["content"].lower() or "dependencia" in r["content"].lower() for r in arch_rubrics)

    # Consulta de OWASP Prompt Injection
    sec_rubrics = retriever.retrieve_rubric(
        criterion="owasp_security_rubric",
        query="Prompt Injection LLM01 delimitation untrusted",
        top_k=2
    )
    assert len(sec_rubrics) >= 1
    assert any("llm01" in r["content"].lower() or "prompt injection" in r["content"].lower() for r in sec_rubrics)

from pathlib import Path
import pytest

from app.rag.knowledge_loader import KnowledgeLoader
from app.rag.vector_store import HybridVectorStore
from app.rag.retriever import KnowledgeRetriever, get_knowledge_retriever


def test_knowledge_loader_extracts_chunks():
    loader = KnowledgeLoader()
    chunks = loader.load_all_chunks()

    assert len(chunks) >= 20, f"Expected at least 20 chunks from knowledge base, got {len(chunks)}"

    criteria_found = {c["criterion"] for c in chunks}
    assert "solid_principles" in criteria_found
    assert "cyclomatic_complexity" in criteria_found
    assert "maintainability_index" in criteria_found
    assert "clean_code" in criteria_found
    assert "architecture_guidelines" in criteria_found

    # Validar campos de un chunk
    first_chunk = chunks[0]
    assert "chunk_id" in first_chunk
    assert "doc_path" in first_chunk
    assert "content" in first_chunk
    assert "chunk_type" in first_chunk
    assert len(first_chunk["content"]) > 20


def test_vector_store_similarity_search():
    store = HybridVectorStore()
    sample_chunks = [
        {
            "chunk_id": "solid#srp",
            "criterion": "solid_principles",
            "heading": "Single Responsibility Principle (SRP)",
            "content": "Una clase debe tener una sola razón para cambiar. No mezclar persistencia y lógica.",
            "chunk_type": "rule",
        },
        {
            "chunk_id": "cc#thresholds",
            "criterion": "cyclomatic_complexity",
            "heading": "Umbrales de Complejidad",
            "content": "Complejidad ciclomática mayor a 10 es riesgo moderado, mayor a 20 es crítico.",
            "chunk_type": "threshold",
        },
        {
            "chunk_id": "clean#functions",
            "criterion": "clean_code",
            "heading": "Funciones Pequeñas",
            "content": "Las funciones deben tener idealmente menos de 20 líneas y un solo nivel de abstracción.",
            "chunk_type": "rule",
        },
    ]

    store.add_chunks(sample_chunks)

    # 1. Búsqueda de SRP
    results_srp = store.search("persistencia y lógica en clase", top_k=2)
    assert len(results_srp) > 0
    assert results_srp[0]["chunk_id"] == "solid#srp"
    assert results_srp[0]["similarity_score"] > 0

    # 2. Búsqueda con filtro de criterio
    results_filtered = store.search("funciones", top_k=2, filters={"criterion": "clean_code"})
    assert len(results_filtered) == 1
    assert results_filtered[0]["chunk_id"] == "clean#functions"


def test_retriever_retrieve_rubric():
    retriever = get_knowledge_retriever()

    # Recuperar rúbrica de SOLID
    chunks = retriever.retrieve_rubric(
        criterion="solid_principles",
        query="clase mezcla base de datos, smtp email y validacion",
        top_k=2
    )

    assert len(chunks) > 0
    assert chunks[0]["criterion"] == "solid_principles"
    assert "single_responsibility" in chunks[0]["content"].lower() or "srp" in chunks[0]["content"].lower() or "responsabilidad" in chunks[0]["content"].lower()

    # Formatear contexto para LLM
    formatted = retriever.format_context_for_llm(chunks)
    assert "--- [RAG CHUNK 1]" in formatted
    assert "Fuente:" in formatted
    assert "Criterio: solid_principles" in formatted


def test_retriever_general_chat_search():
    retriever = get_knowledge_retriever()
    results = retriever.search_general("¿cuáles son los límites de complejidad ciclomática de McCabe?", top_k=3)

    assert len(results) > 0
    criteria_in_results = [r["criterion"] for r in results]
    assert "cyclomatic_complexity" in criteria_in_results

from typing import Dict, Any, List
from app.schemas.state import AnalysisState
from app.rag.retriever import get_knowledge_retriever


def rag_retrieval_node(state: AnalysisState) -> Dict[str, Any]:
    """Nodo 3: Recupera la rúbrica RAG adecuada según los hallazgos y características del repositorio."""
    retriever = get_knowledge_retriever()
    rag_chunks: List[Dict[str, Any]] = []

    # 1. Recuperar contexto de SOLID y Clean Architecture (Canónico + Rúbrica)
    solid_chunks = retriever.retrieve_rubric(
        criterion="solid_principles",
        query="Clean Architecture Robert Martin Single Responsibility Dependency Inversion DIP SRP",
        top_k=2
    )
    if not any(c.get("is_canonical") for c in solid_chunks):
        # Asegurar inclusión del libro canónico de Clean Architecture
        canonical_solid = retriever.search_general("Clean Architecture SOLID Dependency Inversion", top_k=1)
        solid_chunks = (canonical_solid + solid_chunks)[:2]
    rag_chunks.extend(solid_chunks)

    # 2. Recuperar contexto de Clean Code y Refactoring (Canónico + Rúbrica)
    clean_chunks = retriever.retrieve_rubric(
        criterion="clean_code",
        query="Martin Fowler Refactoring Code Smells Long Method small functions guard clauses",
        top_k=2
    )
    rag_chunks.extend(clean_chunks)

    # 3. Si hay violaciones arquitectónicas o ciclos, recuperar ISO 5055 y Clean Architecture
    arch_diff = state.get("architecture_diff", {})
    if arch_diff.get("has_cycles") or arch_diff.get("layer_violations"):
        arch_chunks = retriever.search_general(
            "ISO 5055 architecture layer violations circular dependencies Dependency Rule",
            top_k=2
        )
        rag_chunks.extend(arch_chunks)

    # 4. Si hay complejidad alta, recuperar NIST SP 500-235 (McCabe) e ISO 25010
    if state.get("complexity_findings") or state.get("deterministic_metrics", {}).get("maintainability_index", 100) < 70:
        cc_chunks = retriever.search_general(
            "NIST SP 500-235 McCabe Cyclomatic Complexity ISO 25010 maintainability thresholds",
            top_k=2
        )
        rag_chunks.extend(cc_chunks)

    return {
        "rag_context": rag_chunks,
        "current_step": "rag_retrieval_completed",
    }

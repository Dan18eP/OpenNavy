from pathlib import Path
from typing import List, Dict, Any, Optional

from app.rag.knowledge_loader import KnowledgeLoader
from app.rag.vector_store import HybridVectorStore
from app.core.config import settings


class KnowledgeRetriever:
    """Recuperador semántico RAG para la rúbrica de calidad y estándares técnicos."""

    def __init__(self, kb_dir: Optional[Path] = None):
        self.loader = KnowledgeLoader(kb_dir)
        self.vector_store = HybridVectorStore()
        self._initialize()

    def _initialize(self) -> None:
        """Carga e indexa automáticamente todos los documentos de la base de conocimiento."""
        chunks = self.loader.load_all_chunks()
        if chunks:
            self.vector_store.add_chunks(chunks)

    def retrieve_rubric(
        self,
        criterion: str,
        query: str,
        top_k: int = 3,
        language: str = "all",
    ) -> List[Dict[str, Any]]:
        """
        Recupera los fragmentos de rúbrica más relevantes para un criterio específico y contexto de código.
        """
        filters = {}
        if criterion and criterion != "all":
            filters["criterion"] = criterion

        results = self.vector_store.search(
            query=f"{criterion} {query}",
            top_k=top_k,
            filters=filters if filters else None,
        )

        return results

    def format_context_for_llm(self, chunks: List[Dict[str, Any]]) -> str:
        """Formatea los fragmentos RAG recuperados como texto estructurado para el prompt del LLM."""
        if not chunks:
            return "No se recuperaron fragmentos de rúbrica específicos."

        formatted_parts = []
        for i, chunk in enumerate(chunks, 1):
            source_citation = f"{chunk.get('doc_path', 'doc')}#{chunk.get('chunk_id', '')}"
            authority = chunk.get("authority", "OpenNavy Standard")
            rule_id = chunk.get("rule_id", "NORM")
            tier = chunk.get("source_tier", "")
            is_can = chunk.get("is_canonical") or "canonical/" in str(chunk.get("doc_path", "")).lower()
            if is_can or tier == "canonical":
                tier_label = "FUENTE CANÓNICA CERTIFICADA"
            elif tier == "team_standard":
                tier_label = "ESTÁNDAR DE EQUIPO (POLÍTICA INTERNA)"
            elif tier == "module_doc":
                tier_label = "DOCUMENTACIÓN VIVA DE MÓDULO"
            elif tier == "adr":
                tier_label = "DECISIÓN ARQUITECTÓNICA (ADR)"
            else:
                tier_label = "GUÍA OPERATIVA Y FEW-SHOTS"

            part = (
                f"--- [RAG CHUNK {i}] [{tier_label}] ---\n"
                f"Autoridad: {authority} | Rule-ID: {rule_id} | Fuente: `{source_citation}`\n"
                f"Criterio: {chunk.get('criterion', 'general')} | Tipo: {chunk.get('chunk_type', 'rule')}\n"
                f"{chunk.get('content', '')}\n"
            )
            formatted_parts.append(part)

        return "\n".join(formatted_parts)

    def search_general(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Búsqueda general transversal sobre toda la base de conocimiento (para chat contextual)."""
        return self.vector_store.search(query=query, top_k=top_k)


# Instancia singleton para reutilización eficiente
_global_retriever: Optional[KnowledgeRetriever] = None


def get_knowledge_retriever() -> KnowledgeRetriever:
    global _global_retriever
    if _global_retriever is None:
        _global_retriever = KnowledgeRetriever()
    return _global_retriever

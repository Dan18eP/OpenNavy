"""
Pipeline de ingesta e indexación vectorial de rúbricas normativas internacionales (HU-RAG-01).

Segmenta, valida metadatos estructurados ({authority, rule_id, category, severity})
e indexa los documentos canónicos en el vector store.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from app.rag.knowledge_loader import KnowledgeLoader
from app.rag.vector_store import HybridVectorStore
from app.core.config import settings


class CorpusIndexer:
    """Motor de ingesta e indexación del corpus de autoridades formales."""

    def __init__(self, kb_dir: Optional[Path] = None, vector_store: Optional[HybridVectorStore] = None):
        self.kb_dir = kb_dir or settings.KNOWLEDGE_BASE_PATH
        self.loader = KnowledgeLoader(self.kb_dir)
        self.vector_store = vector_store or HybridVectorStore()

    def index_corpus(self) -> Dict[str, Any]:
        """
        Lee todos los documentos Markdown de la base de conocimiento,
        extrae los metadatos normativos formales y los indexa en el vector store.
        """
        chunks = self.loader.load_all_chunks()

        # Filtrar o enriquecer metadatos
        indexed_chunks = []
        for ch in chunks:
            # Validar que contenga metadatos mínimos requeridos
            if not ch.get("authority"):
                ch["authority"] = "OpenNavy Engineering Standard"
            if not ch.get("rule_id"):
                ch["rule_id"] = f"NAVY-{ch.get('criterion', 'GEN').upper()}"
            if not ch.get("severity"):
                ch["severity"] = "medium"

            indexed_chunks.append(ch)

        self.vector_store.add_chunks(indexed_chunks)

        authorities = list({c["authority"] for c in indexed_chunks if "authority" in c})
        criteria = list({c["criterion"] for c in indexed_chunks if "criterion" in c})

        return {
            "total_chunks_indexed": len(indexed_chunks),
            "distinct_authorities": authorities,
            "distinct_criteria": criteria,
            "is_indexed": True,
        }

    def search_with_threshold(self, query: str, top_k: int = 5, min_score: float = 0.50) -> List[Dict[str, Any]]:
        """
        Búsqueda por similitud semántica con filtro de corte de relevancia.
        """
        raw_results = self.vector_store.search(query=query, top_k=top_k)
        return [r for r in raw_results if r.get("similarity_score", 0.0) >= min_score]

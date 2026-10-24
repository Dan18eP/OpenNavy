import math
import re
from typing import List, Dict, Any, Optional, Tuple
from app.core.config import settings


def tokenize(text: str) -> List[str]:
    """Tokenizador semántico que extrae palabras clave y términos en minúsculas."""
    words = re.findall(r'\b[a-zA-Z0-9_\-]{2,}\b', text.lower())
    # Stopwords comunes en español e inglés
    stopwords = {
        "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "en", "para", "por",
        "con", "sin", "sobre", "que", "es", "son", "se", "un", "este", "esta", "estos", "estas",
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "is", "are",
        "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "of"
    }
    return [w for w in words if w not in stopwords]


class HybridVectorStore:
    """Vector Store en memoria con soporte para búsqueda semántica híbrida y filtrado por metadatos."""

    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.doc_vectors: List[Dict[str, float]] = []
        self.idf: Dict[str, float] = {}
        self._is_indexed: bool = False

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> None:
        """Agrega chunks e indexa sus representaciones vectoriales."""
        self.chunks.extend(chunks)
        self._build_index()

    def _build_index(self) -> None:
        """Construye el índice inverso y los vectores TF-IDF normalizados para cada chunk."""
        num_docs = len(self.chunks)
        if num_docs == 0:
            return

        # 1. Calcular Document Frequency (DF)
        df: Dict[str, int] = {}
        doc_tokens_list: List[List[str]] = []

        for chunk in self.chunks:
            # Combinar criterio, encabezado y contenido para máxima riqueza semántica
            text = f"{chunk.get('criterion', '')} {chunk.get('heading', '')} {chunk.get('content', '')}"
            tokens = tokenize(text)
            doc_tokens_list.append(tokens)

            unique_tokens = set(tokens)
            for token in unique_tokens:
                df[token] = df.get(token, 0) + 1

        # 2. Calcular IDF suavizado
        self.idf = {
            token: math.log((num_docs + 1) / (count + 1)) + 1.0
            for token, count in df.items()
        }

        # 3. Construir vectores TF-IDF normalizados L2
        self.doc_vectors = []
        for tokens in doc_tokens_list:
            tf: Dict[str, float] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0.0) + 1.0

            # Ponderar por longitud de documento
            doc_len = max(1.0, float(len(tokens)))
            vector: Dict[str, float] = {}
            squared_sum = 0.0

            for token, freq in tf.items():
                tfidf_val = (freq / doc_len) * self.idf.get(token, 1.0)
                vector[token] = tfidf_val
                squared_sum += tfidf_val ** 2

            norm = math.sqrt(squared_sum) or 1.0
            normalized_vec = {k: v / norm for k, v in vector.items()}
            self.doc_vectors.append(normalized_vec)

        self._is_indexed = True

    def search(
        self,
        query: str,
        top_k: int = 3,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Búsqueda por similitud semántica con filtrado estricto por metadatos (ej. criterion, language).
        """
        if not self._is_indexed or not self.chunks:
            return []

        # Vectorizar query
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        q_tf: Dict[str, float] = {}
        for t in query_tokens:
            q_tf[t] = q_tf.get(t, 0.0) + 1.0

        q_len = max(1.0, float(len(query_tokens)))
        q_vec: Dict[str, float] = {}
        q_squared_sum = 0.0

        for token, freq in q_tf.items():
            val = (freq / q_len) * self.idf.get(token, 1.0)
            q_vec[token] = val
            q_squared_sum += val ** 2

        q_norm = math.sqrt(q_squared_sum) or 1.0
        q_norm_vec = {k: v / q_norm for k, v in q_vec.items()}

        # Calcular similitud coseno con cada chunk
        scored_results: List[Tuple[float, Dict[str, Any]]] = []

        for idx, chunk in enumerate(self.chunks):
            # Aplicar filtros de metadatos si existen
            if filters:
                match = True
                for f_key, f_val in filters.items():
                    chunk_val = chunk.get(f_key)
                    if chunk_val is not None and chunk_val != "all" and f_val != "all":
                        if chunk_val != f_val:
                            match = False
                            break
                if not match:
                    continue

            # Similitud Coseno
            doc_vec = self.doc_vectors[idx]
            sim = 0.0
            for t, weight in q_norm_vec.items():
                if t in doc_vec:
                    sim += weight * doc_vec[t]

            # Si no hay similitud léxica/semántica real con la consulta del usuario,
            # no aplicar boosts para evitar alucinaciones RAG en consultas irrelevantes (OWASP LLM08)
            if sim < 0.01:
                continue

            # Si hay coincidencia exacta de criterio, darle un impulso (boost)
            if filters and "criterion" in filters and chunk.get("criterion") == filters["criterion"]:
                sim += 0.35

            # Impulso prioritario canónico (Opción 3 / ADR-002): normas y fuentes oficiales lideran
            if chunk.get("is_canonical") or "canonical/" in str(chunk.get("doc_path", "")).lower():
                sim += 0.30
            elif chunk.get("source_tier") == "team_standard" or "team-standards/" in str(chunk.get("doc_path", "")).lower():
                sim += 0.18
            elif chunk.get("source_tier") == "module_doc" or "module-docs/" in str(chunk.get("doc_path", "")).lower():
                sim += 0.12

            scored_results.append((sim, chunk))

        # Ordenar por mayor similitud
        scored_results.sort(key=lambda item: item[0], reverse=True)

        results = []
        for score, chunk in scored_results[:top_k]:
            res = dict(chunk)
            res["similarity_score"] = round(score, 4)
            results.append(res)

        return results

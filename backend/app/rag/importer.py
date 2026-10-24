"""
Pipeline automatizado de ingesta y conversión de fuentes normativas crudas (PDF, DOCX)
a Markdown estructurado con metadatos canónicos para el RAG de Praxia (ADR-002).
"""

import os
import re
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

try:
    from markitdown import MarkItDown
except ImportError:
    MarkItDown = None

from app.core.config import settings
from app.rag.indexer import CorpusIndexer


class DocumentIngestor:
    """Convierte documentos certificados crudos a Markdown enriquecido con metadatos de auditoría."""

    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".html", ".txt"}

    def __init__(self, raw_dir: Optional[Path] = None, output_dir: Optional[Path] = None):
        base_kb = settings.KNOWLEDGE_BASE_PATH
        self.raw_dir = raw_dir or (base_kb / "raw")
        self.output_dir = output_dir or (base_kb / "canonical")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.md_converter = MarkItDown() if MarkItDown else None

    def ingest_file(self, file_path: Path, metadata_override: Optional[Dict[str, str]] = None) -> Optional[Path]:
        """
        Convierte un archivo individual a Markdown con Frontmatter normativo canónico.
        """
        if not file_path.is_file():
            return None

        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return None

        if not self.md_converter:
            raise RuntimeError(
                "La biblioteca 'markitdown' no está instalada. Ejecute: pip install markitdown"
            )

        # 1. Convertir documento a Markdown utilizando MarkItDown de Microsoft
        conversion_result = self.md_converter.convert(str(file_path))
        extracted_markdown = conversion_result.text_content.strip() if hasattr(conversion_result, "text_content") else str(conversion_result).strip()

        # 2. Construir metadatos canónicos
        meta = self._build_canonical_metadata(file_path, extracted_markdown, metadata_override)

        # 3. Ensamblar documento final con Frontmatter estructurado
        frontmatter = self._render_frontmatter(meta)
        target_name = f"{file_path.stem.lower().replace(' ', '_').replace('-', '_')}.md"
        out_file = self.output_dir / target_name

        combined_content = f"{frontmatter}\n\n{extracted_markdown}\n"
        out_file.write_text(combined_content, encoding="utf-8")

        return out_file

    def ingest_directory(self, reindex_after: bool = False) -> Dict[str, Any]:
        """
        Escanea el directorio raw_dir y procesa todos los archivos compatibles.
        """
        processed_files: List[str] = []
        errors: List[Dict[str, str]] = []

        if not self.raw_dir.exists():
            return {
                "total_processed": 0,
                "processed_files": [],
                "errors": [{"error": f"Directorio {self.raw_dir} no existe."}],
            }

        for item in self.raw_dir.iterdir():
            if item.is_file() and item.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    res_path = self.ingest_file(item)
                    if res_path:
                        processed_files.append(res_path.name)
                except Exception as exc:
                    errors.append({"file": item.name, "error": str(exc)})

        reindex_summary = None
        if reindex_after and processed_files:
            indexer = CorpusIndexer(kb_dir=settings.KNOWLEDGE_BASE_PATH)
            reindex_summary = indexer.index_corpus()

        return {
            "total_processed": len(processed_files),
            "processed_files": processed_files,
            "errors": errors,
            "reindex_summary": reindex_summary,
        }

    def _build_canonical_metadata(
        self,
        file_path: Path,
        content: str,
        override: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        """Infiere o asigna los metadatos de auditoría canónicos."""
        override = override or {}
        stem_lower = file_path.stem.lower()

        # Inferencia de autoridad y norma canónica refinada
        if "25010" in stem_lower:
            authority = "ISO/IEC"
            rule_id = "ISO-25010-2023"
            category = "maintainability"
        elif "5055" in stem_lower:
            authority = "ISO/IEC & CISQ"
            rule_id = "ISO-5055-2021"
            category = "code_quality_and_architecture"
        elif "nist" in stem_lower:
            authority = "NIST / SEI"
            rule_id = "NIST-SP-500-235"
            category = "complexity_and_testing"
        elif "owasp-llm" in stem_lower or "owasp_llm" in stem_lower:
            authority = "OWASP Foundation"
            rule_id = "OWASP-LLM-2025"
            category = "llm_security"
        elif "owasp" in stem_lower:
            authority = "OWASP Foundation"
            rule_id = "OWASP-TOP10-2021"
            category = "security"
        elif "clean" in stem_lower or "solid" in stem_lower:
            authority = "Robert C. Martin (Uncle Bob)"
            rule_id = "CLEAN-ARCH-SOLID"
            category = "architecture"
        elif "fowler" in stem_lower or "refactor" in stem_lower:
            authority = "Martin Fowler"
            rule_id = "FOWLER-REFACTOR"
            category = "refactoring"
        elif "identifying" in stem_lower or "ai-use-cases" in stem_lower or "openai" in stem_lower:
            authority = "OpenAI & Industry Framework"
            rule_id = "AI-OPPORTUNITY-SCALING"
            category = "ai_opportunity"
        else:
            authority = "Recognized Engineering Authority"
            rule_id = f"PRAXIA-{stem_lower.upper()[:12]}"
            category = "general"

        meta = {
            "authority": override.get("authority", authority),
            "rule_id": override.get("rule_id", rule_id),
            "category": override.get("category", category),
            "severity": override.get("severity", "high"),
            "criterion": override.get("criterion", stem_lower.replace("-", "_")),
            "source_file": file_path.name,
            "ingestion_engine": "Microsoft MarkItDown",
            "ingestion_date": datetime.now().strftime("%Y-%m-%d"),
        }
        return meta

    def _render_frontmatter(self, meta: Dict[str, str]) -> str:
        """Renderiza cabecera compatible tanto con YAML como con el parser de Praxia."""
        return (
            f"# Documento Canónico Certificado: {meta.get('criterion', '').upper()}\n\n"
            f"**Autoridad:** {meta['authority']}  \n"
            f"**Rule-ID:** {meta['rule_id']}  \n"
            f"**Categoría:** {meta['category']}  \n"
            f"**Severidad:** {meta['severity']}  \n"
            f"**Identificador:** `{meta['criterion']}`  \n"
            f"**Archivo Fuente Original:** `{meta['source_file']}`  \n"
            f"**Motor de Ingesta:** {meta['ingestion_engine']} ({meta['ingestion_date']})\n\n"
            f"---"
        )


def main():
    parser = argparse.ArgumentParser(description="Ingesta de documentos normativos con MarkItDown")
    parser.add_argument("--raw-dir", type=str, help="Directorio con documentos originales")
    parser.add_argument("--out-dir", type=str, help="Directorio destino para Markdown de criterios")
    parser.add_argument("--reindex", action="store_true", help="Reindexar ChromaDB automáticamente tras la ingesta")
    args = parser.parse_args()

    raw_path = Path(args.raw_dir) if args.raw_dir else None
    out_path = Path(args.out_dir) if args.out_dir else None

    ingestor = DocumentIngestor(raw_dir=raw_path, output_dir=out_path)
    res = ingestor.ingest_directory(reindex_after=args.reindex)
    print(f"[MarkItDown Ingestor] Total procesados: {res['total_processed']}")
    for f in res["processed_files"]:
        print(f" -> {f}")
    if res.get("reindex_summary"):
        print(f"[CorpusIndexer] Re-indexación completada: {res['reindex_summary']}")


if __name__ == "__main__":
    main()

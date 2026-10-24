import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.core.config import settings, PROJECT_ROOT


class KnowledgeLoader:
    """Carga y segmenta semánticamente los documentos Markdown de la base de conocimiento."""

    def __init__(self, knowledge_base_dir: Optional[Path] = None):
        self.kb_dir = knowledge_base_dir or settings.KNOWLEDGE_BASE_PATH

    def load_all_chunks(self) -> List[Dict[str, Any]]:
        """
        Escanea todos los subdirectorios de la base de conocimiento (criteria, team-standards, adrs, module-docs)
        y genera chunks semánticos estructurados con metadatos.
        """
        chunks: List[Dict[str, Any]] = []
        if self.kb_dir.exists():
            for md_file in self.kb_dir.rglob("*.md"):
                if md_file.is_file():
                    file_chunks = self.process_markdown_file(md_file)
                    chunks.extend(file_chunks)

        # Cargar ADRs y arquitectura central de OpenNavy
        adr_dir = PROJECT_ROOT / "docs" / "adr"
        if adr_dir.exists():
            for md_file in adr_dir.glob("*.md"):
                if md_file.is_file():
                    chunks.extend(self.process_markdown_file(md_file))

        arch_file = PROJECT_ROOT / "docs" / "ARCHITECTURE.md"
        if arch_file.exists() and arch_file.is_file():
            chunks.extend(self.process_markdown_file(arch_file))

        return chunks

    def process_markdown_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Segmenta un archivo Markdown en chunks basados en secciones semánticas (#, ##, ###)."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return []

        try:
            rel_path = str(file_path.relative_to(self.kb_dir)).replace("\\", "/")
        except ValueError:
            try:
                rel_path = str(file_path.relative_to(PROJECT_ROOT)).replace("\\", "/")
            except Exception:
                rel_path = file_path.name

        # 1. Extraer Metadatos del Encabezado
        doc_metadata = self._extract_metadata(content)
        criterion = doc_metadata.get("criterion", file_path.stem.replace("-", "_"))
        category = doc_metadata.get("category", "general")

        # 2. Dividir por Secciones de Encabezados Markdown
        sections = self._split_by_headings(content)
        chunks: List[Dict[str, Any]] = []

        for i, sec in enumerate(sections):
            heading = sec.get("heading", "General")
            section_body = sec.get("body", "").strip()

            if not section_body or len(section_body) < 20:
                continue

            # Determinar tipo semántico del chunk
            chunk_type = self._infer_chunk_type(heading, section_body)

            # Extraer lenguaje aplicable si se menciona
            language = "all"
            if "python" in heading.lower() or "python" in section_body[:50].lower():
                language = "python"
            elif "typescript" in heading.lower() or "javascript" in heading.lower():
                language = "typescript"

            chunk_id = f"{criterion}#{heading.lower().replace(' ', '_').replace('/', '_')}_{i}"
            path_lower = rel_path.lower()
            is_canonical = "canonical/" in path_lower

            if is_canonical:
                source_tier = "canonical"
            elif "team-standards/" in path_lower:
                source_tier = "team_standard"
            elif "module-docs/" in path_lower:
                source_tier = "module_doc"
            elif "adrs/" in path_lower or "adr/" in path_lower or "architecture" in path_lower:
                source_tier = "adr"
            elif "criteria/" in path_lower:
                source_tier = "criteria"
            else:
                source_tier = "general"

            chunks.append({
                "chunk_id": chunk_id,
                "doc_path": rel_path,
                "criterion": criterion,
                "category": category,
                "authority": doc_metadata.get("authority", "OpenNavy Standards"),
                "rule_id": doc_metadata.get("rule_id", f"NAVY-{criterion.upper()}"),
                "severity": doc_metadata.get("severity", "medium"),
                "heading": heading,
                "chunk_type": chunk_type,
                "language_applicable": language,
                "is_canonical": is_canonical,
                "source_tier": source_tier,
                "content": f"### {heading}\n{section_body}",
                "raw_text": f"{criterion} - {heading}: {section_body}",
            })

        return chunks


    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """Extrae identificadores y metadatos clave del inicio del archivo Markdown."""
        meta = {}
        for line in content.splitlines()[:25]:
            if "**Identificador:**" in line:
                meta["criterion"] = line.split("**Identificador:**")[1].replace("`", "").strip()
            elif "**Categoría:**" in line:
                meta["category"] = line.split("**Categoría:**")[1].strip()
            elif "**Tipo:**" in line:
                meta["type"] = line.split("**Tipo:**")[1].strip()
            elif "**Autoridad:**" in line:
                meta["authority"] = line.split("**Autoridad:**")[1].strip()
            elif "**Rule-ID:**" in line:
                meta["rule_id"] = line.split("**Rule-ID:**")[1].strip()
            elif "**Severidad:**" in line:
                meta["severity"] = line.split("**Severidad:**")[1].strip()
        return meta


    def _split_by_headings(self, content: str) -> List[Dict[str, str]]:
        """Divide el texto Markdown respetando los bloques de encabezados nivel 1, 2 y 3."""
        lines = content.splitlines()
        sections: List[Dict[str, str]] = []
        current_heading = "Introducción"
        current_lines: List[str] = []

        heading_pattern = re.compile(r'^(#{1,3})\s+(.*)$')

        for line in lines:
            match = heading_pattern.match(line)
            if match:
                if current_lines:
                    sections.append({
                        "heading": current_heading,
                        "body": "\n".join(current_lines),
                    })
                    current_lines = []
                current_heading = match.group(2).strip()
            else:
                current_lines.append(line)

        if current_lines:
            sections.append({
                "heading": current_heading,
                "body": "\n".join(current_lines),
            })

        return sections

    def _infer_chunk_type(self, heading: str, body: str) -> str:
        """Infiere si el chunk es una regla, umbral, ejemplo, definición o refactor."""
        h_lower = heading.lower()
        b_lower = body.lower()

        if any(w in h_lower for w in ["umbral", "rango", "clasificación", "severidad"]):
            return "threshold"
        if any(w in h_lower for w in ["ejemplo", "violación", "contraejemplo"]):
            return "example"
        if any(w in h_lower for w in ["refactor", "solución", "corrección", "estrategia"]):
            return "refactoring"
        if any(w in h_lower for w in ["definición", "visión general", "propósito", "fundamento"]):
            return "definition"
        if any(w in h_lower for w in ["regla", "principio", "directriz", "estándar"]):
            return "rule"

        if "```" in body:
            return "example"
        return "guideline"

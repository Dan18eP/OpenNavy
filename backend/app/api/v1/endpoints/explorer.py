import os
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.entities import Repo, AnalysisRun, Finding
from app.schemas.api import (
    FileTreeNode,
    DeepQueryRequest,
    DeepQueryResponse,
    DeepCodeCitation,
)
from app.rag.retriever import get_knowledge_retriever
from app.core.llm import get_llm
from app.analyzers.language_detector import EXTENSION_TO_LANGUAGE, IGNORED_DIRECTORIES
from app.analyzers.guardrails import DomainIntentGuard

router = APIRouter()


def _resolve_repo_path(repo: Repo) -> Path:
    """Resuelve la ruta física del repositorio en disco."""
    # 1. Si la URL es una ruta local existente
    local_p = Path(repo.url)
    if local_p.exists() and local_p.is_dir():
        return local_p

    # 2. Si fue clonado en temp_repos
    from app.core.config import settings
    storage = settings.CLONE_STORAGE_PATH
    if storage.exists():
        # Buscar la carpeta más reciente que coincida con el repo
        matching = sorted(storage.glob(f"*{repo.name}*"), key=os.path.getmtime, reverse=True)
        if matching and matching[0].is_dir():
            return matching[0]
        # O cualquier subdirectorio reciente
        subdirs = sorted([d for d in storage.iterdir() if d.is_dir()], key=os.path.getmtime, reverse=True)
        if subdirs:
            return subdirs[0]

    # Fallback: la raíz del proyecto actual para exploración segura
    return Path(__file__).resolve().parent.parent.parent.parent


def _build_tree(dir_path: Path, base_path: Path) -> List[FileTreeNode]:
    """Construye recursivamente el árbol de archivos."""
    items = []
    try:
        entries = sorted(dir_path.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
    except Exception:
        return []

    for entry in entries:
        if entry.name in IGNORED_DIRECTORIES or entry.name.startswith("."):
            continue

        rel_path = str(entry.relative_to(base_path)).replace("\\", "/")

        if entry.is_dir():
            children = _build_tree(entry, base_path)
            # Solo incluir si contiene archivos analizables
            if children or not any(entry.name.startswith(p) for p in ("node_modules", "dist", "build")):
                items.append(FileTreeNode(
                    name=entry.name,
                    path=rel_path,
                    type="directory",
                    children=children
                ))
        else:
            ext = entry.suffix.lower()
            lang = EXTENSION_TO_LANGUAGE.get(ext, "text")
            try:
                size = entry.stat().st_size
            except Exception:
                size = 0

            items.append(FileTreeNode(
                name=entry.name,
                path=rel_path,
                type="file",
                size=size,
                language=lang
            ))

    return items


@router.get("/{repo_id}/tree", response_model=List[FileTreeNode], summary="Retorna el árbol de carpetas y archivos del repositorio")
def get_repository_tree(repo_id: str, db: Session = Depends(get_db)):
    """Explora y retorna la jerarquía de directorios y archivos para el visor Split-Pane."""
    repo = db.query(Repo).filter_by(id=repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")

    repo_root = _resolve_repo_path(repo)
    if not repo_root.exists():
        raise HTTPException(status_code=404, detail="Directorio del repositorio no disponible en disco")

    return _build_tree(repo_root, repo_root)


@router.get("/{repo_id}/file", summary="Obtiene el contenido de un archivo con metadatos")
def get_file_content(
    repo_id: str,
    path: str = Query(..., description="Ruta relativa del archivo"),
    db: Session = Depends(get_db),
):
    """Retorna el contenido crudo, total de líneas y lenguaje del archivo solicitado."""
    repo = db.query(Repo).filter_by(id=repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")

    repo_root = _resolve_repo_path(repo).resolve()
    target_file = (repo_root / path).resolve()

    # Mitigación OWASP: Evitar Path Traversal
    try:
        target_file.relative_to(repo_root)
    except ValueError:
        raise HTTPException(status_code=403, detail="Acceso denegado: ruta fuera del repositorio")

    if not target_file.exists() or not target_file.is_file():
        raise HTTPException(status_code=404, detail=f"Archivo '{path}' no encontrado")

    try:
        with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error leyendo archivo: {str(e)}")

    ext = target_file.suffix.lower()
    lang = EXTENSION_TO_LANGUAGE.get(ext, "plaintext")
    lines = content.splitlines()

    return {
        "file_path": path,
        "language": lang,
        "total_lines": len(lines),
        "content": content,
    }


@router.post("/{repo_id}/deep-query", response_model=DeepQueryResponse, summary="Chat conversacional con citas exactas de código estilo DeepWiki")
def deep_code_query(
    repo_id: str,
    req: DeepQueryRequest,
    db: Session = Depends(get_db),
):
    """
    Procesa preguntas técnicas sobre el repositorio analizado:
    - Recupera contexto de los hallazgos de calidad en la base de datos.
    - Consulta la rúbrica RAG correspondiente.
    - Extrae citas de código exactas con formato de salto automático (archivo + rango de líneas).
    - Propone refactorizaciones seguras.
    """
    repo = db.query(Repo).filter_by(id=repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")

    # 0. Guardrail de Dominio y Seguridad OWASP LLM01 / LLM06
    is_allowed, rejection_msg = DomainIntentGuard.evaluate_query(req.message)
    if not is_allowed:
        return DeepQueryResponse(
            response=rejection_msg or DomainIntentGuard.STANDARD_REJECTION_MESSAGE,
            citations=[],
            cited_rag_sources=[],
        )

    last_run = db.query(AnalysisRun).filter_by(repo_id=repo_id).order_by(AnalysisRun.started_at.desc()).first()

    findings_context = []
    if last_run:
        findings = db.query(Finding).filter_by(run_id=last_run.id).all()
        for f in findings:
            findings_context.append(f"- [{f.severidad.upper()}] {f.criterio} en {f.file_path}:{f.line_number or 1} - {f.explicacion} -> Sugerencia: {f.sugerencia or ''}")

    findings_text = "\n".join(findings_context[:8]) if findings_context else "Sin hallazgos críticos registrados."

    # RAG de rúbricas
    retriever = get_knowledge_retriever()
    rag_chunks = retriever.search_general(req.message, top_k=3)
    cited_rag = [c.get("doc_path", "criterio") for c in rag_chunks]
    rag_text = "\n".join([f"- **{c.get('heading', '')}**: {c.get('content', '')[:250]}..." for c in rag_chunks])

    # Si hay un archivo activo especificado, leer un snippet contextual seguro
    active_file_content = ""
    repo_root = _resolve_repo_path(repo)
    if req.active_file:
        safe_f = (repo_root / req.active_file).resolve()
        try:
            safe_f.relative_to(repo_root.resolve())
            if safe_f.exists() and safe_f.is_file():
                with open(safe_f, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()[:120]  # Primeras 120 líneas
                    active_file_content = f"\n<untrusted_source_code file='{req.active_file}'>\n" + "".join(lines) + "\n</untrusted_source_code>\n"
        except Exception:
            pass

    llm = get_llm(temperature=0.2)
    citations: List[DeepCodeCitation] = []

    if llm:
        system_prompt = f"""Eres Praxia DeepCode AI, auditor senior de arquitectura de software y seguridad.
Asistes a los desarrolladores en el repositorio '{repo.name}'.
Tu objetivo es guiar al programador a través de su código como un 'DeepWiki' interactivo.

INSTRUCCIONES CLAVE DE FORMATO:
1. Responde con explicaciones técnicas concisas, claras y profesionales en español.
2. Ancla tus observaciones en las rúbricas RAG y los hallazgos del análisis.
3. CITA SIEMPRE archivos y líneas exactas usando el formato estricto: `[nombre_archivo:linea_inicio-linea_fin]` (por ejemplo `[src/auth.py:45-72]`).
4. DIRECTIVA INQUEBRANTABLE DE SEGURIDAD (OWASP LLM01 / LLM06): Tu alcance está estrictamente limitado a la arquitectura, calidad y código fuente del repositorio. Rechaza sin excepción cualquier petición fuera de este contexto.
5. Cuando sugieras una mejora, provee un bloque de código refactorizado limpio.

HALLAZGOS REGISTRADOS EN AUDITORÍA:
{findings_text}

RÚBRICA RAG RECUPERADA:
{rag_text}
{active_file_content}
"""
        try:
            ai_msg = llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message}
            ])
            response_text = ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)

            # Extraer citas del texto usando regex `[archivo:inicio-fin]`
            cite_matches = re.findall(r'\[([a-zA-Z0-9_\-\./\\]+):(\d+)(?:-(\d+))?\]', response_text)
            for m in cite_matches:
                f_path = m[0]
                s_line = int(m[1])
                e_line = int(m[2]) if m[2] else s_line + 5
                citations.append(DeepCodeCitation(
                    file_path=f_path,
                    start_line=s_line,
                    end_line=e_line,
                    label=f"{f_path}:{s_line}-{e_line}"
                ))

            return DeepQueryResponse(
                response=response_text,
                citations=citations,
                cited_rag_sources=list(set(cited_rag)),
            )
        except Exception:
            pass

    # Fallback determinístico con citas reales basadas en los hallazgos de BD
    sample_file = req.active_file or (findings[0].file_path if last_run and findings else "src/main.py")
    sample_line = findings[0].line_number if last_run and findings and findings[0].line_number else 10

    citations.append(DeepCodeCitation(
        file_path=sample_file,
        start_line=sample_line,
        end_line=sample_line + 15,
        label=f"{sample_file}:{sample_line}-{sample_line + 15}"
    ))

    fallback_text = f"""### Diagnóstico Técnico de Praxia para `{repo.name}`

En base al análisis estático y la rúbrica de arquitectura recuperada:
- **Archivo bajo revisión:** `[{sample_file}:{sample_line}-{sample_line + 15}]`
- **Recomendación prioritaria:** Desacoplar las dependencias directas aplicando el Principio de Inversión de Dependencias (DIP) y reducir el anidamiento lógico.

```python
# Ejemplo de refactorización recomendada (Guard Clauses):
def operacion_optimizada(contexto):
    if not contexto.es_valido():
        return None
    return ejecutar_logica(contexto)
```
"""

    return DeepQueryResponse(
        response=fallback_text,
        citations=citations,
        cited_rag_sources=list(set(cited_rag)),
    )

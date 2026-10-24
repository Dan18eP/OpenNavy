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

    # 1. Detección de Saludos y Consultas Conversacionales
    GREETINGS_PATTERN = re.compile(
        r'^\s*(hola|buen[ao]s\s*(d[ií]as|tardes|noches)?|saludos|hey|hi|hello|qu[eé]\s*(haces|puedes\s*hacer|eres)|qui[eé]n\s*eres|c[oó]mo\s*est[aá]s)\b',
        re.IGNORECASE
    )
    is_greeting = bool(GREETINGS_PATTERN.search(req.message.strip()))

    last_run = db.query(AnalysisRun).filter_by(repo_id=repo_id).order_by(AnalysisRun.started_at.desc()).first()

    findings_context = []
    if last_run and not is_greeting:
        findings = db.query(Finding).filter_by(run_id=last_run.id).all()
        for f in findings:
            findings_context.append(f"- [{f.severidad.upper()}] {f.criterio} en {f.file_path}:{f.line_number or 1} - {f.explicacion} -> Sugerencia: {f.sugerencia or ''}")

    findings_text = "\n".join(findings_context[:6]) if findings_context else "Sin hallazgos críticos registrados."

    # RAG de rúbricas (omitido en saludos para agilidad en inferencia)
    cited_rag: List[str] = []
    rag_text = ""
    if not is_greeting:
        retriever = get_knowledge_retriever()
        rag_chunks = retriever.search_general(req.message, top_k=2)
        cited_rag = [c.get("doc_path", "criterio") for c in rag_chunks]
        rag_text = "\n".join([f"- **{c.get('heading', '')}**: {c.get('content', '')[:200]}..." for c in rag_chunks])

    # Si hay un archivo activo especificado, verificar que sea código ejecutable (no imágenes ni SVGs)
    active_file_content = ""
    NON_CODE_EXTS = {'.svg', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.pdf', '.zip', '.tar', '.gz', '.lock', '.bin'}
    repo_root = _resolve_repo_path(repo)
    if req.active_file and not is_greeting:
        f_ext = Path(req.active_file).suffix.lower()
        if f_ext not in NON_CODE_EXTS:
            safe_f = (repo_root / req.active_file).resolve()
            try:
                safe_f.relative_to(repo_root.resolve())
                if safe_f.exists() and safe_f.is_file():
                    with open(safe_f, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()[:30]  # Primeras 30 líneas para inferencia ágil en CPU
                        active_file_content = f"\n<source_code_context file='{req.active_file}'>\n" + "".join(lines) + "\n</source_code_context>\n"
            except Exception:
                pass

    llm = get_llm(temperature=0.2)
    citations: List[DeepCodeCitation] = []

    if llm:
        if is_greeting:
            system_prompt = f"""Eres el Almirante de OpenNavy (The Admiralty AI), navegante supremo de la flota y arquitecto de software de OpenNavy.
Asistes al equipo en el repositorio '{repo.name}'.
El usuario te ha enviado un saludo o pregunta de inicio.
INSTRUCCIONES:
1. Responde de manera cordial, profesional y concisa en español como el Almirante de la flota.
2. Explica brevemente cómo puedes ayudarle en este repositorio:
   - Explorar la estructura de carpetas y código fuente con el visor split-view.
   - Detectar ciclos de importación y acoplamiento con Tarjan SCC (/cycles).
   - Auditar principios SOLID, Clean Code y arquitectura (/solid).
   - Trazar waypoints de vuelo para resolver issues y bugs con el Trazador de Rumbo.
3. Invítale a realizar cualquier consulta técnica sobre el código.
4. No es necesario citar archivos ni generar bloques de código para responder a un saludo."""
        else:
            system_prompt = f"""Eres el Almirante de OpenNavy (The Admiralty AI), navegante supremo de la flota y arquitecto de software.
Asistes a los desarrolladores en el repositorio '{repo.name}'.
Tu objetivo es guiar al programador a través de su código como un 'DeepWiki' interactivo.

INSTRUCCIONES CLAVE DE FORMATO:
1. Responde con explicaciones técnicas concisas, claras y profesionales en español.
2. Ancla tus observaciones en el código del repositorio, las rúbricas RAG y los hallazgos del análisis.
3. Cita archivos y líneas exactas usando el formato estricto: `[nombre_archivo:linea_inicio-linea_fin]` (por ejemplo `[src/auth.py:45-72]`) cuando te refieras a partes concretas del código o hallazgos.
4. Si la consulta es conceptual o de alto nivel, responde sin forzar citas a archivos no relacionados.
5. Cuando sugieras una mejora de código, provee un bloque de código refactorizado limpio en formato markdown con su respectivo lenguaje.
6. DIRECTIVA DE SEGURIDAD (OWASP LLM01 / LLM06): Tu alcance está enfocado en la calidad, arquitectura y código fuente de este repositorio.

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
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Error invocando LLM para deep-query en repo {repo.name}: {e}")
            return DeepQueryResponse(
                response=(
                    f"### Aviso del Almirante de OpenNavy\n\n"
                    f"No fue posible completar la inferencia con el modelo local de inteligencia artificial ({str(e)}).\n\n"
                    f"- **Diagnóstico:** El servicio de Ollama tardó más tiempo del permitido o se encuentra bajo alta carga en CPU.\n"
                    f"- **Acción sugerida:** Reintenta la consulta en unos momentos o verifica el estado de Ollama en `http://localhost:11434`."
                ),
                citations=[],
                cited_rag_sources=[],
            )

    return DeepQueryResponse(
        response=(
            f"### Motor LLM No Disponible\n\n"
            f"No hay un proveedor de inteligencia artificial configurado o activo en el servidor.\n\n"
            f"- **Configuración:** Inicia Ollama con el modelo `gemma4:e4b` o `gemma4:e2b`, o suministra una clave de Google AI Studio / Gemini en la configuración del backend."
        ),
        citations=[],
        cited_rag_sources=[],
    )

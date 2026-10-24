import asyncio
import json
import time
from typing import Dict, Any
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db, SessionLocal
from app.models.entities import Repo, AnalysisRun, TriggerType, RunStatus
from app.schemas.api import (
    AnalysisCreateRequest,
    AnalysisJobResponse,
    AnalysisRunDetailResponse,
)
from app.agents.graph import praxia_graph

from app.core.event_channel import get_or_create_channel, remove_channel, SSEProgressEvent

router = APIRouter()

# Diccionario de retrocompatibilidad
job_progress_events: Dict[str, list] = {}


def run_analysis_task(run_id: str, repo_id: str, repo_url: str, branch: str):
    """Tarea en segundo plano que ejecuta el grafo de LangGraph y emite eventos en tiempo real."""
    channel = get_or_create_channel(str(run_id))

    channel.emit_sync(
        node="clone",
        status="in_progress",
        progress_percent=15,
        message="Clonando repositorio...",
    )
    job_progress_events[str(run_id)] = [
        {"step": "cloning", "progress": 15, "message": "Clonando repositorio...", "timestamp": time.time()}
    ]

    initial_state = {
        "run_id": str(run_id),
        "repo_id": str(repo_id),
        "repo_url": repo_url,
        "branch": branch,
        "local_path": "",
        "languages_detected": [],
        "files": [],
        "static_metrics": {},
        "complexity_findings": [],
        "solid_violations": [],
        "architecture_diff": None,
        "rag_context": [],
        "evaluation_report": {},
        "generated_docs": [],
        "errors": [],
        "retry_count": 0,
        "current_step": "init",
    }

    try:
        channel.emit_sync(
            node="static_analysis",
            status="in_progress",
            progress_percent=40,
            message="Calculando AST, Complejidad Ciclomática y Duplicación...",
        )
        job_progress_events[str(run_id)].append({
            "step": "static_analysis",
            "progress": 40,
            "message": "Calculando AST, Complejidad Ciclomática y Duplicación...",
            "timestamp": time.time(),
        })

        # Invocar StateGraph de LangGraph
        result = praxia_graph.invoke(initial_state)

        channel.emit_sync(
            node="rag_evaluation",
            status="in_progress",
            progress_percent=80,
            message="Evaluando principios SOLID, Clean Code y arquitectura con RAG...",
        )
        job_progress_events[str(run_id)].append({
            "step": "rag_evaluation",
            "progress": 80,
            "message": "Evaluando principios SOLID, Clean Code y arquitectura con RAG...",
            "timestamp": time.time(),
        })

        global_score = result.get("evaluation_report", {}).get("global_score", 0.0)
        channel.emit_sync(
            node="completed",
            status="completed",
            progress_percent=100,
            message="Análisis finalizado con éxito.",
            partial_data={"global_score": global_score},
        )
        job_progress_events[str(run_id)].append({
            "step": "completed",
            "progress": 100,
            "message": "Análisis finalizado con éxito.",
            "global_score": global_score,
            "timestamp": time.time(),
        })
    except Exception as e:
        channel.emit_sync(
            node="failed",
            status="failed",
            progress_percent=100,
            message=f"Error en análisis: {str(e)}",
        )
        job_progress_events[str(run_id)].append({
            "step": "failed",
            "progress": 100,
            "message": f"Error en análisis: {str(e)}",
            "timestamp": time.time(),
        })
        db = SessionLocal()
        try:
            run = db.query(AnalysisRun).filter_by(id=run_id).first()
            if run:
                run.status = RunStatus.FAILED.value
                run.error_message = str(e)
                db.commit()
        finally:
            db.close()


@router.post("/analyze", response_model=AnalysisJobResponse, summary="Disparar análisis de repositorio")
def trigger_analysis(
    req: AnalysisCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Crea un job de análisis asíncrono y lo ejecuta en segundo plano con LangGraph."""
    # 1. Crear o recuperar Repo
    repo = db.query(Repo).filter_by(url=req.repo_url).first()
    if not repo:
        raw_target = req.repo_url.rstrip("/\\")
        from pathlib import Path
        name = Path(raw_target).name or raw_target.split("/")[-1].replace(".git", "") or "repositorio"
        repo = Repo(
            url=req.repo_url,
            name=name,
            default_branch=req.branch or "main",
        )
        db.add(repo)

        db.commit()
        db.refresh(repo)

    # 2. Crear AnalysisRun en estado PENDING
    run = AnalysisRun(
        repo_id=repo.id,
        branch=req.branch or "main",
        triggered_by=TriggerType.MANUAL.value,
        status=RunStatus.PENDING.value,
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    # 3. Lanzar tarea en segundo plano
    background_tasks.add_task(
        run_analysis_task,
        run.id,
        repo.id,
        req.repo_url,
        req.branch or "main",
    )

    return AnalysisJobResponse(
        job_id=run.id,
        repo_id=repo.id,
        status=RunStatus.PENDING.value,
        message="Análisis encolado y en ejecución.",
    )


@router.get("/analyze/{job_id}/stream", summary="Streaming SSE en tiempo real del progreso de análisis")
async def stream_analysis_progress(job_id: str, db: Session = Depends(get_db)):
    """Transmite eventos SSE (Server-Sent Events) reactivos vía asyncio.Queue con el estado en vivo del pipeline."""
    channel = get_or_create_channel(str(job_id))

    async def event_generator():
        timeout = 60.0
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Esperar nuevo evento en la cola asíncrona
                event: Optional[SSEProgressEvent] = await asyncio.wait_for(channel.queue.get(), timeout=1.0)
                if event is None:
                    break

                yield f"data: {event.model_dump_json()}\n\n"

                if event.status in ("completed", "failed") or event.node in ("completed", "failed"):
                    break
            except asyncio.TimeoutError:
                # Comprobar si la corrida ya terminó en base de datos
                run = db.query(AnalysisRun).filter_by(id=job_id).first()
                if run and run.status == RunStatus.COMPLETED.value:
                    fallback_event = SSEProgressEvent(
                        node="completed",
                        status="completed",
                        progress_percent=100,
                        message="Análisis completado.",
                        partial_data={"global_score": run.global_score},
                        timestamp=time.time(),
                    )
                    yield f"data: {fallback_event.model_dump_json()}\n\n"
                    break

        await asyncio.sleep(0.1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/{repo_id}/stream", summary="Streaming SSE por repo_id para el cliente web")
async def stream_analysis_by_repo(repo_id: str, db: Session = Depends(get_db)):
    """Permite al cliente web suscribirse al stream SSE del último análisis ejecutado para el repositorio."""
    last_run = (
        db.query(AnalysisRun)
        .filter_by(repo_id=repo_id)
        .order_by(AnalysisRun.started_at.desc())
        .first()
    )
    if not last_run:
        raise HTTPException(status_code=404, detail="No hay análisis registrados para este repositorio")

    return await stream_analysis_progress(str(last_run.id), db)


@router.get("/runs/{run_id}", response_model=AnalysisRunDetailResponse, summary="Obtener detalle de una corrida")
def get_run_detail(run_id: str, db: Session = Depends(get_db)):
    run = db.query(AnalysisRun).filter_by(id=run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Corrida de análisis no encontrada")
    return run

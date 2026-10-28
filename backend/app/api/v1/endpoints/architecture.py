from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.entities import Repo, AnalysisRun, ArchitectureDiff, GeneratedDoc
from app.services.anti_drift_service import anti_drift_service

router = APIRouter()


class DriftEvaluationRequest(BaseModel):
    waypoints: List[Dict[str, Any]] = Field(..., description="Lista de waypoints a evaluar")


@router.get("/{repo_id}/architecture", summary="Obtener analisis y grafo de arquitectura")
def get_architecture_summary(repo_id: str, db: Session = Depends(get_db)):
    """Retorna el resumen arquitectonico, dependencias circulares y violaciones de capas."""
    repo = db.query(Repo).filter_by(id=repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")

    last_run = (
        db.query(AnalysisRun)
        .filter_by(repo_id=repo_id)
        .order_by(AnalysisRun.started_at.desc())
        .first()
    )

    if not last_run:
        return {"repo_id": repo_id, "architecture": None}

    arch = db.query(ArchitectureDiff).filter_by(run_id=last_run.id).first()

    return {
        "repo_id": repo_id,
        "run_id": last_run.id,
        "resumen": arch.resumen if arch else "Sin datos arquitectonicos.",
        "ciclos_detectados": arch.ciclos_detectados if arch else [],
        "has_circular_dependencies": len(arch.ciclos_detectados) > 0 if arch else False,
        "dependencias_nuevas": arch.dependencias_nuevas if arch else [],
        "dependencias_rotas": arch.dependencias_rotas if arch else [],
    }


@router.get("/{repo_id}/knowledge", summary="Documentacion viva y ADRs generados")
def get_generated_knowledge(repo_id: str, db: Session = Depends(get_db)):
    """Retorna los Architecture Decision Records (ADRs) y resumenes autogenerados."""
    docs = db.query(GeneratedDoc).filter_by(repo_id=repo_id).order_by(GeneratedDoc.created_at.desc()).all()

    return {
        "repo_id": repo_id,
        "total_documents": len(docs),
        "documents": [
            {
                "id": d.id,
                "tipo": d.tipo,
                "path": d.path,
                "titulo": d.titulo,
                "contenido": d.contenido,
                "created_at": d.created_at,
            }
            for d in docs
        ],
    }


@router.get("/{repo_id}/topography", summary="Topografia AST y Arrecifes de Tarjan en tiempo real")
def get_repo_topography(repo_id: str, db: Session = Depends(get_db)):
    """
    Retorna la Carta Nautica en tiempo real: arbol de archivos AST, simbolos principales
    y ciclos de acoplamiento fuerte (Arrecifes de Tarjan) calculados en <1 segundo.
    """
    repo = db.query(Repo).filter_by(id=repo_id).first()
    repo_name = repo.name if repo else "OpenSource-Repo"

    workspace_root = Path(".").resolve()
    repo_dir = str(workspace_root)
    if repo and Path(repo.url).exists():
        repo_dir = str(Path(repo.url).resolve())

    topography = anti_drift_service.get_repo_ast_topography(repo_dir, max_files=50)

    return {
        "repo_id": repo_id,
        "repo_name": repo_name,
        "repo_dir": repo_dir,
        "total_modules": topography.get("total_modules", 0),
        "files": topography.get("files", []),
        "symbols": topography.get("symbols", {}),
        "scc_cycles": topography.get("scc_cycles", []),
        "adjacency": topography.get("adjacency", {}),
    }


@router.post("/{repo_id}/drift/evaluate", summary="Evaluar riesgo de deriva arquitectonica")
def evaluate_drift(
    repo_id: str,
    payload: DriftEvaluationRequest,
    db: Session = Depends(get_db),
):
    """
    Ejecuta el Motor Anti Code Drift sobre un conjunto de waypoints propuestos,
    calculando el radio de impacto (Blast Radius), advertencias de arrecifes y recomendacion ADR.
    """
    repo = db.query(Repo).filter_by(id=repo_id).first()
    repo_name = repo.name if repo else "OpenSource-Repo"

    workspace_root = Path(".").resolve()
    repo_dir = str(workspace_root)
    if repo and Path(repo.url).exists():
        repo_dir = str(Path(repo.url).resolve())

    result = anti_drift_service.evaluate_course_drift(repo_name, payload.waypoints, repo_dir)
    return {
        "repo_id": repo_id,
        "repo_name": repo_name,
        "evaluation": result,
    }

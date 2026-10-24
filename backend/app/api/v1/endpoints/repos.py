from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import Repo, AnalysisRun
from app.schemas.api import RepoCreate, RepoResponse

router = APIRouter()


@router.post("/", response_model=RepoResponse, summary="Registrar o conectar un repositorio")
def create_repo(repo_in: RepoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo repositorio para monitoreo y análisis."""
    existing = db.query(Repo).filter_by(url=repo_in.url).first()
    if existing:
        return existing

    name = repo_in.name
    if not name:
        raw_target = repo_in.url.rstrip("/\\")
        from pathlib import Path
        name = Path(raw_target).name or raw_target.split("/")[-1].replace(".git", "") or "repositorio"


    repo = Repo(
        url=repo_in.url,
        name=name,
        default_branch=repo_in.default_branch or "main",
    )
    db.add(repo)
    db.commit()
    db.refresh(repo)
    return repo


@router.get("/", summary="Listar todos los repositorios vigilados")
def list_repos(db: Session = Depends(get_db)):
    """Retorna la lista de repositorios vigilados junto con el score del último análisis."""
    repos = db.query(Repo).order_by(Repo.connected_at.desc()).all()
    results = []
    for r in repos:
        last_run = (
            db.query(AnalysisRun)
            .filter_by(repo_id=r.id)
            .order_by(AnalysisRun.started_at.desc())
            .first()
        )
        results.append({
            "id": r.id,
            "url": r.url,
            "name": r.name,
            "default_branch": r.default_branch,
            "connected_at": r.connected_at,
            "last_run_status": last_run.status if last_run else None,
            "last_global_score": last_run.global_score if last_run else None,
            "last_analyzed_at": last_run.finished_at if last_run else None,
        })
    return results


@router.get("/{repo_id}", response_model=RepoResponse, summary="Obtener detalle de un repositorio")
def get_repo(repo_id: str, db: Session = Depends(get_db)):
    repo = db.query(Repo).filter_by(id=repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")
    return repo


@router.delete("/{repo_id}", summary="Eliminar un repositorio y todos sus análisis asociados")
def delete_repo(repo_id: str, db: Session = Depends(get_db)):
    """Elimina permanentemente un repositorio y todos sus datos en cascada (runs, métricas, hallazgos, docs)."""
    repo = db.query(Repo).filter_by(id=repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")

    repo_name = repo.name
    db.delete(repo)
    db.commit()

    return {
        "success": True,
        "message": f"Repositorio '{repo_name}' eliminado correctamente junto con todos sus análisis.",
        "repo_id": repo_id,
    }


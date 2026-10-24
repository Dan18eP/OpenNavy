from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.entities import Repo, AnalysisRun, ArchitectureDiff, GeneratedDoc

router = APIRouter()


@router.get("/{repo_id}/architecture", summary="Obtener análisis y grafo de arquitectura")
def get_architecture_summary(repo_id: str, db: Session = Depends(get_db)):
    """Retorna el resumen arquitectónico, dependencias circulares y violaciones de capas."""
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
        "resumen": arch.resumen if arch else "Sin datos arquitectónicos.",
        "ciclos_detectados": arch.ciclos_detectados if arch else [],
        "has_circular_dependencies": len(arch.ciclos_detectados) > 0 if arch else False,
        "dependencias_nuevas": arch.dependencias_nuevas if arch else [],
        "dependencias_rotas": arch.dependencias_rotas if arch else [],
    }


@router.get("/{repo_id}/knowledge", summary="Documentación viva y ADRs generados")
def get_generated_knowledge(repo_id: str, db: Session = Depends(get_db)):
    """Retorna los Architecture Decision Records (ADRs) y resúmenes autogenerados."""
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

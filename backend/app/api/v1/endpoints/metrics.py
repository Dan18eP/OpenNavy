from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.entities import Repo, AnalysisRun, Metric, Finding, ArchitectureDiff, GeneratedDoc
from app.schemas.api import MetricResponse, FindingResponse
from app.services.pdf_report import PDFReportGenerator

router = APIRouter()


@router.get("/{repo_id}/metrics", summary="Obtener últimas métricas y score global")
def get_latest_metrics(repo_id: str, db: Session = Depends(get_db)):
    """Retorna las métricas del último escaneo completado para el repositorio."""
    repo = db.query(Repo).filter_by(id=repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")

    last_run = (
        db.query(AnalysisRun)
        .filter_by(repo_id=repo_id, status="completed")
        .order_by(AnalysisRun.started_at.desc())
        .first()
    )

    if not last_run:
        # Fallback a última corrida en cualquier estado
        last_run = (
            db.query(AnalysisRun)
            .filter_by(repo_id=repo_id)
            .order_by(AnalysisRun.started_at.desc())
            .first()
        )

    if not last_run:
        return {
            "repo_id": repo_id,
            "status": "no_analyses_yet",
            "global_score": None,
            "metrics": [],
        }

    metrics = db.query(Metric).filter_by(run_id=last_run.id).all()

    return {
        "repo_id": repo_id,
        "run_id": last_run.id,
        "commit_sha": last_run.commit_sha,
        "global_score": last_run.global_score,
        "analyzed_at": last_run.finished_at or last_run.started_at,
        "metrics": [
            {
                "criterio": m.criterio,
                "valor": m.valor,
                "umbral": m.umbral_config,
                "severidad": m.severidad,
                "detalles": m.detalles,
            }
            for m in metrics
        ],
    }


@router.get("/{repo_id}/dependencies", summary="Auditoría y control de versiones de dependencias")
def get_dependencies_audit(repo_id: str, db: Session = Depends(get_db)):
    """Retorna el desglose de dependencias detectadas, versiones actuales, propuestas y estado de compatibilidad."""
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
        return {
            "repo_id": repo_id,
            "total_dependencies": 0,
            "score": 100.0,
            "up_to_date_count": 0,
            "outdated_count": 0,
            "incompatible_count": 0,
            "dependencies": [],
        }

    dep_metric = (
        db.query(Metric)
        .filter_by(run_id=last_run.id, criterio="dependency_version_control")
        .first()
    )

    if dep_metric and dep_metric.detalles and len(dep_metric.detalles.get("dependencies", [])) > 0:
        details = dict(dep_metric.detalles)
        details["repo_id"] = repo_id
        details["run_id"] = last_run.id
        return details

    # Si no hay dependencias en el registro histórico, ejecutar auditoría en caliente
    try:
        from app.analyzers.repo_cloner import RepoCloner
        from app.analyzers.dependency_version_analyzer import DependencyVersionAnalyzer

        cloner = RepoCloner()
        local_path, _, is_temp = cloner.prepare_repo(repo.url, last_run.branch or "main")
        analyzer = DependencyVersionAnalyzer()
        deps_data = analyzer.analyze_dependencies(local_path)
        if is_temp:
            cloner.cleanup(local_path)

        if deps_data and deps_data.get("total_dependencies", 0) > 0:
            if not dep_metric:
                dep_metric = Metric(
                    run_id=last_run.id,
                    criterio="dependency_version_control",
                    valor=deps_data.get("score", 100.0),
                    detalles=deps_data,
                )
                db.add(dep_metric)
            else:
                dep_metric.detalles = deps_data
                dep_metric.valor = deps_data.get("score", 100.0)
            db.commit()

            details = dict(deps_data)
            details["repo_id"] = repo_id
            details["run_id"] = last_run.id
            return details
    except Exception:
        pass

    if dep_metric and dep_metric.detalles:
        details = dict(dep_metric.detalles)
        details["repo_id"] = repo_id
        details["run_id"] = last_run.id
        return details

    return {
        "repo_id": repo_id,
        "run_id": last_run.id,
        "score": dep_metric.valor if dep_metric else 100.0,
        "total_dependencies": 0,
        "up_to_date_count": 0,
        "outdated_count": 0,
        "incompatible_count": 0,
        "dependencies": [],
    }


@router.get("/{repo_id}/metrics/history", summary="Historial temporal de métricas para tendencias")
def get_metrics_history(repo_id: str, db: Session = Depends(get_db)):
    """Retorna la serie temporal de scores globales para gráficos de tendencia."""
    runs = (
        db.query(AnalysisRun)
        .filter_by(repo_id=repo_id, status="completed")
        .order_by(AnalysisRun.started_at.asc())
        .all()
    )

    history = []
    for r in runs:
        history.append({
            "run_id": r.id,
            "commit_sha": r.commit_sha or "HEAD",
            "global_score": r.global_score,
            "started_at": r.started_at,
            "finished_at": r.finished_at,
        })

    return {
        "repo_id": repo_id,
        "total_runs": len(history),
        "history": history,
    }


@router.get("/{repo_id}/findings", summary="Listado de hallazgos y violaciones de calidad")
def get_findings(
    repo_id: str,
    severity: Optional[str] = Query(None, description="Filtrar por severidad: critical, high, warning, info"),
    criterio: Optional[str] = Query(None, description="Filtrar por criterio: solid_principles, clean_code, etc."),
    db: Session = Depends(get_db),
):
    """Retorna los hallazgos cualitativos y violaciones detectadas en el último análisis."""
    last_run = (
        db.query(AnalysisRun)
        .filter_by(repo_id=repo_id)
        .order_by(AnalysisRun.started_at.desc())
        .first()
    )

    if not last_run:
        return {"repo_id": repo_id, "total_findings": 0, "findings": []}

    query = db.query(Finding).filter_by(run_id=last_run.id)
    if severity:
        query = query.filter_by(severidad=severity)
    if criterio:
        query = query.filter_by(criterio=criterio)

    findings = query.all()

    return {
        "repo_id": repo_id,
        "run_id": last_run.id,
        "total_findings": len(findings),
        "findings": [
            {
                "id": f.id,
                "file_path": f.file_path,
                "function_name": f.function_name,
                "line_number": f.line_number,
                "criterio": f.criterio,
                "veredicto": f.veredicto,
                "explicacion": f.explicacion,
                "rag_source": f.rag_source,
                "severidad": f.severidad,
                "sugerencia": f.sugerencia,
            }
            for f in findings
        ],
    }


@router.get("/{repo_id}/complexity", summary="Mapa de funciones complejas")
def get_complexity_map(repo_id: str, db: Session = Depends(get_db)):
    """Retorna las funciones con mayor complejidad ciclomática del repositorio."""
    last_run = (
        db.query(AnalysisRun)
        .filter_by(repo_id=repo_id)
        .order_by(AnalysisRun.started_at.desc())
        .first()
    )

    if not last_run:
        return {"repo_id": repo_id, "complex_functions": []}

    findings = (
        db.query(Finding)
        .filter_by(run_id=last_run.id)
        .filter(Finding.criterio.in_(["cyclomatic_complexity", "solid_principles"]))
        .all()
    )

    return {
        "repo_id": repo_id,
        "run_id": last_run.id,
        "complex_functions": [
            {
                "file": f.file_path,
                "function": f.function_name,
                "line": f.line_number,
                "severity": f.severidad,
                "explicacion": f.explicacion,
                "sugerencia": f.sugerencia,
            }
            for f in findings
        ],
    }


@router.get("/{repo_id}/report/pdf", summary="Descargar Informe Completo de Auditoría y Mejoras en PDF")
def download_pdf_report(repo_id: str, db: Session = Depends(get_db)):
    """Genera y descarga un informe ejecutivo completo en PDF con el diagnóstico de los 8 criterios, arquitectura y plan de mejoras."""
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
        raise HTTPException(status_code=400, detail="El repositorio no cuenta con análisis ejecutados aún.")

    metrics = db.query(Metric).filter_by(run_id=last_run.id).all()
    findings = db.query(Finding).filter_by(run_id=last_run.id).all()
    arch = db.query(ArchitectureDiff).filter_by(run_id=last_run.id).first()
    docs = db.query(GeneratedDoc).filter_by(repo_id=repo_id).all()
    dep_metric = next((m for m in metrics if m.criterio == "dependency_version_control"), None)

    generator = PDFReportGenerator()
    pdf_bytes = generator.generate(
        repo_name=repo.name,
        repo_url=repo.url,
        branch=last_run.branch,
        commit_sha=last_run.commit_sha or "HEAD",
        global_score=last_run.global_score or 0.0,
        metrics=[{"criterio": m.criterio, "valor": m.valor} for m in metrics],
        findings=[
            {
                "file_path": f.file_path,
                "function_name": f.function_name,
                "line_number": f.line_number,
                "criterio": f.criterio,
                "severidad": f.severidad,
                "explicacion": f.explicacion,
                "rag_source": f.rag_source,
                "sugerencia": f.sugerencia,
            }
            for f in findings
        ],
        architecture={
            "resumen": arch.resumen if arch else "",
            "has_circular_dependencies": len(arch.ciclos_detectados) > 0 if arch else False,
            "ciclos_detectados": arch.ciclos_detectados if arch else [],
        },
        generated_docs=[{"titulo": d.titulo, "path": d.path, "tipo": d.tipo} for d in docs],
        dependencies=dep_metric.detalles if dep_metric else None,
    )

    filename = f"Praxia_Report_{repo.name}_{datetime.utcnow().strftime('%Y%m%d')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


@router.post("/{repo_id}/ai-opportunity", summary="Auditar Oportunidad de Inteligencia Artificial (Sesión 01)")
def evaluate_ai_opportunity(
    repo_id: str,
    payload: Optional[List[dict]] = None,
    db: Session = Depends(get_db),
):
    """
    Evalúa la pertinencia de adopción de Inteligencia Artificial en los componentes del repositorio
    utilizando la matriz de 4 cuadrantes formal de la Sesión 01.
    """
    repo = db.query(Repo).filter_by(id=repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")

    from app.services.ai_opportunity_evaluator import AIOpportunityEvaluator
    evaluator = AIOpportunityEvaluator()

    modules_to_evaluate = payload or []

    # Si no se suministraron módulos explícitos en el payload, usar archivos del último análisis
    if not modules_to_evaluate:
        last_run = (
            db.query(AnalysisRun)
            .filter_by(repo_id=repo_id)
            .order_by(AnalysisRun.started_at.desc())
            .first()
        )
        if last_run and last_run.files_analyzed:
            for f in last_run.files_analyzed[:15]:
                modules_to_evaluate.append({
                    "name": f.get("path", "modulo"),
                    "description": f"Módulo de lenguaje {f.get('language', 'código')} con {f.get('lines_of_code', 0)} LOC",
                })

    # Si aún está vacío, simular componentes del core
    if not modules_to_evaluate:
        modules_to_evaluate = [
            {"name": "Auth & Webhook Verification", "description": "Validación criptográfica HMAC-SHA256 de webhooks"},
            {"name": "Deterministic AST Parser", "description": "Parsing sintáctico y cálculo de complejidad ciclomática"},
            {"name": "Architecture Assistant Chat", "description": "Asistente técnico interactivo con RAG"},
            {"name": "Secret Masker", "description": "Enmascaramiento determinístico de API keys y tokens"},
        ]

    result = evaluator.evaluate_repository(modules_to_evaluate)
    return result.model_dump()


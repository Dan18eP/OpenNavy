from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.schemas.state import AnalysisState
from app.core.database import SessionLocal
from app.models.entities import (
    AnalysisRun,
    Metric,
    Finding,
    ArchitectureDiff,
    GeneratedDoc,
    RunStatus,
)
from app.analyzers.repo_cloner import RepoCloner


def _persist_run_status(
    db: Session,
    run_id: int,
    eval_report: Dict[str, Any],
    errors: List[str],
) -> None:
    """Actualiza el estado de finalización y score del AnalysisRun."""
    run = db.query(AnalysisRun).filter_by(id=run_id).first()
    if not run:
        return

    if errors:
        run.status = RunStatus.FAILED.value
        run.error_message = "\n".join(errors)
    else:
        run.status = RunStatus.COMPLETED.value
        run.global_score = eval_report.get("global_score")
    run.finished_at = datetime.utcnow()
    db.add(run)


def _persist_criterion_metrics(
    db: Session,
    run_id: int,
    eval_report: Dict[str, Any],
    deps_data: Dict[str, Any],
) -> None:
    """Persiste las métricas individuales por criterio de evaluación."""
    criterion_scores = eval_report.get("criterion_scores", {})
    for crit_name, score_val in criterion_scores.items():
        metric_details = deps_data if crit_name == "dependency_version_control" else None
        metric = Metric(
            run_id=run_id,
            criterio=crit_name,
            valor=float(score_val),
            umbral_config=70.0,
            severidad="info" if score_val >= 60 else "warning",
            detalles=metric_details,
        )
        db.add(metric)


def _persist_findings(
    db: Session,
    run_id: int,
    solid_violations: List[Dict[str, Any]],
) -> None:
    """Persiste los hallazgos cualitativos detectados."""
    for f in solid_violations:
        finding = Finding(
            run_id=run_id,
            file_path=f.get("file", "unknown"),
            function_name=f.get("function"),
            line_number=f.get("line"),
            criterio=f.get("criterio", "general"),
            veredicto=f.get("veredicto", "advertencia"),
            explicacion=f.get("explicacion", ""),
            rag_source=f.get("fragmento_rag_citado"),
            severidad=f.get("severidad", "high"),
            sugerencia=f.get("sugerencia"),
        )
        db.add(finding)


def _persist_architecture_diff(
    db: Session,
    run_id: int,
    arch_diff: Dict[str, Any],
) -> None:
    """Persiste los registros de diferencias y ciclos de arquitectura."""
    if not arch_diff:
        return
    arch_record = ArchitectureDiff(
        run_id=run_id,
        resumen=f"Módulos analizados: {arch_diff.get('total_modules', 0)}. Ciclos: {len(arch_diff.get('circular_dependencies', []))}",
        dependencias_nuevas=[],
        dependencias_rotas=[],
        ciclos_detectados=arch_diff.get("circular_dependencies", []),
    )
    db.add(arch_record)


def _persist_generated_docs(
    db: Session,
    repo_id: Optional[int],
    generated_docs: List[Dict[str, Any]],
) -> None:
    """Persiste los documentos y ADRs autogenerados en DB y los materializa en disco bajo knowledge-base/."""
    from app.core.config import settings
    kb_path = settings.KNOWLEDGE_BASE_PATH

    for doc in generated_docs:
        # 1. Guardar en Base de Datos SQL si hay repo_id
        if repo_id:
            gen_doc = GeneratedDoc(
                repo_id=repo_id,
                tipo=doc.get("tipo", "adr"),
                path=doc.get("path", ""),
                titulo=doc.get("titulo", "Documento"),
                contenido=doc.get("contenido", ""),
            )
            db.add(gen_doc)

        # 2. Materialización física en disco bajo knowledge-base/ (module-docs/ o adrs/)
        rel_doc_path = doc.get("path", "")
        doc_content = doc.get("contenido", "")
        if rel_doc_path and doc_content and kb_path.exists():
            # Evitar ensuciar el repositorio base durante pruebas unitarias estándar
            if "test-repo" not in rel_doc_path and "test_" not in rel_doc_path and "ADR-0002" not in rel_doc_path:
                try:
                    target_file = kb_path / rel_doc_path
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    target_file.write_text(doc_content, encoding="utf-8")
                except Exception:
                    pass


def persist_node(state: AnalysisState) -> Dict[str, Any]:
    """Nodo 6: Persiste los resultados del análisis en la base de datos relacional."""
    run_id = state.get("run_id")
    repo_id = state.get("repo_id")
    eval_report = state.get("evaluation_report", {})
    solid_violations = state.get("solid_violations", [])
    arch_diff = state.get("architecture_diff", {})
    generated_docs = state.get("generated_docs", [])
    deps_data = state.get("dependencies", {})
    errors = state.get("errors", [])

    if not run_id:
        return {"current_step": "completed"}

    db = SessionLocal()
    try:
        _persist_run_status(db, run_id, eval_report, errors)
        _persist_criterion_metrics(db, run_id, eval_report, deps_data)
        _persist_findings(db, run_id, solid_violations)
        _persist_architecture_diff(db, run_id, arch_diff)
        _persist_generated_docs(db, repo_id, generated_docs)
        db.commit()
    except Exception as e:
        db.rollback()
        errors.append(f"Error al persistir en BD: {str(e)}")
    finally:
        db.close()

    local_path = state.get("local_path", "")
    is_temporary = state.get("is_temporary", False)
    if is_temporary and local_path:
        RepoCloner().cleanup(local_path)

    return {
        "current_step": "completed",
        "errors": errors,
    }

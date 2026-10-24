from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db, SessionLocal
from app.models.entities import Repo, AnalysisRun, TriggerType, RunStatus
from app.api.v1.endpoints.analysis import run_analysis_task
from app.core.security import verify_github_signature, verify_gitlab_token

router = APIRouter()


class PRCommentFormatter:
    """Genera comentarios de Pull Request listos para GitHub / GitLab con el reporte de calidad."""

    @staticmethod
    def format_comment(
        repo_name: str,
        global_score: float,
        findings_count: int,
        metrics: Dict[str, float],
        has_cycles: bool,
    ) -> str:
        status_emoji = "🟢" if global_score >= 80 else "🟡" if global_score >= 60 else "🔴"
        status_text = "SALUDABLE" if global_score >= 80 else "REQUIERE ATENCIÓN" if global_score >= 60 else "DEUDA TÉCNICA CRÍTICA"

        lines = [
            f"## {status_emoji} Praxia — Reporte de Calidad de Código",
            f"**Score Global de Salud:** `{global_score:.1f} / 100` — **{status_text}**",
            "",
            "### 📊 Desglose de Criterios de Calidad",
            "| Criterio | Puntaje | Umbral |",
            "|---|---|---|",
            f"| Índice de Mantenibilidad | `{metrics.get('maintainability_index', 0):.1f}/100` | ≥ 65 |",
            f"| Complejidad Ciclomática | `{metrics.get('cyclomatic_complexity', 0):.1f}/100` | ≤ 10 / func |",
            f"| Principios SOLID | `{metrics.get('solid_principles', 0):.1f}/100` | 0 críticas |",
            f"| Duplicación de Código | `{metrics.get('code_duplication', 0):.1f}/100` | < 5% |",
            f"| Directrices de Arquitectura | `{metrics.get('architecture', 0):.1f}/100` | 0 ciclos |",
            f"| Clean Code | `{metrics.get('clean_code', 0):.1f}/100` | Sin advertencias |",
            "",
        ]

        if has_cycles:
            lines.extend([
                "> ⚠️ **ALERTA ARQUITECTÓNICA:** Se detectaron dependencias circulares en este cambio. "
                "Revisa la pestaña de Arquitectura en el panel de Praxia.",
                ""
            ])

        lines.extend([
            f"🔍 **Hallazgos detectados en este PR:** {findings_count}",
            "",
            "---",
            "*Reporte autogenerado por Praxia AI con rúbrica RAG y LangGraph.*",
        ])

        return "\n".join(lines)


@router.post("/github", summary="Webhook para eventos de GitHub (Push / Pull Request)")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: Optional[str] = Header(None),
    x_hub_signature_256: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Procesa eventos de GitHub (push, pull_request) y dispara automáticamente el análisis del repo."""
    raw_body = await request.body()
    verify_github_signature(raw_body, x_hub_signature_256)

    try:
        import json
        payload = json.loads(raw_body)
    except Exception:
        raise HTTPException(status_code=400, detail="Payload JSON inválido")

    event = x_github_event or "push"
    repository = payload.get("repository", {})
    repo_url = repository.get("clone_url") or repository.get("html_url")
    repo_name = repository.get("name", "repo")

    if not repo_url:
        return {"status": "ignored", "message": "No se encontró URL de repositorio en el payload"}

    branch = "main"
    commit_sha = "HEAD"

    if event == "push":
        ref = payload.get("ref", "")
        branch = ref.replace("refs/heads/", "") if "refs/heads/" in ref else "main"
        commit_sha = payload.get("after") or "HEAD"
    elif event == "pull_request":
        pr = payload.get("pull_request", {})
        branch = pr.get("head", {}).get("ref", "main")
        commit_sha = pr.get("head", {}).get("sha", "HEAD")

    # 1. Registrar o recuperar repo
    repo = db.query(Repo).filter_by(url=repo_url).first()
    if not repo:
        repo = Repo(url=repo_url, name=repo_name, default_branch=branch)
        db.add(repo)
        db.commit()
        db.refresh(repo)

    # 2. Registrar corrida
    run = AnalysisRun(
        repo_id=repo.id,
        commit_sha=commit_sha,
        branch=branch,
        triggered_by=TriggerType.WEBHOOK.value,
        status=RunStatus.PENDING.value,
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    # 3. Lanzar análisis en segundo plano
    background_tasks.add_task(
        run_analysis_task,
        run.id,
        repo.id,
        repo_url,
        branch,
    )

    return {
        "status": "triggered",
        "event": event,
        "repo": repo_name,
        "branch": branch,
        "job_id": run.id,
    }


@router.post("/gitlab", summary="Webhook para eventos de GitLab (Push / Merge Request)")
async def gitlab_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_gitlab_event: Optional[str] = Header(None),
    x_gitlab_token: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Procesa eventos de GitLab (Push Hook, Merge Request Hook) y dispara el análisis."""
    verify_gitlab_token(x_gitlab_token)

    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Payload JSON inválido")

    project = payload.get("project", {})
    repo_url = project.get("git_http_url") or project.get("web_url")
    repo_name = project.get("name", "gitlab-repo")

    if not repo_url:
        return {"status": "ignored", "message": "No se encontró URL en el payload de GitLab"}

    branch = payload.get("ref", "main").replace("refs/heads/", "")
    commit_sha = payload.get("after", "HEAD")

    repo = db.query(Repo).filter_by(url=repo_url).first()
    if not repo:
        repo = Repo(url=repo_url, name=repo_name, default_branch=branch)
        db.add(repo)
        db.commit()
        db.refresh(repo)

    run = AnalysisRun(
        repo_id=repo.id,
        commit_sha=commit_sha,
        branch=branch,
        triggered_by=TriggerType.WEBHOOK.value,
        status=RunStatus.PENDING.value,
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    background_tasks.add_task(
        run_analysis_task,
        run.id,
        repo.id,
        repo_url,
        branch,
    )

    return {
        "status": "triggered",
        "event": x_gitlab_event or "Push Hook",
        "repo": repo_name,
        "branch": branch,
        "job_id": run.id,
    }

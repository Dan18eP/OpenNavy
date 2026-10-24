import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any

from app.core.database import SessionLocal
from app.models.entities import Repo, AnalysisRun, TriggerType, RunStatus
from app.agents.graph import praxia_graph


class PeriodicRepoScanner:
    """Escáner periódico de repositorios conectados para detectar drift y degradación de calidad."""

    def __init__(self, db_session_factory=SessionLocal):
        self.session_factory = db_session_factory

    def scan_monitored_repos(self) -> List[Dict[str, Any]]:
        """Escanea todos los repositorios vigilados registrados en la base de datos."""
        db = self.session_factory()
        results = []

        try:
            repos = db.query(Repo).all()
            for repo in repos:
                last_run = (
                    db.query(AnalysisRun)
                    .filter_by(repo_id=repo.id)
                    .order_by(AnalysisRun.started_at.desc())
                    .first()
                )

                # Registrar nueva corrida con trigger cron
                run = AnalysisRun(
                    repo_id=repo.id,
                    branch=repo.default_branch or "main",
                    triggered_by=TriggerType.CRON.value,
                    status=RunStatus.PENDING.value,
                )
                db.add(run)
                db.commit()
                db.refresh(run)

                initial_state = {
                    "run_id": run.id,
                    "repo_id": repo.id,
                    "repo_url": repo.url,
                    "branch": repo.default_branch or "main",
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
                    graph_result = praxia_graph.invoke(initial_state)
                    score = graph_result.get("evaluation_report", {}).get("global_score")
                    results.append({
                        "repo_id": repo.id,
                        "repo_name": repo.name,
                        "status": "completed",
                        "global_score": score,
                    })
                except Exception as ex:
                    results.append({
                        "repo_id": repo.id,
                        "repo_name": repo.name,
                        "status": "failed",
                        "error": str(ex),
                    })
        finally:
            db.close()

        return results

import tempfile
import uuid
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.agents.graph import praxia_graph
from app.core.database import Base, SessionLocal, init_db
from app.models.entities import Repo, AnalysisRun, TriggerType, RunStatus


def test_graph_compilation():
    assert praxia_graph is not None


def test_end_to_end_graph_execution():
    init_db()

    # 1. Crear directorio temporal con código de prueba
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Archivo A: Servicio con función grande y parámetros excesivos (Violación SRP & Clean Code)
        service_code = """
def process_customer_order(order_id, user_id, payment_method, shipping_addr, coupon_code, notify_email):
    total = 0
    if payment_method == 'card':
        for i in range(10):
            if i % 2 == 0:
                total += i
    elif payment_method == 'paypal':
        while total < 5:
            total += 1
    return total
"""
        (tmp_path / "order_service.py").write_text(service_code, encoding="utf-8")

        # Archivo B y C: Dependencia circular
        (tmp_path / "billing.py").write_text("import shipping\ndef invoice(): pass", encoding="utf-8")
        (tmp_path / "shipping.py").write_text("import billing\ndef ship(): pass", encoding="utf-8")

        # 2. Registrar Repo y Run en la base de datos
        unique_url = f"https://github.com/test-org/order-app-{uuid.uuid4().hex[:6]}"
        db = SessionLocal()
        repo = db.query(Repo).filter_by(url=unique_url).first()
        if not repo:
            repo = Repo(
                url=unique_url,
                name="order-app",
                default_branch="main",
            )
            db.add(repo)
            db.commit()

        run = AnalysisRun(
            repo_id=repo.id,
            commit_sha="c0ffee123",
            branch="main",
            triggered_by=TriggerType.MANUAL.value,
            status=RunStatus.PENDING.value,
        )
        db.add(run)
        db.commit()
        run_id = run.id
        repo_id = repo.id
        db.close()

        # 3. Invocar el Grafo de LangGraph
        initial_state = {
            "run_id": run_id,
            "repo_id": repo_id,
            "repo_url": str(tmp_path),
            "branch": "main",
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

        result_state = praxia_graph.invoke(initial_state)

        # 4. Validar el estado resultante
        assert result_state["current_step"] == "completed"
        assert len(result_state["files"]) >= 3
        assert "python" in result_state["languages_detected"]

        # Validar hallazgos de SOLID / Clean Code / Arquitectura
        findings = result_state["solid_violations"]
        assert len(findings) >= 1

        # Validar que se generaron documentos (ADR / Resumen)
        docs = result_state["generated_docs"]
        assert len(docs) >= 1
        assert any(d["tipo"] == "summary" for d in docs)

        # Validar persistencia en BD
        db = SessionLocal()
        saved_run = db.query(AnalysisRun).filter_by(id=run_id).first()
        assert saved_run.status == RunStatus.COMPLETED.value
        assert saved_run.global_score is not None
        assert len(saved_run.metrics) >= 5
        assert len(saved_run.findings) >= 1
        assert saved_run.architecture_diff is not None
        db.close()

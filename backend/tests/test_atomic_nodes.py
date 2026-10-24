import pytest
from unittest.mock import MagicMock, patch

from app.schemas.state import PraxiaGraphState, ArchitectureFinding
from app.agents.graph import build_analysis_graph, praxia_graph
from app.agents.nodes.clone_node import clone_node
from app.agents.nodes.static_analysis_node import static_analysis_node
from app.agents.nodes.rag_retrieval_node import rag_retrieval_node
from app.agents.nodes.llm_evaluator_node import llm_evaluator_node
from app.agents.nodes.docs_generator_node import docs_generator_node
from app.agents.nodes.persist_node import persist_node


class TestAtomicNodes:
    """Pruebas unitarias de desacoplamiento de nodos atómicos y StateGraph (HU-CORE-01)."""

    def test_praxia_graph_state_schema_attributes(self):
        state: PraxiaGraphState = {
            "run_id": "run-001",
            "repo_id": "1",
            "repo_url": "https://github.com/org/test-repo.git",
            "branch": "main",
            "local_path": "/tmp/test",
            "is_temporary": False,
            "languages_detected": ["python"],
            "files": [],
            "deterministic_metrics": {"loc": 100},
            "static_metrics": {"cc": 2.0},
            "complexity_findings": [],
            "architecture_profile": {"pattern": "layered"},
            "architecture_diff": {"has_cycles": False},
            "dependencies": {},
            "detected_secrets": [],
            "sanitized_code": {},
            "rag_context": [],
            "findings": [],
            "solid_violations": [],
            "evaluation_report": {"global_score": 85.0},
            "generated_docs": [],
            "adrs": [],
            "assessment": [],
            "errors": [],
            "retry_count": 0,
            "current_step": "init",
        }
        assert state["run_id"] == "run-001"
        assert state["architecture_profile"]["pattern"] == "layered"

    def test_architecture_finding_structured_model(self):
        finding = ArchitectureFinding(
            file="src/domain/user.py",
            function="get_user",
            line=15,
            criterio="solid_principles",
            veredicto="violacion",
            explicacion="La función gestiona persistencia y cálculo simultáneamente.",
            fragmento_rag_citado="solid-principles.md#single-responsibility",
            severidad="high",
            sugerencia="Extraer acceso a datos a un repositorio."
        )
        assert finding.file == "src/domain/user.py"
        assert finding.severidad == "high"

    def test_graph_builds_and_compiles_successfully(self):
        compiled = build_analysis_graph()
        assert compiled is not None
        assert hasattr(compiled, "invoke")

    def test_llm_evaluator_node_invokes_llm_when_available(self):
        mock_llm = MagicMock()
        mock_ai_msg = MagicMock()
        mock_ai_msg.content = "Revisión arquitectónica: El módulo presenta alto acoplamiento con la capa de infraestructura."
        mock_llm.invoke.return_value = mock_ai_msg

        with patch("app.core.llm.get_llm", return_value=mock_llm):
            state = {
                "files": [
                    {
                        "path": "src/service.py",
                        "language": "python",
                        "cyclomatic_complexity_total": 12,
                        "raw_content": "def run():\n    pass\n"
                    }
                ],
                "static_metrics": {},
                "architecture_diff": {},
                "dependencies": {},
                "rag_context": [{"criterion": "solid", "content": "SRP rule"}],
                "errors": [],
            }
            out = llm_evaluator_node(state)
            assert out["current_step"] == "rag_evaluation_completed"
            assert "findings" in out
            llm_findings = [f for f in out["findings"] if f.get("criterio") == "llm_contextual_review"]
            assert len(llm_findings) == 1
            assert "alto acoplamiento" in llm_findings[0]["explicacion"]

    def test_llm_evaluator_node_resilient_fallback_without_llm(self):
        with patch("app.core.llm.get_llm", return_value=None):
            state = {
                "files": [
                    {
                        "path": "src/simple.py",
                        "language": "python",
                        "cyclomatic_complexity_total": 1,
                        "raw_content": "def simple(): return 1"
                    }
                ],
                "static_metrics": {},
                "architecture_diff": {},
                "dependencies": {},
                "rag_context": [],
                "errors": [],
            }
            out = llm_evaluator_node(state)
            assert out["current_step"] == "rag_evaluation_completed"
            assert "evaluation_report" in out
            assert out["evaluation_report"]["global_score"] >= 0.0

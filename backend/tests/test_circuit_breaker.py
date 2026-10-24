import pytest
from unittest.mock import patch, MagicMock

from app.agents.graph import build_analysis_graph, route_evaluation_or_offline
from app.agents.nodes.offline_synthesizer_node import offline_synthesizer_node


class TestCircuitBreakerAndOfflineMode:
    """Pruebas del Circuit Breaker y Modo Offline con Fallback Determinístico (HU-CORE-03)."""

    def test_route_evaluation_or_offline_selects_offline_when_flag_present(self):
        state = {"offline_mode": True}
        route = route_evaluation_or_offline(state)
        assert route == "offline"

    def test_route_evaluation_or_offline_selects_offline_when_llm_unavailable(self):
        with patch("app.core.llm.get_llm", return_value=None):
            state = {"offline_mode": False}
            route = route_evaluation_or_offline(state)
            assert route == "offline"

    def test_route_evaluation_or_offline_selects_llm_when_llm_available_and_not_offline(self):
        mock_llm = MagicMock()
        with patch("app.core.llm.get_llm", return_value=mock_llm):
            state = {"offline_mode": False}
            route = route_evaluation_or_offline(state)
            assert route == "llm"

    def test_offline_synthesizer_node_produces_deterministic_report_with_banner(self):
        state = {
            "files": [
                {
                    "path": "backend/app/service.py",
                    "maintainability_index": 45.0,
                    "functions": [
                        {"name": "complex_calc", "lines_of_code": 80, "cyclomatic_complexity": 14, "parameters_count": 5, "nesting_depth": 4}
                    ]
                }
            ],
            "static_metrics": {
                "average_maintainability_index": 45.0,
                "average_cyclomatic_complexity": 14.0,
                "duplication_percentage": 6.5,
            },
            "architecture_diff": {
                "has_cycles": True,
                "circular_dependencies": [["module_a", "module_b", "module_a"]],
                "layer_violations": [],
            },
            "dependencies": {},
            "detected_secrets": [
                {"file": "config.py", "type": "OpenAI API Key", "sample": "sk-p****"}
            ],
        }

        out = offline_synthesizer_node(state)
        assert out["current_step"] == "offline_synthesis_completed"
        assert out["offline_mode"] is True

        report = out["evaluation_report"]
        assert report["mode"] == "deterministic_offline"
        assert "Generado en Modo Determinístico Offline" in report["banner"]
        assert report["global_score"] >= 0.0

        findings = out["findings"]
        criteria = [f["criterio"] for f in findings]
        assert "security_secrets" in criteria
        assert "architecture_guidelines" in criteria
        assert "solid_principles" in criteria

    def test_graph_executes_offline_circuit_breaker_end_to_end(self):
        graph = build_analysis_graph()
        initial_state = {
            "run_id": "offline-run-001",
            "repo_id": "1",
            "repo_url": "https://github.com/org/test-repo.git",
            "branch": "main",
            "local_path": "",
            "is_temporary": False,
            "offline_mode": True,  # Activar circuit breaker
            "languages_detected": [],
            "files": [],
            "static_metrics": {},
            "complexity_findings": [],
            "solid_violations": [],
            "architecture_diff": None,
            "dependencies": None,
            "detected_secrets": [],
            "rag_context": [],
            "evaluation_report": {},
            "generated_docs": [],
            "errors": [],
            "retry_count": 0,
            "current_step": "init",
        }

        # Mocking clone_node y persist_node para aislamiento
        with patch("app.agents.nodes.clone_node.RepoCloner.prepare_repo", return_value=("/tmp/repo", "sha1", False)), \
             patch("app.analyzers.manager.AnalyzerManager.analyze_repository", return_value={"file_nodes": [], "languages": [], "summary_metrics": {}, "architecture": {}, "dependencies": {}}), \
             patch("app.agents.nodes.persist_node.SessionLocal") as mock_session:

            mock_db = MagicMock()
            mock_session.return_value = mock_db

            result = graph.invoke(initial_state)
            assert result["current_step"] == "completed"
            assert result.get("offline_mode") is True
            assert result.get("evaluation_report", {}).get("mode") == "deterministic_offline"

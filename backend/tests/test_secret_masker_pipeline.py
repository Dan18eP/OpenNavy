import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
import tempfile
import shutil

from fastapi.testclient import TestClient
from app.main import app
from app.analyzers.secret_masker import SecretMasker
from app.analyzers.manager import AnalyzerManager
from app.agents.nodes.static_analysis_node import static_analysis_node
from app.agents.nodes.llm_evaluator_node import llm_evaluator_node
from app.models.entities import Repo, AnalysisRun

client = TestClient(app)


class TestSecretMaskerUnit:
    """Pruebas unitarias de enmascaramiento con patrones sensibles."""

    def test_secret_masker_patterns_comprehensive(self):
        masker = SecretMasker()
        content = """
        AWS_KEY = "AKIA1234567890ABCDEF"
        OPENAI = "sk-proj-abc123456789012345678901234567890"
        GITHUB = "ghp_1234567890abcdef1234567890abcdef1234"
        JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        password = "SuperSecretPassword123!"
        """
        masked, detections = masker.mask_secrets(content)

        assert "AKIA1234567890ABCDEF" not in masked
        assert "[REDACTED_AWS_KEY]" in masked

        assert "sk-proj-abc" not in masked
        assert "[REDACTED_OPENAI_KEY]" in masked

        assert "ghp_1234567890" not in masked
        assert "[REDACTED_GITHUB_TOKEN]" in masked

        assert "eyJhbGci" not in masked
        assert "[REDACTED_JWT_TOKEN]" in masked

        assert "SuperSecretPassword123!" not in masked
        assert "[REDACTED_PASSWORD]" in masked
        assert len(detections) >= 5


class TestPipelineSecretMasking:
    """Pruebas de integración del enmascaramiento en AnalyzerManager y nodos del pipeline."""

    def test_analyzer_manager_masks_file_node_content_and_reports_secrets(self):
        tmp_dir = tempfile.mkdtemp(prefix="praxia_test_secrets_")
        try:
            secret_file = Path(tmp_dir) / "config.py"
            secret_file.write_text(
                'API_KEY = "sk-proj-supersecrettoken1234567890"\n'
                'AWS_ACCESS = "AKIA1234567890ABCDEF"\n'
                'def get_key():\n    return API_KEY\n',
                encoding="utf-8"
            )

            manager = AnalyzerManager()
            results = manager.analyze_repository(tmp_dir)

            assert "detected_secrets" in results
            assert len(results["detected_secrets"]) >= 2
            types = [s["type"] for s in results["detected_secrets"]]
            assert "OpenAI API Key" in types
            assert "AWS Access Key" in types

            # Verificar que el raw_content del FileNode fue enmascarado
            file_node = results["file_nodes"][0]
            assert "sk-proj-supersecrettoken" not in file_node.raw_content
            assert "AKIA1234567890ABCDEF" not in file_node.raw_content
            assert "[REDACTED_OPENAI_KEY]" in file_node.raw_content
            assert "[REDACTED_AWS_KEY]" in file_node.raw_content
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_static_analysis_node_propagates_detected_secrets(self):
        tmp_dir = tempfile.mkdtemp(prefix="praxia_test_node_")
        try:
            secret_file = Path(tmp_dir) / "app.py"
            secret_file.write_text('SECRET_TOKEN = "ghp_1234567890abcdef1234567890abcdef1234"\n', encoding="utf-8")

            state = {
                "run_id": "test-run",
                "repo_id": "test-repo",
                "repo_url": "https://github.com/test/repo.git",
                "branch": "main",
                "local_path": tmp_dir,
                "is_temporary": False,
                "languages_detected": [],
                "files": [],
                "static_metrics": {},
                "complexity_findings": [],
                "solid_violations": [],
                "architecture_diff": None,
                "dependencies": None,
                "rag_context": [],
                "evaluation_report": {},
                "generated_docs": [],
                "errors": [],
                "retry_count": 0,
                "current_step": "cloned",
            }

            out = static_analysis_node(state)
            assert out["current_step"] == "static_analysis_completed"
            assert "detected_secrets" in out
            assert len(out["detected_secrets"]) >= 1
            assert out["detected_secrets"][0]["type"] == "GitHub Token"
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    def test_llm_evaluator_node_generates_security_critical_findings(self):
        state = {
            "files": [],
            "static_metrics": {},
            "architecture_diff": {},
            "dependencies": {},
            "detected_secrets": [
                {"file": "src/auth.py", "type": "OpenAI API Key", "sample": "sk-p****"}
            ],
            "rag_context": [],
            "errors": [],
        }

        out = llm_evaluator_node(state)
        findings = out["solid_violations"]
        sec_findings = [f for f in findings if f.get("criterio") == "security_secrets"]
        assert len(sec_findings) == 1
        assert sec_findings[0]["severidad"] == "critical"
        assert sec_findings[0]["file"] == "src/auth.py"
        assert "OpenAI API Key" in sec_findings[0]["explicacion"]


class TestChatSecretMasking:
    """Pruebas de enmascaramiento forzoso en el endpoint de Chat."""

    def test_chat_masks_secrets_before_llm_and_rag(self):
        # 1. Crear un repo real en SQLite de pruebas
        create_payload = {
            "url": "https://github.com/test-org/chat-secret-guard",
            "name": "chat-secret-guard",
            "default_branch": "main",
        }
        repo_resp = client.post("/api/v1/repos/", json=create_payload)
        assert repo_resp.status_code == 200
        repo_id = repo_resp.json()["id"]

        with patch("app.api.v1.endpoints.chat.get_knowledge_retriever") as mock_retriever_getter, \
             patch("app.api.v1.endpoints.chat.get_llm") as mock_llm_getter:

            mock_retriever = MagicMock()
            mock_retriever.search_general.return_value = []
            mock_retriever_getter.return_value = mock_retriever

            mock_llm = MagicMock()
            mock_response = MagicMock()
            mock_response.content = "Respuesta segura de prueba."
            mock_llm.invoke.return_value = mock_response
            mock_llm_getter.return_value = mock_llm

            raw_secret = "ghp_1234567890abcdef1234567890abcdef1234"
            payload = {
                "message": f"¿Cómo puedo refactorizar este token {raw_secret} en mi API?"
            }

            resp = client.post(f"/api/v1/repos/{repo_id}/chat", json=payload)
            assert resp.status_code == 200

            # Verificar que el LLM NUNCA recibió el token en texto plano
            llm_calls = mock_llm.invoke.call_args_list
            assert len(llm_calls) == 1
            messages_sent = llm_calls[0][0][0]
            user_msg = next(m["content"] for m in messages_sent if m["role"] == "user")
            assert raw_secret not in user_msg
            assert "[REDACTED_GITHUB_TOKEN]" in user_msg

            # Verificar que el RAG Retriever tampoco recibió el secreto
            retriever_calls = mock_retriever.search_general.call_args_list
            assert len(retriever_calls) == 1
            rag_query = retriever_calls[0][0][0]
            assert raw_secret not in rag_query
            assert "[REDACTED_GITHUB_TOKEN]" in rag_query

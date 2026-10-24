import hmac
import hashlib
import json
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings

client = TestClient(app)


class TestWebhookCryptographicVerification:
    """Pruebas de validación criptográfica HMAC-SHA256 y tokens en Webhooks (HU-SEC-03)."""

    def test_github_webhook_rejects_missing_signature_when_secret_set(self):
        with patch.object(settings, "WEBHOOK_SECRET", "super-secret-key-123"):
            payload = {
                "repository": {"clone_url": "https://github.com/org/repo.git", "name": "repo"},
                "ref": "refs/heads/main",
                "after": "abcdef123456"
            }
            resp = client.post("/api/v1/webhooks/github", json=payload)
            assert resp.status_code == 401
            assert "X-Hub-Signature-256 faltante" in resp.json()["detail"]

    def test_github_webhook_rejects_invalid_signature(self):
        with patch.object(settings, "WEBHOOK_SECRET", "super-secret-key-123"):
            payload = {
                "repository": {"clone_url": "https://github.com/org/repo.git", "name": "repo"},
                "ref": "refs/heads/main",
                "after": "abcdef123456"
            }
            headers = {"X-Hub-Signature-256": "sha256=invalidhexsignature00000000000000000000000000000000"}
            resp = client.post("/api/v1/webhooks/github", json=payload, headers=headers)
            assert resp.status_code == 401
            assert "Firma criptográfica inválida" in resp.json()["detail"]

    @patch("app.api.v1.endpoints.webhooks.run_analysis_task")
    def test_github_webhook_accepts_valid_hmac_signature(self, mock_run):
        mock_run.return_value = None
        secret = "super-secret-key-123"
        with patch.object(settings, "WEBHOOK_SECRET", secret):
            payload = {
                "repository": {"clone_url": "https://github.com/org/valid-repo.git", "name": "valid-repo"},
                "ref": "refs/heads/main",
                "after": "abcdef123456"
            }
            raw_body = json.dumps(payload).encode("utf-8")
            signature = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
            headers = {
                "X-Hub-Signature-256": f"sha256={signature}",
                "Content-Type": "application/json"
            }

            resp = client.post("/api/v1/webhooks/github", content=raw_body, headers=headers)
            assert resp.status_code == 200
            assert resp.json()["status"] == "triggered"

    def test_gitlab_webhook_rejects_missing_or_invalid_token(self):
        with patch.object(settings, "GITLAB_WEBHOOK_TOKEN", "gitlab-secret-token-xyz"):
            payload = {
                "project": {"git_http_url": "https://gitlab.com/org/gl-repo.git", "name": "gl-repo"},
                "ref": "refs/heads/main",
                "after": "987654abcdef"
            }
            # 1. Sin header
            resp = client.post("/api/v1/webhooks/gitlab", json=payload)
            assert resp.status_code == 401
            assert "X-Gitlab-Token faltante" in resp.json()["detail"]

            # 2. Con header erróneo
            headers = {"X-Gitlab-Token": "wrong-token"}
            resp = client.post("/api/v1/webhooks/gitlab", json=payload, headers=headers)
            assert resp.status_code == 401
            assert "Token de webhook de GitLab inválido" in resp.json()["detail"]

    @patch("app.api.v1.endpoints.webhooks.run_analysis_task")
    def test_gitlab_webhook_accepts_valid_token(self, mock_run):
        mock_run.return_value = None
        secret_token = "gitlab-secret-token-xyz"
        with patch.object(settings, "GITLAB_WEBHOOK_TOKEN", secret_token):
            payload = {
                "project": {"git_http_url": "https://gitlab.com/org/gl-valid.git", "name": "gl-valid"},
                "ref": "refs/heads/main",
                "after": "987654abcdef"
            }
            headers = {"X-Gitlab-Token": secret_token}
            resp = client.post("/api/v1/webhooks/gitlab", json=payload, headers=headers)
            assert resp.status_code == 200
            assert resp.json()["status"] == "triggered"

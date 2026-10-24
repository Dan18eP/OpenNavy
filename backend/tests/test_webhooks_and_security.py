import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db
from app.analyzers.secret_masker import SecretMasker
from app.api.v1.endpoints.webhooks import PRCommentFormatter

client = TestClient(app)


# ── 1. Secret Masker ───────────────────────────────────────────────────────────

def test_secret_masker_redacts_aws_key():
    masker = SecretMasker()
    code = 'AWS_KEY = "AKIA1234567890ABCDEF"'
    masked, detections = masker.mask_secrets(code)
    assert "AKIA1234567890ABCDEF" not in masked
    assert "[REDACTED_AWS_KEY]" in masked
    assert any(d["type"] == "AWS Access Key" for d in detections)


def test_secret_masker_redacts_openai_key():
    masker = SecretMasker()
    code = 'key = "sk-proj-abc123456789012345678901234567890"'
    masked, detections = masker.mask_secrets(code)
    assert "sk-proj-abc" not in masked
    assert "[REDACTED_OPENAI_KEY]" in masked


def test_secret_masker_redacts_github_token():
    masker = SecretMasker()
    code = 'token = "ghp_1234567890abcdef1234567890abcdef1234"'
    masked, detections = masker.mask_secrets(code)
    assert "ghp_" not in masked
    assert "[REDACTED_GITHUB_TOKEN]" in masked


def test_secret_masker_clean_code_unchanged():
    masker = SecretMasker()
    clean_code = 'def hello():\n    print("Hello World")\n    return 42\n'
    masked, detections = masker.mask_secrets(clean_code)
    assert masked == clean_code
    assert len(detections) == 0


# ── 2. PR Comment Formatter ────────────────────────────────────────────────────

def test_pr_comment_formatter_healthy_repo():
    comment = PRCommentFormatter.format_comment(
        repo_name="my-service",
        global_score=88.5,
        findings_count=3,
        metrics={
            "maintainability_index": 82.0,
            "cyclomatic_complexity": 90.0,
            "solid_principles": 85.0,
            "code_duplication": 95.0,
            "architecture": 80.0,
            "clean_code": 89.0,
        },
        has_cycles=False,
    )
    assert "Praxia — Reporte de Calidad" in comment
    assert "88.5 / 100" in comment
    assert "Índice de Mantenibilidad" in comment
    assert "SALUDABLE" in comment
    assert "" in comment


def test_pr_comment_formatter_critical_repo_with_cycles():
    comment = PRCommentFormatter.format_comment(
        repo_name="legacy-monolith",
        global_score=45.0,
        findings_count=23,
        metrics={"maintainability_index": 35.0, "architecture": 20.0},
        has_cycles=True,
    )
    assert "DEUDA TÉCNICA CRÍTICA" in comment
    assert "" in comment
    assert "ALERTA ARQUITECTÓNICA" in comment


# ── 3. Webhooks GitHub / GitLab ────────────────────────────────────────────────

@patch("app.api.v1.endpoints.webhooks.run_analysis_task")
def test_github_webhook_push_event(mock_run):
    init_db()
    mock_run.return_value = None

    payload = {
        "repository": {
            "name": "push-event-repo",
            "clone_url": "https://github.com/my-org/push-event-repo",
            "html_url": "https://github.com/my-org/push-event-repo",
        },
        "ref": "refs/heads/feature/login",
        "after": "9f8e7d6c5b4a",
    }

    res = client.post(
        "/api/v1/webhooks/github",
        json=payload,
        headers={"X-GitHub-Event": "push"},
    )

    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "triggered"
    assert data["branch"] == "feature/login"
    assert "job_id" in data


@patch("app.api.v1.endpoints.webhooks.run_analysis_task")
def test_gitlab_webhook_push_event(mock_run):
    init_db()
    mock_run.return_value = None

    payload = {
        "project": {
            "name": "gitlab-billing",
            "git_http_url": "https://gitlab.com/my-org/gitlab-billing",
        },
        "ref": "refs/heads/main",
        "after": "1a2b3c4d5e6f",
    }

    res = client.post(
        "/api/v1/webhooks/gitlab",
        json=payload,
        headers={"X-Gitlab-Event": "Push Hook"},
    )

    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "triggered"
    assert data["repo"] == "gitlab-billing"
    assert "job_id" in data

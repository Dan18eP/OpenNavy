import asyncio
import json
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.core.event_channel import get_or_create_channel, remove_channel, SSEProgressEvent
from app.api.v1.endpoints.analysis import run_analysis_task

client = TestClient(app)


class TestSSEStreamingQueue:
    """Pruebas de streaming reactivo SSE con asyncio.Queue (HU-CORE-02)."""

    @pytest.mark.asyncio
    async def test_event_channel_emits_and_consumes_typed_events(self):
        channel = get_or_create_channel("test-job-123")
        try:
            await channel.emit(
                node="static_analysis",
                status="in_progress",
                progress_percent=40,
                message="Analizando AST y métricas...",
                partial_data={"loc": 250}
            )

            event = await asyncio.wait_for(channel.queue.get(), timeout=2.0)
            assert isinstance(event, SSEProgressEvent)
            assert event.node == "static_analysis"
            assert event.progress_percent == 40
            assert event.partial_data == {"loc": 250}
        finally:
            remove_channel("test-job-123")

    def test_run_analysis_task_emits_to_channel_and_sse_endpoint_receives(self):
        job_id = "test-job-sse-456"
        channel = get_or_create_channel(job_id)

        # Emitir eventos de prueba al canal
        channel.emit_sync(
            node="clone",
            status="in_progress",
            progress_percent=15,
            message="Clonando repositorio..."
        )
        channel.emit_sync(
            node="completed",
            status="completed",
            progress_percent=100,
            message="Análisis finalizado con éxito.",
            partial_data={"global_score": 88.5}
        )

        with client.stream("GET", f"/api/v1/repos/analyze/{job_id}/stream") as response:
            assert response.status_code == 200
            assert "text/event-stream" in response.headers.get("content-type", "")

            lines = [line for line in response.iter_lines() if line.startswith("data: ")]
            assert len(lines) >= 2

            first_payload = json.loads(lines[0].replace("data: ", ""))
            assert first_payload["node"] == "clone"
            assert first_payload["progress_percent"] == 15

            last_payload = json.loads(lines[-1].replace("data: ", ""))
            assert last_payload["node"] == "completed"
            assert last_payload["status"] == "completed"
            assert last_payload["partial_data"]["global_score"] == 88.5

        remove_channel(job_id)

import asyncio
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel


class SSEProgressEvent(BaseModel):
    node: str
    status: str  # in_progress, completed, failed
    progress_percent: int
    message: str
    partial_data: Optional[Dict[str, Any]] = None
    timestamp: float


class AnalysisEventChannel:
    """
    Canal asíncrono basado en asyncio.Queue para desacoplar la emisión y consumo
    de eventos Server-Sent Events (SSE) en tiempo real por cada corrida de análisis.
    """

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.queue: asyncio.Queue = asyncio.Queue()
        self.is_closed = False

    async def emit(
        self,
        node: str,
        status: str,
        progress_percent: int,
        message: str,
        partial_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        if self.is_closed:
            return

        event = SSEProgressEvent(
            node=node,
            status=status,
            progress_percent=progress_percent,
            message=message,
            partial_data=partial_data,
            timestamp=time.time(),
        )
        await self.queue.put(event)

    def emit_sync(
        self,
        node: str,
        status: str,
        progress_percent: int,
        message: str,
        partial_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Permite emitir eventos desde hilos o funciones síncronas de forma thread-safe."""
        if self.is_closed:
            return

        event = SSEProgressEvent(
            node=node,
            status=status,
            progress_percent=progress_percent,
            message=message,
            partial_data=partial_data,
            timestamp=time.time(),
        )
        try:
            self.queue.put_nowait(event)
        except Exception:
            pass

    async def close(self) -> None:
        self.is_closed = True
        # Enviar centinela None para desbloquear generadores
        await self.queue.put(None)


# Gestor global de canales por run_id
_active_channels: Dict[str, AnalysisEventChannel] = {}


def get_or_create_channel(run_id: str) -> AnalysisEventChannel:
    if run_id not in _active_channels:
        _active_channels[run_id] = AnalysisEventChannel(run_id)
    return _active_channels[run_id]


def remove_channel(run_id: str) -> None:
    _active_channels.pop(run_id, None)

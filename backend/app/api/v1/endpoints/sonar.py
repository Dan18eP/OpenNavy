import json
import logging
from typing import Dict, List, Set, Any, Optional
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

router = APIRouter()


class FleetSonarManager:
    """
    Concentrador en tiempo real de Sonar de Flota (Fleet Sonar).
    Coordina la presencia de tripulantes y el radar de colisión arquitectónica sobre red local.
    """

    def __init__(self):
        # Conexiones activas: websocket -> metadata del tripulante
        self.active_connections: Dict[WebSocket, Dict[str, Any]] = {}

    async def connect(self, websocket: WebSocket, officer_name: str):
        await websocket.accept()
        self.active_connections[websocket] = {
            "officer_name": officer_name,
            "current_file": None,
            "current_issue": None,
            "connected_at": datetime.utcnow().isoformat(),
        }
        logger.info(f"[FleetSonar] Oficial '{officer_name}' se unió al puente de mando.")
        await self.broadcast_fleet_status()

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            officer = self.active_connections[websocket]["officer_name"]
            del self.active_connections[websocket]
            logger.info(f"[FleetSonar] Oficial '{officer}' abandonó la sesión.")

    async def broadcast(self, message: Dict[str, Any]):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)

    async def broadcast_fleet_status(self):
        """Difunde la lista completa de tripulantes activos a toda la flota."""
        crew_members = [
            {
                "officer_name": meta["officer_name"],
                "current_file": meta["current_file"],
                "current_issue": meta["current_issue"],
                "connected_at": meta["connected_at"],
            }
            for meta in self.active_connections.values()
        ]
        await self.broadcast({
            "type": "FLEET_UPDATE",
            "active_officers_count": len(crew_members),
            "crew": crew_members,
            "timestamp": datetime.utcnow().isoformat(),
        })

    async def handle_navigation(self, websocket: WebSocket, file_path: str, issue_id: Optional[str] = None):
        """Actualiza la posición del tripulante y activa el radar de colisión."""
        if websocket not in self.active_connections:
            return

        current_officer = self.active_connections[websocket]["officer_name"]
        self.active_connections[websocket]["current_file"] = file_path
        if issue_id:
            self.active_connections[websocket]["current_issue"] = issue_id

        # 1. Alerta de Presencia
        await self.broadcast({
            "type": "PEER_PRESENCE",
            "officer_name": current_officer,
            "file_path": file_path,
            "issue_id": issue_id,
            "timestamp": datetime.utcnow().isoformat(),
        })

        # 2. Radar de Colisión: Detectar si otro tripulante está en el mismo archivo o módulo acoplado
        for other_ws, other_meta in self.active_connections.items():
            if other_ws != websocket and other_meta.get("current_file"):
                other_file = other_meta["current_file"]
                # Colisión directa (mismo archivo)
                if other_file == file_path:
                    await self.broadcast({
                        "type": "COLLISION_ALERT",
                        "severity": "CRITICAL",
                        "reason": "Ambos oficiales están editando exactamente el mismo archivo.",
                        "officers": [current_officer, other_meta["officer_name"]],
                        "conflicting_files": [file_path],
                        "timestamp": datetime.utcnow().isoformat(),
                    })
                # Colisión por módulo acoplado (misma carpeta o prefijo)
                elif self._are_modules_coupled(file_path, other_file):
                    await self.broadcast({
                        "type": "COLLISION_ALERT",
                        "severity": "WARNING",
                        "reason": "Módulos fuertemente interconectados detectados por el Radar de Tarjan.",
                        "officers": [current_officer, other_meta["officer_name"]],
                        "conflicting_files": [file_path, other_file],
                        "timestamp": datetime.utcnow().isoformat(),
                    })

    def _are_modules_coupled(self, file_a: str, file_b: str) -> bool:
        """Determina heurísticamente acoplamiento cercano si comparten directorio o submódulo."""
        parts_a = file_a.replace("\\", "/").split("/")
        parts_b = file_b.replace("\\", "/").split("/")
        if len(parts_a) > 1 and len(parts_b) > 1:
            return parts_a[:-1] == parts_b[:-1]
        return False

    async def broadcast_course_plotted(self, officer_name: str, mission: str, waypoints: List[Dict[str, Any]]):
        """Difunde a la flota que un nuevo plan de navegación ha sido trazado por Gemma 4."""
        await self.broadcast({
            "type": "SHARED_BLUEPRINT",
            "officer_name": officer_name,
            "mission": mission,
            "waypoints": waypoints,
            "timestamp": datetime.utcnow().isoformat(),
        })


sonar_hub = FleetSonarManager()


@router.websocket("/ws/sonar")
async def sonar_websocket_endpoint(websocket: WebSocket, officer: str = "Cadet"):
    """
    Endpoint WebSocket de Fleet Sonar para sincronización LAN en tiempo real.
    Conéctate desde React con: ws://<HOST_IP>:8000/api/v1/sonar/ws/sonar?officer=Daniel
    """
    await sonar_hub.connect(websocket, officer)
    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")

            if event_type == "NAVIGATE":
                file_path = data.get("file_path", "")
                issue_id = data.get("issue_id")
                await sonar_hub.handle_navigation(websocket, file_path, issue_id)

            elif event_type == "PING":
                await websocket.send_json({"type": "PONG", "timestamp": datetime.utcnow().isoformat()})

    except WebSocketDisconnect:
        sonar_hub.disconnect(websocket)
        await sonar_hub.broadcast_fleet_status()
    except Exception as e:
        logger.error(f"[FleetSonar] Error en WebSocket: {e}")
        sonar_hub.disconnect(websocket)
        await sonar_hub.broadcast_fleet_status()


@router.get("/status", summary="Estado actual de la Flota")
def get_fleet_status():
    """Consulta HTTP rápida del estado de tripulantes activos en LAN."""
    return {
        "active_officers": len(sonar_hub.active_connections),
        "officers": [meta["officer_name"] for meta in sonar_hub.active_connections.values()],
    }

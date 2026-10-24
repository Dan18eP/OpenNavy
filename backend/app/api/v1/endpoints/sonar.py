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
    Coordina la presencia de tripulantes, planos compartidos y el radar de colision arquitectonica sobre red local.
    """

    def __init__(self):
        # Conexiones activas: websocket -> metadata del tripulante
        self.active_connections: Dict[WebSocket, Dict[str, Any]] = {}
        # Buffer de ultimos planos trazados por Gemma 4 (ultimos 20)
        self.blueprints: List[Dict[str, Any]] = []

    async def connect(self, websocket: WebSocket, officer_name: str):
        await websocket.accept()
        self.active_connections[websocket] = {
            "officer_name": officer_name,
            "current_file": None,
            "current_issue": None,
            "connected_at": datetime.utcnow().isoformat(),
        }
        logger.info(f"[FleetSonar] Oficial '{officer_name}' se unio al puente de mando.")
        await self.broadcast_fleet_status()

        # Enviar inmediatamente el ultimo plano activo al tripulante recien conectado
        latest = self.get_latest_blueprint()
        if latest:
            try:
                await websocket.send_json({
                    "type": "SHARED_BLUEPRINT_SYNC",
                    "blueprint": latest,
                    "timestamp": datetime.utcnow().isoformat(),
                })
            except Exception as e:
                logger.warning(f"[FleetSonar] No se pudo enviar blueprint inicial a '{officer_name}': {e}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            officer = self.active_connections[websocket]["officer_name"]
            del self.active_connections[websocket]
            logger.info(f"[FleetSonar] Oficial '{officer}' abandono la sesion.")

    async def broadcast(self, message: Dict[str, Any]):
        disconnected = []
        for connection in list(self.active_connections.keys()):
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
        """Actualiza la posicion del tripulante y activa el radar de colision."""
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

        # 2. Radar de Colision: Detectar si otro tripulante esta en el mismo archivo o modulo acoplado
        for other_ws, other_meta in list(self.active_connections.items()):
            if other_ws != websocket and other_meta.get("current_file"):
                other_file = other_meta["current_file"]
                # Colision directa (mismo archivo)
                if other_file == file_path:
                    await self.broadcast({
                        "type": "COLLISION_ALERT",
                        "severity": "CRITICAL",
                        "reason": "Ambos oficiales estan editando exactamente el mismo archivo.",
                        "officers": [current_officer, other_meta["officer_name"]],
                        "conflicting_files": [file_path],
                        "timestamp": datetime.utcnow().isoformat(),
                    })
                # Colision por modulo acoplado (segun matriz de Tarjan o submodulo)
                elif self._are_modules_coupled(file_path, other_file):
                    await self.broadcast({
                        "type": "COLLISION_ALERT",
                        "severity": "WARNING",
                        "reason": "Modulos fuertemente interconectados detectados por el Radar de Tarjan.",
                        "officers": [current_officer, other_meta["officer_name"]],
                        "conflicting_files": [file_path, other_file],
                        "timestamp": datetime.utcnow().isoformat(),
                    })

    def _are_modules_coupled(self, file_a: str, file_b: str) -> bool:
        """
        Determina acoplamiento entre modulos utilizando la matriz de Tarjan SCC
        del servicio AntiDrift, con fallback a coincidencia de directorio.
        """
        try:
            from app.services.anti_drift_service import anti_drift_service
            if anti_drift_service.are_modules_coupled_via_tarjan(file_a, file_b):
                return True
        except Exception as e:
            logger.debug(f"[FleetSonar] Error consultando acoplamiento Tarjan: {e}")

        parts_a = file_a.replace("\\", "/").split("/")
        parts_b = file_b.replace("\\", "/").split("/")
        if len(parts_a) > 1 and len(parts_b) > 1:
            return parts_a[:-1] == parts_b[:-1]
        return False

    async def broadcast_course_plotted(self, officer_name: str, mission: str, waypoints: List[Dict[str, Any]]):
        """Difunde a la flota que un nuevo plan de navegacion ha sido trazado por Gemma 4."""
        blueprint_entry = {
            "id": f"bp-{int(datetime.utcnow().timestamp())}",
            "officer_name": officer_name,
            "mission": mission,
            "waypoints": waypoints,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Guardar en buffer circular (maximo 20)
        self.blueprints.append(blueprint_entry)
        if len(self.blueprints) > 20:
            self.blueprints.pop(0)

        await self.broadcast({
            "type": "SHARED_BLUEPRINT",
            "blueprint": blueprint_entry,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def get_latest_blueprint(self) -> Optional[Dict[str, Any]]:
        """Retorna el ultimo plano de navegacion registrado si existe."""
        return self.blueprints[-1] if self.blueprints else None

    def get_all_blueprints(self) -> List[Dict[str, Any]]:
        """Retorna el historial completo de planos registrados en la sesion."""
        return list(reversed(self.blueprints))


sonar_hub = FleetSonarManager()


@router.websocket("/ws/sonar")
async def sonar_websocket_endpoint(websocket: WebSocket, officer: str = "Cadet"):
    """
    Endpoint WebSocket de Fleet Sonar para sincronizacion LAN en tiempo real.
    Conectate desde React con: ws://<HOST_IP>:8000/api/v1/sonar/ws/sonar?officer=Daniel
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
    """Consulta HTTP rapida del estado de tripulantes activos en LAN."""
    return {
        "active_officers": len(sonar_hub.active_connections),
        "officers": [meta["officer_name"] for meta in sonar_hub.active_connections.values()],
    }


@router.get("/blueprints/latest", summary="Ultimo plano de navegacion compartido")
def get_latest_blueprint():
    """Retorna el ultimo blueprint trazado por Gemma 4 o null si no se ha trazado ninguno."""
    return {
        "latest_blueprint": sonar_hub.get_latest_blueprint()
    }


@router.get("/blueprints", summary="Historial de planos de navegacion compartidos")
def get_all_blueprints():
    """Retorna el listado cronologico inverso de planos de navegacion compartidos en la sesion."""
    return {
        "count": len(sonar_hub.blueprints),
        "blueprints": sonar_hub.get_all_blueprints()
    }

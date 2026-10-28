import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.endpoints.sonar import FleetSonarManager, sonar_hub


@pytest.fixture
def mock_websocket():
    ws = MagicMock()
    ws.accept = AsyncMock()
    ws.send_json = AsyncMock()
    return ws


@pytest.mark.asyncio
async def test_sonar_manager_connect_and_disconnect(mock_websocket):
    manager = FleetSonarManager()
    await manager.connect(mock_websocket, "Commander-Test")

    assert len(manager.active_connections) == 1
    assert manager.active_connections[mock_websocket]["officer_name"] == "Commander-Test"
    mock_websocket.accept.assert_awaited_once()

    manager.disconnect(mock_websocket)
    assert len(manager.active_connections) == 0


@pytest.mark.asyncio
async def test_sonar_blueprint_broadcast_and_history():
    manager = FleetSonarManager()
    ws1 = MagicMock()
    ws1.send_json = AsyncMock()
    ws1.accept = AsyncMock()
    await manager.connect(ws1, "Officer-Alpha")

    waypoints = [
        {"file": "app/core.py", "lines": [10, 25], "reason": "AST patch"}
    ]
    await manager.broadcast_course_plotted(
        officer_name="Officer-Alpha",
        mission="Resolve memory leak in graph solver",
        waypoints=waypoints,
    )

    latest = manager.get_latest_blueprint()
    assert latest is not None
    assert latest["officer_name"] == "Officer-Alpha"
    assert latest["mission"] == "Resolve memory leak in graph solver"
    assert len(latest["waypoints"]) == 1

    all_bps = manager.get_all_blueprints()
    assert len(all_bps) == 1
    assert all_bps[0]["mission"] == "Resolve memory leak in graph solver"


@pytest.mark.asyncio
async def test_sonar_collision_alert_direct():
    manager = FleetSonarManager()
    ws1 = MagicMock()
    ws1.send_json = AsyncMock()
    ws1.accept = AsyncMock()

    ws2 = MagicMock()
    ws2.send_json = AsyncMock()
    ws2.accept = AsyncMock()

    await manager.connect(ws1, "Officer-1")
    await manager.connect(ws2, "Officer-2")

    # Officer 1 navigates to auth.py
    await manager.handle_navigation(ws1, "src/auth.py", issue_id="ISSUE-101")
    # Officer 2 navigates to exact same file
    await manager.handle_navigation(ws2, "src/auth.py", issue_id="ISSUE-102")

    # Check that COLLISION_ALERT was sent
    calls = [call.args[0] for call in ws1.send_json.call_args_list if call.args]
    collision_events = [c for c in calls if c.get("type") == "COLLISION_ALERT"]
    assert len(collision_events) >= 1
    assert collision_events[0]["severity"] == "CRITICAL"


def test_sonar_rest_endpoints():
    client = TestClient(app)

    res_status = client.get("/api/v1/sonar/status")
    assert res_status.status_code == 200
    data_status = res_status.json()
    assert "active_officers" in data_status

    res_latest = client.get("/api/v1/sonar/blueprints/latest")
    assert res_latest.status_code == 200
    data_latest = res_latest.json()
    assert "latest_blueprint" in data_latest

    res_list = client.get("/api/v1/sonar/blueprints")
    assert res_list.status_code == 200
    data_list = res_list.json()
    assert "count" in data_list
    assert "blueprints" in data_list

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db

client = TestClient(app)


def setup_module():
    init_db()


def test_chat_sessions_lifecycle():
    # 1. Crear una nueva sesion de chat
    payload = {
        "title": "Auditoria de modularidad y ciclos",
        "source": "cli",
        "model": "qwen2.5-coder:1.5b",
        "tier": "light",
        "messages": [
            {"role": "user", "content": "analiza la modularidad de este repo"},
            {"role": "assistant", "content": "Se detectaron 2 modulos con alto acoplamiento."},
        ]
    }
    res = client.post("/api/v1/sessions/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == payload["title"]
    assert data["source"] == "cli"
    assert len(data["messages"]) == 2
    session_id = data["id"]

    # 2. Listar sesiones
    list_res = client.get("/api/v1/sessions/")
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    found = next((s for s in items if s["id"] == session_id), None)
    assert found is not None
    assert found["messages_count"] == 2

    # 3. Obtener detalle de la sesion
    detail_res = client.get(f"/api/v1/sessions/{session_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["id"] == session_id
    assert len(detail["messages"]) == 2

    # 4. Actualizar la sesion agregando mensajes
    update_payload = {
        "title": "Auditoria de modularidad y ciclos (actualizada)",
        "source": "cli",
        "model": "qwen2.5-coder:1.5b",
        "tier": "light",
        "messages": [
            {"role": "user", "content": "analiza la modularidad de este repo"},
            {"role": "assistant", "content": "Se detectaron 2 modulos con alto acoplamiento."},
            {"role": "user", "content": "/cycles"},
            {"role": "assistant", "content": "Cero dependencias circulares detectadas."}
        ]
    }
    update_res = client.put(f"/api/v1/sessions/{session_id}", json=update_payload)
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert len(updated_data["messages"]) == 4
    assert updated_data["title"] == "Auditoria de modularidad y ciclos (actualizada)"

    # 5. Eliminar la sesion
    del_res = client.delete(f"/api/v1/sessions/{session_id}")
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # 6. Comprobar que ya no existe (404)
    check_res = client.get(f"/api/v1/sessions/{session_id}")
    assert check_res.status_code == 404

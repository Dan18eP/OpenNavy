from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_assessment_evaluate_opportunity():
    payload = {
        "proyecto": "Asistente de Triage Inteligente",
        "equipo": "Equipo Alpha",
        "problema": "Los tickets tardan 12 minutos en clasificarse a mano.",
        "situacion": "Clasificación manual con demoras.",
        "resultado": "Clasificar automáticamente y priorizar incidentes.",
        "dimension": "Tiempo",
        "metrica": "Minutos por ticket",
        "meta": "Reducir a 5 min",
        "cap_reglas": "Sí",
        "cap_prediccion": "Sí",
        "cap_comprension": "Sí",
        "cap_generacion": "Sí",
        "cap_consulta": "Sí",
        "cap_accion": "No",
        "cap_autonomia": "No",
        "suficiencia": "No",
        "solucion_simple": "Reglas por palabra clave que no interpretan texto libre",
        "info_necesaria": "Histórico de tickets y base de conocimiento",
        "info_existe": "Sí",
        "info_accesible": "Sí",
        "info_confiable": "Sí",
        "info_sensible": "Sí",
        "autonomia_nivel": "Recomienda",
        "riesgo_desc": "Clasificar erróneamente un ticket crítico",
        "riesgo_nivel": "Medio",
        "hipotesis": "Requiere comprensión y predicción para triage donde reglas no bastan."
    }
    response = client.post("/api/v1/assessment/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "op"
    assert data["title"] == "OPORTUNIDAD POTENCIAL DE IA"
    assert len(data["why"]) >= 2


def test_assessment_evaluate_conventional_automation():
    payload = {
        "proyecto": "Script Validador de Nombres",
        "cap_reglas": "Sí",
        "cap_prediccion": "No",
        "cap_comprension": "No",
        "cap_generacion": "No",
        "cap_consulta": "No",
        "cap_accion": "No",
        "cap_autonomia": "No",
        "suficiencia": "Sí",
        "solucion_simple": "Expresiones regulares fijas"
    }
    response = client.post("/api/v1/assessment/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "auto"
    assert data["title"] == "AUTOMATIZACIÓN CONVENCIONAL PODRÍA SER SUFICIENTE"


def test_assessment_evaluate_to_validate():
    payload = {
        "proyecto": "Proyecto Incompleto",
        "cap_reglas": "Por validar",
        "cap_prediccion": "Por validar",
        "suficiencia": "Por validar"
    }
    response = client.post("/api/v1/assessment/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "val"
    assert data["title"] == "POR VALIDAR"


def test_assessment_list():
    response = client.get("/api/v1/assessment/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

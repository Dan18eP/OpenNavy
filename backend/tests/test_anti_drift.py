import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.anti_drift_service import AntiDriftService, anti_drift_service


def test_blast_radius_calculation():
    service = AntiDriftService()
    # Grafo de importaciones:
    # service_a -> core_config
    # service_b -> core_config
    # api_endpoint -> service_a
    adjacency = {
        "app/services/service_a.py": ["app/core/config.py"],
        "app/services/service_b.py": ["app/core/config.py"],
        "app/api/endpoints/user.py": ["app/services/service_a.py"],
    }

    # Si modificamos config.py
    result = service.calculate_blast_radius(adjacency, ["app/core/config.py"])
    assert result["total_affected_count"] >= 2
    assert "app/services/service_a.py" in result["direct_dependents"]
    assert "app/services/service_b.py" in result["direct_dependents"]
    assert "app/api/endpoints/user.py" in result["indirect_dependents"]
    assert result["severity"] in ("MEDIUM", "HIGH")


def test_hexagonal_layer_drift_validation():
    service = AntiDriftService()

    # Violacion: Dominio importando de API
    violations_1 = service.validate_layer_drift(
        source_file="app/domain/entities.py",
        imported_modules=["app/api/v1/endpoints/course.py"]
    )
    assert len(violations_1) == 1
    assert violations_1[0]["severity"] == "CRITICAL"
    assert "Domain cannot import from Api" in violations_1[0]["rule"]

    # Violacion: Servicio de aplicacion importando API
    violations_2 = service.validate_layer_drift(
        source_file="app/services/auth_service.py",
        imported_modules=["app/api/v1/endpoints/sonar.py"]
    )
    assert len(violations_2) == 1
    assert violations_2[0]["severity"] == "HIGH"

    # Caso valido: Dominio importando otro submodulo de dominio
    violations_clean = service.validate_layer_drift(
        source_file="app/domain/order.py",
        imported_modules=["app/domain/customer.py"]
    )
    assert len(violations_clean) == 0


def test_anti_drift_course_evaluation():
    service = AntiDriftService()
    waypoints = [
        {"file": "app/core/config.py", "lines": [10, 20], "reason": "Config update"}
    ]
    evaluation = service.evaluate_course_drift(
        repo_name="TestRepo",
        waypoints=waypoints,
        repo_path="backend/app/core"
    )

    assert "drift_risk" in evaluation
    assert "blast_radius" in evaluation
    assert "reef_warnings" in evaluation
    assert isinstance(evaluation["reef_warnings"], list)


def test_topography_and_drift_endpoints():
    client = TestClient(app)

    # 1. Endpoint de Topografia
    res_topo = client.get("/api/v1/repos/local-demo-repo/topography")
    assert res_topo.status_code == 200
    topo_data = res_topo.json()
    assert "files" in topo_data
    assert "scc_cycles" in topo_data
    assert "adjacency" in topo_data

    # 2. Endpoint de Evaluacion de Deriva
    payload = {
        "waypoints": [
            {"file": "backend/app/core/config.py", "lines": [15, 30], "reason": "Settings adjustment"}
        ]
    }
    res_eval = client.post("/api/v1/repos/local-demo-repo/drift/evaluate", json=payload)
    assert res_eval.status_code == 200
    eval_data = res_eval.json()
    assert "evaluation" in eval_data
    assert "drift_risk" in eval_data["evaluation"]
    assert "blast_radius" in eval_data["evaluation"]


def test_course_plot_endpoint_enriched_with_drift():
    client = TestClient(app)
    payload = {
        "repo_id": "test-repo-anti-drift",
        "mission": "Fix CORS security header leakage and token expiration",
        "officer_name": "Lieutenant-Test",
    }
    res = client.post("/api/v1/course/plot", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "waypoints" in data
    assert len(data["waypoints"]) >= 1
    assert "drift_risk" in data
    assert "blast_radius" in data
    assert "reef_warnings" in data

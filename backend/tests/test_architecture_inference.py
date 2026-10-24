import pytest
from pathlib import Path
from app.analyzers.architecture_detector import ArchitecturePatternDetector
from app.agents.nodes.architecture_inference_node import architecture_inference_node
from app.schemas.state import FileNode, AnalysisState
from app.agents.graph import praxia_graph


def test_classify_architectural_layers():
    detector = ArchitecturePatternDetector()

    assert detector.classify_layer("src/domain/entities/user.py") == "domain"
    assert detector.classify_layer("src/core/domain/order.go") == "domain"
    assert detector.classify_layer("app/application/usecases/create_user.ts") == "application"
    assert detector.classify_layer("internal/services/payment_service.go") == "application"
    assert detector.classify_layer("src/infrastructure/database/postgres_repo.py") == "infrastructure"
    assert detector.classify_layer("src/adapters/db/mongo.ts") == "infrastructure"
    assert detector.classify_layer("app/api/v1/endpoints/users.py") == "presentation"
    assert detector.classify_layer("controllers/order_controller.js") == "presentation"


def test_infer_clean_architecture_pattern():
    detector = ArchitecturePatternDetector()
    file_paths = [
        "src/domain/entities/order.ts",
        "src/domain/repositories/order_repository.ts",
        "src/application/use_cases/create_order.ts",
        "src/infrastructure/database/typeorm_order_repo.ts",
        "src/api/controllers/order_controller.ts",
    ]
    layers_map = {
        "domain": ["src/domain/entities/order.ts", "src/domain/repositories/order_repository.ts"],
        "application": ["src/application/use_cases/create_order.ts"],
        "infrastructure": ["src/infrastructure/database/typeorm_order_repo.ts"],
        "presentation": ["src/api/controllers/order_controller.ts"],
    }

    pattern, confidence = detector.infer_pattern(file_paths, layers_map)
    assert pattern == "Clean Architecture"
    assert confidence > 0.6


def test_infer_hexagonal_ports_and_adapters_pattern():
    detector = ArchitecturePatternDetector()
    file_paths = [
        "src/domain/model/account.java",
        "src/ports/inbound/deposit_usecase.java",
        "src/ports/outbound/account_port.java",
        "src/adapters/driving/web/account_controller.java",
        "src/adapters/driven/persistence/account_repository.java",
    ]
    layers_map = {
        "domain": ["src/domain/model/account.java"],
        "application": ["src/ports/inbound/deposit_usecase.java"],
        "infrastructure": ["src/adapters/driven/persistence/account_repository.java"],
        "presentation": ["src/adapters/driving/web/account_controller.java"],
    }

    pattern, confidence = detector.infer_pattern(file_paths, layers_map)
    assert "Ports & Adapters" in pattern
    assert confidence > 0.5


def test_detect_dependency_rule_violation():
    """Dominio importando directamente infraestructura o presentación viola la Regla de Dependencia."""
    detector = ArchitecturePatternDetector()
    root = Path("/dummy/repo")

    # Archivo de dominio que importa la base de datos
    node_domain = FileNode(
        path="src/domain/entities/user.py",
        language="python",
        lines_of_code=20,
        imports=["src.infrastructure.database.db"],
    )
    # Archivo de infraestructura
    node_infra = FileNode(
        path="src/infrastructure/database/db.py",
        language="python",
        lines_of_code=30,
        imports=[],
    )

    adjacency_list = {
        "src/domain/entities/user": ["src/infrastructure/database/db"],
        "src/infrastructure/database/db": [],
    }

    analysis = detector.analyze_architecture([node_domain, node_infra], adjacency_list, root)

    assert analysis["dependency_rule_violations_count"] >= 1
    viol = analysis["dependency_rule_violations"][0]
    assert viol["severity"] == "critical"
    assert "no debe importar la capa externa" in viol["rule"]
    assert analysis["dependency_rule_compliance"] < 100.0


def test_architecture_inference_node_in_graph():
    """Verifica que architecture_inference_node se ejecute y enriquezca el AnalysisState."""
    state: AnalysisState = {
        "run_id": "test-run",
        "repo_id": "test-repo",
        "repo_url": "https://github.com/test/repo",
        "branch": "main",
        "local_path": "/tmp/test",
        "is_temporary": False,
        "languages_detected": ["python"],
        "files": [
            {
                "path": "app/domain/models.py",
                "language": "python",
                "lines_of_code": 25,
                "functions": [],
                "classes": [],
                "imports": [],
                "cyclomatic_complexity_total": 1,
                "maintainability_index": 80.0,
            },
            {
                "path": "app/api/endpoints.py",
                "language": "python",
                "lines_of_code": 30,
                "functions": [],
                "classes": [],
                "imports": ["app.domain.models"],
                "cyclomatic_complexity_total": 1,
                "maintainability_index": 80.0,
            }
        ],
        "static_metrics": {},
        "complexity_findings": [],
        "solid_violations": [],
        "architecture_diff": {
            "graph": {"app/api/endpoints": ["app/domain/models"], "app/domain/models": []},
            "has_cycles": False,
            "circular_dependencies": [],
            "layer_violations": [],
        },
        "dependencies": {},
        "detected_secrets": [],
        "rag_context": [],
        "evaluation_report": {},
        "generated_docs": [],
        "offline_mode": False,
        "errors": [],
        "retry_count": 0,
        "current_step": "static_analysis_completed",
    }

    result = architecture_inference_node(state)
    assert result["current_step"] == "architecture_inference_completed"
    assert "architecture_profile" in result
    profile = result["architecture_profile"]
    assert "dominant_pattern" in profile
    assert profile["dependency_rule_compliance"] == 100.0


def test_graph_compiles_with_architecture_inference():
    """Asegura que el grafo compile correctamente con el nodo architecture_inference."""
    assert praxia_graph is not None
    node_names = list(praxia_graph.nodes.keys())
    assert "architecture_inference" in node_names
    assert "static_analysis" in node_names
    assert "rag_retrieval" in node_names

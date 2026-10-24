from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import Base
from app.models.entities import (
    Repo,
    AnalysisRun,
    Metric,
    Finding,
    ArchitectureDiff,
    GeneratedDoc,
    KnowledgeChunk,
    TriggerType,
    RunStatus,
    SeverityLevel,
)
from app.schemas.state import AnalysisState, FileNode, FunctionMetadata
from app.schemas.api import RepoCreate, AnalysisCreateRequest


def test_settings_loaded():
    assert settings.PROJECT_NAME == "Praxia - AI Code Review & Live Docs"
    assert "maintainability_index" in settings.CRITERIA_WEIGHTS
    assert "cyclomatic_complexity" in settings.CRITERIA_WEIGHTS
    assert "dependency_version_control" in settings.CRITERIA_WEIGHTS
    assert sum(settings.CRITERIA_WEIGHTS.values()) == pytest.approx(1.0, 0.01)


def test_knowledge_base_files_exist():
    kb_path = Path(settings.KNOWLEDGE_BASE_PATH)
    assert kb_path.exists(), f"Knowledge base path does not exist: {kb_path}"

    expected_criteria = [
        "maintainability-index.md",
        "cyclomatic-complexity.md",
        "code-duplication.md",
        "test-coverage.md",
        "solid-principles.md",
        "clean-code.md",
        "architecture-guidelines.md",
        "defect-density.md",
        "change-failure-rate.md",
        "dependency-version-control.md",
    ]

    criteria_dir = kb_path / "criteria"
    assert criteria_dir.exists()
    for doc in expected_criteria:
        file_path = criteria_dir / doc
        assert file_path.exists(), f"Missing criteria doc: {doc}"
        assert file_path.stat().st_size > 100, f"Criteria doc is too small/empty: {doc}"

    standards_dir = kb_path / "team-standards"
    assert standards_dir.exists()
    assert (standards_dir / "naming-conventions.md").exists()
    assert (standards_dir / "layering-rules.md").exists()


def test_database_models_and_relationships():
    # Usar SQLite en memoria para tests
    test_engine = create_engine("sqlite:///:memory:")
    TestSession = sessionmaker(bind=test_engine)
    Base.metadata.create_all(test_engine)

    session = TestSession()

    # 1. Crear Repo
    repo = Repo(
        url="https://github.com/example/demo-app",
        name="demo-app",
        default_branch="main",
    )
    session.add(repo)
    session.commit()
    assert repo.id is not None

    # 2. Crear AnalysisRun
    run = AnalysisRun(
        repo_id=repo.id,
        commit_sha="a1b2c3d4e5",
        branch="main",
        triggered_by=TriggerType.MANUAL.value,
        status=RunStatus.COMPLETED.value,
        global_score=85.5,
    )
    session.add(run)
    session.commit()
    assert run.id is not None

    # 3. Crear Metric
    metric = Metric(
        run_id=run.id,
        criterio="cyclomatic_complexity",
        valor=6.2,
        umbral_config=10.0,
        severidad=SeverityLevel.INFO.value,
        detalles={"max_function_complexity": 9},
    )
    session.add(metric)

    # 4. Crear Finding
    finding = Finding(
        run_id=run.id,
        file_path="src/services/payment.py",
        function_name="process_payment",
        line_number=42,
        criterio="solid_principles",
        veredicto="violacion",
        explicacion="Mezcla validación y persistencia directa.",
        rag_source="solid-principles.md#single-responsibility",
        severidad=SeverityLevel.HIGH.value,
        sugerencia="Extraer PaymentRepository como colaborador.",
    )
    session.add(finding)

    # 5. Crear ArchitectureDiff
    arch_diff = ArchitectureDiff(
        run_id=run.id,
        resumen="Se agregaron nuevas dependencias de capa de dominio.",
        dependencias_nuevas=["payment -> notification"],
        dependencias_rotas=[],
        ciclos_detectados=[],
    )
    session.add(arch_diff)

    # 6. Crear KnowledgeChunk
    chunk = KnowledgeChunk(
        doc_path="criteria/solid-principles.md",
        criterio="solid_principles",
        tipo="regla",
        lenguaje_aplicable="all",
        contenido="Single Responsibility Principle: Una clase debe tener una sola razón para cambiar.",
    )
    session.add(chunk)

    session.commit()

    # Validar relaciones
    queried_repo = session.query(Repo).filter_by(id=repo.id).first()
    assert len(queried_repo.runs) == 1
    assert queried_repo.runs[0].global_score == 85.5
    assert len(queried_repo.runs[0].metrics) == 1
    assert len(queried_repo.runs[0].findings) == 1
    assert queried_repo.runs[0].architecture_diff is not None
    assert queried_repo.runs[0].architecture_diff.resumen == "Se agregaron nuevas dependencias de capa de dominio."

    session.close()


def test_pydantic_schemas_and_state():
    # Validar esquemas DTO
    repo_dto = RepoCreate(url="https://github.com/my-org/my-project")
    assert repo_dto.url == "https://github.com/my-org/my-project"
    assert repo_dto.default_branch == "main"

    # Validar FileNode y FunctionMetadata
    func = FunctionMetadata(
        name="calculate_discount",
        start_line=10,
        end_line=25,
        lines_of_code=15,
        parameters_count=2,
        cyclomatic_complexity=3,
        nesting_depth=1,
    )
    node = FileNode(
        path="src/discount.py",
        language="python",
        lines_of_code=50,
        functions=[func],
        cyclomatic_complexity_total=3,
        maintainability_index=78.4,
    )
    assert node.functions[0].name == "calculate_discount"
    assert node.maintainability_index == 78.4

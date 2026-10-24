import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.entities import Repo, AnalysisRun, Metric, GeneratedDoc, ArchitectureDiff
from app.core.seeder import seed_opennavy_repo


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


def test_seed_opennavy_repo_creates_entities(in_memory_db):
    # Verificar base vacia
    assert in_memory_db.query(Repo).count() == 0

    # Ejecutar seed
    seed_opennavy_repo(in_memory_db)

    # Verificar que se creo el repositorio OpenNavy
    repo = in_memory_db.query(Repo).filter_by(name="OpenNavy").first()
    assert repo is not None
    assert repo.default_branch == "develop"

    # Verificar que se creo el AnalysisRun inicial
    run = in_memory_db.query(AnalysisRun).filter_by(repo_id=repo.id).first()
    assert run is not None
    assert run.status == "completed"
    assert run.global_score >= 90.0

    # Verificar metricas
    metrics = in_memory_db.query(Metric).filter_by(run_id=run.id).all()
    assert len(metrics) >= 5

    # Verificar ADRs reales cargados desde docs/adr/
    adrs = in_memory_db.query(GeneratedDoc).filter_by(repo_id=repo.id).all()
    assert len(adrs) >= 4
    assert any("0001" in doc.path for doc in adrs)

    # Verificar arquitectura sin ciclos
    arch = in_memory_db.query(ArchitectureDiff).filter_by(run_id=run.id).first()
    assert arch is not None
    assert len(arch.ciclos_detectados) == 0


def test_seed_opennavy_repo_idempotency(in_memory_db):
    # Llamar dos veces no duplica el repositorio
    seed_opennavy_repo(in_memory_db)
    seed_opennavy_repo(in_memory_db)

    assert in_memory_db.query(Repo).filter_by(name="OpenNavy").count() == 1

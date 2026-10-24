import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    JSON,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class TriggerType(str, enum.Enum):
    MANUAL = "manual"
    WEBHOOK = "webhook"
    CRON = "cron"


class RunStatus(str, enum.Enum):
    PENDING = "pending"
    CLONING = "cloning"
    PARSING = "parsing"
    STATIC_ANALYSIS = "static_analysis"
    RAG_EVALUATION = "rag_evaluation"
    GENERATING_DOCS = "generating_docs"
    COMPLETED = "completed"
    FAILED = "failed"


class SeverityLevel(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"


class DocType(str, enum.Enum):
    ADR = "adr"
    MODULE_DOC = "module_doc"
    SUMMARY = "summary"


class Repo(Base):
    __tablename__ = "repos"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    url = Column(String(512), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    default_branch = Column(String(100), default="main")
    connected_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    runs = relationship("AnalysisRun", back_populates="repo", cascade="all, delete-orphan")
    generated_docs = relationship("GeneratedDoc", back_populates="repo", cascade="all, delete-orphan")


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    repo_id = Column(String(36), ForeignKey("repos.id"), nullable=False, index=True)
    commit_sha = Column(String(64), nullable=True)
    branch = Column(String(100), default="main")
    triggered_by = Column(String(50), default=TriggerType.MANUAL.value)
    status = Column(String(50), default=RunStatus.PENDING.value)
    global_score = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    # Relaciones
    repo = relationship("Repo", back_populates="runs")
    metrics = relationship("Metric", back_populates="run", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="run", cascade="all, delete-orphan")
    architecture_diff = relationship("ArchitectureDiff", back_populates="run", uselist=False, cascade="all, delete-orphan")


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    run_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=False, index=True)
    criterio = Column(String(100), nullable=False)
    valor = Column(Float, nullable=False)
    umbral_config = Column(Float, nullable=True)
    severidad = Column(String(50), default=SeverityLevel.INFO.value)
    detalles = Column(JSON, nullable=True)  # Detalles adicionales o desglose por archivo

    run = relationship("AnalysisRun", back_populates="metrics")


class Finding(Base):
    __tablename__ = "findings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    run_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=False, index=True)
    file_path = Column(String(512), nullable=False)
    function_name = Column(String(255), nullable=True)
    line_number = Column(Integer, nullable=True)
    criterio = Column(String(100), nullable=False)
    veredicto = Column(String(100), nullable=False)  # ej. violacion, advertencia, sugerencia
    explicacion = Column(Text, nullable=False)
    rag_source = Column(String(255), nullable=True)  # Archivo/sección RAG citado
    severidad = Column(String(50), default=SeverityLevel.HIGH.value)
    sugerencia = Column(Text, nullable=True)

    run = relationship("AnalysisRun", back_populates="findings")


class ArchitectureDiff(Base):
    __tablename__ = "architecture_diffs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    run_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=False, unique=True)
    resumen = Column(Text, nullable=False)
    dependencias_nuevas = Column(JSON, default=list)
    dependencias_rotas = Column(JSON, default=list)
    ciclos_detectados = Column(JSON, default=list)

    run = relationship("AnalysisRun", back_populates="architecture_diff")


class GeneratedDoc(Base):
    __tablename__ = "generated_docs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    repo_id = Column(String(36), ForeignKey("repos.id"), nullable=False, index=True)
    tipo = Column(String(50), default=DocType.ADR.value)
    path = Column(String(512), nullable=False)
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    vector_indexed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    repo = relationship("Repo", back_populates="generated_docs")


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    doc_path = Column(String(512), nullable=False)
    criterio = Column(String(100), nullable=False, index=True)
    tipo = Column(String(50), nullable=False)  # regla, umbral, ejemplo, directriz
    lenguaje_aplicable = Column(String(50), default="all")
    contenido = Column(Text, nullable=False)
    version = Column(String(20), default="1.0")
    created_at = Column(DateTime, default=datetime.utcnow)


class AIOpportunityAssessment(Base):
    __tablename__ = "ai_opportunity_assessments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_name = Column(String(255), nullable=False)
    team_name = Column(String(255), nullable=True)
    problem_statement = Column(Text, nullable=True)
    current_situation = Column(Text, nullable=True)
    expected_result = Column(Text, nullable=True)
    value_dimension = Column(String(100), nullable=True)
    metric_name = Column(String(255), nullable=True)
    target_goal = Column(String(255), nullable=True)
    cap_reglas = Column(String(50), default="Por validar")
    cap_prediccion = Column(String(50), default="Por validar")
    cap_comprension = Column(String(50), default="Por validar")
    cap_generacion = Column(String(50), default="Por validar")
    cap_consulta = Column(String(50), default="Por validar")
    cap_accion = Column(String(50), default="Por validar")
    cap_autonomia = Column(String(50), default="Por validar")
    simplicity_sufficient = Column(String(50), default="Por validar")
    simplest_solution = Column(Text, nullable=True)
    data_needed = Column(Text, nullable=True)
    data_exists = Column(String(50), default="Por validar")
    data_accessible = Column(String(50), default="Por validar")
    data_reliable = Column(String(50), default="Por validar")
    data_sensitive = Column(String(50), default="Por validar")
    autonomy_level = Column(String(50), default="Recomienda")
    initial_risk_description = Column(Text, nullable=True)
    initial_risk_level = Column(String(50), default="Medio")
    hypothesis = Column(Text, nullable=True)
    verdict_key = Column(String(50), nullable=False)
    verdict_title = Column(String(255), nullable=False)
    verdict_lead = Column(Text, nullable=False)
    verdict_detail = Column(Text, nullable=True)
    verdict_reasons = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    repo_id = Column(String(36), ForeignKey("repos.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    source = Column(String(50), default="cli")  # "cli" | "web"
    model = Column(String(100), default="qwen2.5-coder:1.5b")
    tier = Column(String(50), default="light")
    messages = Column(JSON, default=list)  # lista de dicts: {role, content, citations, timestamp, ...}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)




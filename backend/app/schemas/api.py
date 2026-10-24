from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


# Repositorios
class RepoCreate(BaseModel):
    url: str = Field(..., description="URL pública o accesible de Git (GitHub, GitLab, etc.)")
    name: Optional[str] = Field(None, description="Nombre descriptivo del repositorio")
    default_branch: str = Field("main", description="Rama por defecto a analizar")


class RepoResponse(BaseModel):
    id: str
    url: str
    name: str
    default_branch: str
    connected_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Análisis
class AnalysisCreateRequest(BaseModel):
    repo_url: str = Field(..., description="URL del repositorio Git")
    branch: Optional[str] = Field("main", description="Rama específica a analizar")


class AnalysisJobResponse(BaseModel):
    job_id: str
    repo_id: str
    status: str
    message: str


class MetricResponse(BaseModel):
    id: str
    criterio: str
    valor: float
    umbral_config: Optional[float] = None
    severidad: str
    detalles: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class FindingResponse(BaseModel):
    id: str
    file_path: str
    function_name: Optional[str] = None
    line_number: Optional[int] = None
    criterio: str
    veredicto: str
    explicacion: str
    rag_source: Optional[str] = None
    severidad: str
    sugerencia: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ArchitectureSummaryResponse(BaseModel):
    run_id: str
    resumen: str
    dependencias_nuevas: List[str] = []
    dependencias_rotas: List[str] = []
    ciclos_detectados: List[str] = []


class AnalysisRunDetailResponse(BaseModel):
    id: str
    repo_id: str
    commit_sha: Optional[str] = None
    branch: str
    triggered_by: str
    status: str
    global_score: Optional[float] = None
    error_message: Optional[str] = None
    started_at: datetime
    finished_at: Optional[datetime] = None
    metrics: List[MetricResponse] = []
    findings: List[FindingResponse] = []
    architecture_diff: Optional[ArchitectureSummaryResponse] = None

    model_config = ConfigDict(from_attributes=True)


# Chat RAG
class DeepCodeCitation(BaseModel):
    file_path: str
    start_line: int
    end_line: int
    label: str


class ChatRequest(BaseModel):
    message: str = Field(..., description="Pregunta del desarrollador sobre el repo o sus métricas")
    context_filters: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    response: str
    cited_sources: List[str] = []
    citations: List[DeepCodeCitation] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ── Schemas de la Sesión 01: AI Opportunity Assessment ─────────────────
class AssessmentData(BaseModel):
    proyecto: Optional[str] = "Proyecto de Software"
    equipo: Optional[str] = None
    problema: Optional[str] = None
    situacion: Optional[str] = None
    resultado: Optional[str] = None
    dimension: Optional[str] = "Tiempo"
    metrica: Optional[str] = None
    meta: Optional[str] = None

    cap_reglas: Optional[str] = "Por validar"
    cap_prediccion: Optional[str] = "Por validar"
    cap_comprension: Optional[str] = "Por validar"
    cap_generacion: Optional[str] = "Por validar"
    cap_consulta: Optional[str] = "Por validar"
    cap_accion: Optional[str] = "Por validar"
    cap_autonomia: Optional[str] = "Por validar"

    suficiencia: Optional[str] = "Por validar"
    solucion_simple: Optional[str] = None

    info_necesaria: Optional[str] = None
    info_existe: Optional[str] = "Por validar"
    info_accesible: Optional[str] = "Por validar"
    info_confiable: Optional[str] = "Por validar"
    info_sensible: Optional[str] = "Por validar"

    autonomia_nivel: Optional[str] = "Recomienda"
    riesgo_desc: Optional[str] = None
    riesgo_nivel: Optional[str] = "Medio"
    hipotesis: Optional[str] = None


class AssessmentVerdictResponse(BaseModel):
    id: Optional[str] = None
    key: str
    tag: str
    title: str
    lead: str
    detail: Optional[str] = None
    why: List[str] = []
    raw_data: Dict[str, Any] = {}
    created_at: Optional[datetime] = None


# ── Schemas DeepCode Explorer (DeepWiki) ───────────────────────────────
class FileTreeNode(BaseModel):
    name: str
    path: str
    type: str  # "file" o "directory"
    size: Optional[int] = 0
    language: Optional[str] = None
    children: Optional[List["FileTreeNode"]] = None


class DeepQueryRequest(BaseModel):
    message: str = Field(..., description="Pregunta del desarrollador")
    active_file: Optional[str] = Field(None, description="Archivo actualmente abierto en el visor")


class DeepQueryResponse(BaseModel):
    response: str
    citations: List[DeepCodeCitation] = []
    recommended_refactor: Optional[str] = None
    cited_rag_sources: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ── Schemas de Gestión y Reanudación de Sesiones (/resume) ────────────
class ChatSessionItem(BaseModel):
    id: str
    repo_id: Optional[str] = None
    title: str
    source: str
    model: str
    tier: str
    messages_count: int = 0
    created_at: datetime
    updated_at: datetime


class ChatSessionDetail(BaseModel):
    id: str
    repo_id: Optional[str] = None
    title: str
    source: str
    model: str
    tier: str
    messages: List[Dict[str, Any]] = []
    created_at: datetime
    updated_at: datetime


class ChatSessionCreate(BaseModel):
    repo_id: Optional[str] = None
    title: str
    source: str = "cli"
    model: str = "qwen2.5-coder:1.5b"
    tier: str = "light"
    messages: List[Dict[str, Any]] = []



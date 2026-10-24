from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field


class FunctionMetadata(BaseModel):
    name: str
    start_line: int
    end_line: int
    lines_of_code: int
    parameters_count: int
    cyclomatic_complexity: int
    nesting_depth: int
    docstring: Optional[str] = None


class ClassMetadata(BaseModel):
    name: str
    start_line: int
    end_line: int
    methods_count: int
    docstring: Optional[str] = None


class FileNode(BaseModel):
    path: str
    language: str
    lines_of_code: int
    functions: List[FunctionMetadata] = Field(default_factory=list)
    classes: List[ClassMetadata] = Field(default_factory=list)
    imports: List[str] = Field(default_factory=list)
    cyclomatic_complexity_total: int = 0
    maintainability_index: float = 100.0
    raw_content: Optional[str] = None


class FindingItem(BaseModel):
    file: str
    function: Optional[str] = None
    line: Optional[int] = None
    criterio: str
    veredicto: str  # violacion, advertencia, sugerencia, optimo
    explicacion: str
    fragmento_rag_citado: Optional[str] = None
    severidad: str = "high"  # info, warning, high, critical
    sugerencia: Optional[str] = None


class MetricItem(BaseModel):
    criterio: str
    valor: float
    umbral: Optional[float] = None
    severidad: str = "info"
    detalles: Optional[Dict[str, Any]] = None


class GeneratedDocItem(BaseModel):
    tipo: str  # adr, module_doc, summary
    path: str
    titulo: str
    contenido: str


class RagChunk(BaseModel):
    criterio: str
    tipo: str
    doc_name: str
    content: str
    score: float = 0.0


class ArchitectureFinding(BaseModel):
    file: str
    function: Optional[str] = None
    line: Optional[int] = 1
    criterio: str
    veredicto: str  # violacion, advertencia, sugerencia, optimo
    explicacion: str
    fragmento_rag_citado: Optional[str] = None
    severidad: str = "high"  # info, warning, high, critical
    sugerencia: Optional[str] = None


class AssessmentItem(BaseModel):
    modulo: str
    evaluacion_ia: str
    justificacion: str
    roi_estimado: str


# Contrato enriquecido para nodos atomicos de OpenNavy (HU-CORE-01)
class OpenNavyGraphState(TypedDict):
    pass
PraxiaGraphState = OpenNavyGraphState
class _OldPraxiaGraphState(TypedDict):
    run_id: str
    repo_id: str
    repo_url: str
    branch: str
    local_path: str
    is_temporary: Optional[bool]
    languages_detected: List[str]
    files: List[Dict[str, Any]]
    deterministic_metrics: Dict[str, Any]
    static_metrics: Dict[str, Any]
    complexity_findings: List[Dict[str, Any]]
    architecture_profile: Optional[Dict[str, Any]]
    architecture_diff: Optional[Dict[str, Any]]
    dependencies: Optional[Dict[str, Any]]
    detected_secrets: Optional[List[Dict[str, Any]]]
    sanitized_code: Optional[Dict[str, str]]
    rag_context: List[Dict[str, Any]]
    findings: List[Dict[str, Any]]
    solid_violations: List[Dict[str, Any]]
    evaluation_report: Dict[str, Any]
    generated_docs: List[Dict[str, Any]]
    adrs: Optional[List[Dict[str, Any]]]
    assessment: Optional[List[Dict[str, Any]]]
    offline_mode: Optional[bool]  # Si es True, el circuito se desvía al sintetizador determinístico
    errors: List[str]
    retry_count: int
    current_step: str


# Estado tipado para el grafo de orquestación en LangGraph (Sección 6.1)
class AnalysisState(TypedDict):
    run_id: str
    repo_id: str
    repo_url: str
    branch: str
    local_path: str
    is_temporary: Optional[bool]  # True si es un clon efímero generado por Praxia
    languages_detected: List[str]
    files: List[Dict[str, Any]]  # List of FileNode dicts
    static_metrics: Dict[str, Any]
    complexity_findings: List[Dict[str, Any]]
    solid_violations: List[Dict[str, Any]]
    architecture_diff: Optional[Dict[str, Any]]
    architecture_profile: Optional[Dict[str, Any]]
    dependencies: Optional[Dict[str, Any]]
    detected_secrets: Optional[List[Dict[str, Any]]]  # Secretos detectados y enmascarados
    rag_context: List[Dict[str, Any]]  # Chunks recuperados
    evaluation_report: Dict[str, Any]  # Resumen y score global
    generated_docs: List[Dict[str, Any]]  # ADRs y docs generados
    offline_mode: Optional[bool]  # Flag de modo offline / circuit breaker activado
    errors: List[str]
    retry_count: int
    current_step: str

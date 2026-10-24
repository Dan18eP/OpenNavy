from pathlib import Path
from typing import Dict, List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Determinar raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BASE_DIR.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = "OpenNavy - Sovereign Fleet Navigator"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Base de Datos (SQLite por defecto para facilidad local, conmutable a PostgreSQL)
    DATABASE_URL: str = Field(
        default=f"sqlite:///{BASE_DIR / 'opennavy.db'}",
        description="URL de conexión SQLAlchemy para base de datos"
    )

    # Proveedor LLM preferido: "auto", "google", "openai", "ollama"
    LLM_PROVIDER: str = Field(default="ollama", description="Proveedor LLM: ollama, auto, google o openai")

    # Configuración Ollama / llama.cpp (Inferencia Local On-Premise - ADR-001 / ADR-003)
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434", description="URL base de la instancia local de Ollama / llama.cpp")
    OPENNAVY_TIER: str = Field(default="e2b", description="Perfil de hardware: e4b (razonamiento) o e2b (ultrarrápido)")
    PRAXIA_LOCAL_TIER: str = Field(default="standard", description="Alias de compatibilidad heredada para perfil local")
    OLLAMA_MODEL: str = Field(default="gemma4:e2b", description="Modelo primario de navegación Google Gemma 4")
    OLLAMA_FALLBACK_MODEL: str = Field(default="gemma4:e4b", description="Modelo secundario de contingencia")


    # Configuración Google AI Studio / Gemini
    GOOGLE_API_KEY: Optional[str] = Field(default=None, description="API Key de Google AI Studio / Gemini")
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Alias para API Key de Gemini")
    GOOGLE_MODEL: str = Field(default="gemini-1.5-flash", description="Modelo Google Gemini para evaluación y chat")

    # Configuración OpenAI
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="API Key de OpenAI")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini", description="Modelo OpenAI para evaluación")
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-large", description="Modelo de embeddings RAG")

    # Seguridad y Webhooks
    WEBHOOK_SECRET: Optional[str] = Field(default=None, description="Secreto compartido HMAC-SHA256 para GitHub Webhooks")
    GITLAB_WEBHOOK_TOKEN: Optional[str] = Field(default=None, description="Token secreto para GitLab Webhooks")

    # Rutas del Sistema
    KNOWLEDGE_BASE_PATH: Path = PROJECT_ROOT / "docs" / "knowledge_base"
    CLONE_STORAGE_PATH: Path = BASE_DIR / "temp_repos"

    # Ponderaciones de los Criterios para el Score Global de Salud (Suma = 1.00)
    CRITERIA_WEIGHTS: Dict[str, float] = {
        "maintainability_index": 0.15,
        "cyclomatic_complexity": 0.15,
        "solid_principles": 0.15,
        "code_duplication": 0.10,
        "test_coverage": 0.15,
        "architecture": 0.15,
        "clean_code": 0.05,
        "dependency_version_control": 0.10,
    }

    # Umbrales Críticos de Alerta
    CRITICAL_SCORE_THRESHOLD: float = 60.0
    HIGH_COMPLEXITY_THRESHOLD: int = 15
    LOW_MAINTAINABILITY_THRESHOLD: float = 50.0

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*"
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


settings = Settings()

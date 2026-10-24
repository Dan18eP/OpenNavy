import os
import logging
from typing import Optional, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


def get_llm(temperature: float = 0.2) -> Optional[Any]:
    """
    Retorna una instancia de LLM compatible con LangChain/LangGraph basada en la configuración.
    Soporta Ollama (Local On-Premise), Google AI Studio / Gemini y OpenAI con auto-detección de claves.
    """
    provider = settings.LLM_PROVIDER.lower()

    # 1. Prioridad: Ollama Local On-Premise (Si provider es 'ollama' o 'local' explícito)
    if provider in ("ollama", "local"):
        try:
            from app.core.ollama_client import ChatOllamaLocal
            logger.info(f"Inicializando LLM Local con Ollama (modelo: {settings.OLLAMA_MODEL}) en {settings.OLLAMA_BASE_URL}")
            return ChatOllamaLocal(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_MODEL,
                temperature=temperature,
            )
        except Exception as e:
            logger.warning(f"No se pudo inicializar ChatOllamaLocal: {e}")

    # 1b. Si provider es 'auto', intentar primero con Ollama si responde en localhost
    if provider == "auto":
        try:
            import httpx
            with httpx.Client(timeout=0.5) as client:
                resp = client.get(f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/tags")
                if resp.status_code == 200:
                    from app.core.ollama_client import ChatOllamaLocal
                    logger.info(f"Auto-detectado Ollama Local en {settings.OLLAMA_BASE_URL}")
                    return ChatOllamaLocal(
                        base_url=settings.OLLAMA_BASE_URL,
                        model=settings.OLLAMA_MODEL,
                        temperature=temperature,
                    )
        except Exception:
            pass



    google_key = settings.GOOGLE_API_KEY or settings.GEMINI_API_KEY or os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    openai_key = settings.OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY")

    # 2. Intentar con Google AI Studio / Gemini
    if (provider in ("google", "gemini", "auto")) and google_key and not google_key.startswith("sk-tu-"):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            logger.info("Inicializando LLM con Google AI Studio (Gemini)")
            return ChatGoogleGenerativeAI(
                model=settings.GOOGLE_MODEL,
                google_api_key=google_key,
                temperature=temperature,
            )
        except Exception as e:
            logger.warning(f"No se pudo inicializar ChatGoogleGenerativeAI: {e}")

    # 3. Intentar con OpenAI
    if (provider in ("openai", "auto")) and openai_key and not openai_key.startswith("sk-tu-"):
        try:
            from langchain_openai import ChatOpenAI
            logger.info("Inicializando LLM con OpenAI")
            return ChatOpenAI(
                model=settings.OPENAI_MODEL,
                api_key=openai_key,
                temperature=temperature,
            )
        except Exception as e:
            logger.warning(f"No se pudo inicializar ChatOpenAI: {e}")

    logger.info("Sin API Key de LLM configurada o válida. Se utilizará el motor de reglas y RAG interno.")
    return None

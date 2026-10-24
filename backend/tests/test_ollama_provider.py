import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage, SystemMessage

from app.core.config import settings
from app.core.llm import get_llm
from app.core.ollama_client import ChatOllamaLocal


class TestOllamaProvider:
    """Pruebas de inferencia local On-Premise con Ollama."""

    def test_ollama_client_generates_response(self):
        client = ChatOllamaLocal(base_url="http://localhost:11434", model="qwen2.5-coder:1.5b")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {
                "role": "assistant",
                "content": "Código refactorizado exitosamente sin dependencias circulares."
            }
        }
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.Client.post", return_value=mock_response) as mock_post:
            messages = [
                SystemMessage(content="Eres un revisor de arquitectura."),
                HumanMessage(content="¿Cómo desacoplar este módulo?")
            ]
            result = client.invoke(messages)

            assert result.content == "Código refactorizado exitosamente sin dependencias circulares."
            assert mock_post.called

            # Verificar que el payload hacia Ollama cumple el formato de API de chat y ADR-003
            args, kwargs = mock_post.call_args
            assert args[0] == "http://localhost:11434/api/chat"
            payload = kwargs["json"]
            assert payload["model"] == "qwen2.5-coder:1.5b"
            assert payload["stream"] is False
            assert payload["options"]["num_ctx"] == 4096
            assert payload["options"]["top_p"] == 0.9
            assert payload["options"]["temperature"] == 0.2
            assert len(payload["messages"]) == 2
            assert payload["messages"][0]["role"] == "system"
            assert payload["messages"][1]["role"] == "user"

    def test_get_llm_factory_returns_ollama_when_configured(self):
        with patch.object(settings, "LLM_PROVIDER", "ollama"), \
             patch.object(settings, "OLLAMA_BASE_URL", "http://127.0.0.1:11434"), \
             patch.object(settings, "OLLAMA_MODEL", "qwen2.5-coder:3b"):

            llm = get_llm()
            assert isinstance(llm, ChatOllamaLocal)
            assert llm.base_url == "http://127.0.0.1:11434"
            assert llm.model == "qwen2.5-coder:3b"

    def test_zero_cloud_network_requests_when_ollama_active(self):
        """Verifica que cuando LLM_PROVIDER=ollama NUNCA se invoca Google ni OpenAI."""
        with patch.object(settings, "LLM_PROVIDER", "ollama"), \
             patch.object(settings, "GOOGLE_API_KEY", "dummy-google-key"), \
             patch.object(settings, "OPENAI_API_KEY", "dummy-openai-key"), \
             patch("langchain_google_genai.ChatGoogleGenerativeAI") as mock_google, \
             patch("langchain_openai.ChatOpenAI") as mock_openai:

            llm = get_llm()
            assert isinstance(llm, ChatOllamaLocal)
            assert not mock_google.called
            assert not mock_openai.called

    def test_qwen_coder_tier_defaults_and_hardware_profile(self):
        """Valida que la configuración por defecto respete la familia qwen2.5-coder y perfiles de hardware (ADR-001/ADR-003)."""
        assert "coder" in settings.OLLAMA_MODEL
        assert settings.PRAXIA_LOCAL_TIER in ("light", "standard", "pro")


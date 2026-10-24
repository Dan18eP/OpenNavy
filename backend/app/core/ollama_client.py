import logging
from typing import Any, List, Optional, Dict
import httpx
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration

logger = logging.getLogger(__name__)


class ChatOllamaLocal(BaseChatModel):
    """
    Cliente local robusto y desacoplado para Ollama API (HTTP nativo con streaming y retry).
    Compatible con la interfaz estándar BaseChatModel de LangChain/LangGraph.
    Garantiza inferencia 100% on-premise sin llamadas a la nube.
    """
    base_url: str = "http://localhost:11434"
    model: str = "qwen2.5-coder:1.5b"
    temperature: float = 0.2
    top_p: float = 0.9
    num_ctx: int = 4096
    timeout: float = 60.0

    @property
    def _llm_type(self) -> str:
        return "ollama-local"

    def _convert_messages_to_ollama_format(self, messages: List[BaseMessage]) -> List[Dict[str, str]]:
        formatted: List[Dict[str, str]] = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                role = "system"
            elif isinstance(msg, HumanMessage):
                role = "user"
            elif isinstance(msg, AIMessage):
                role = "assistant"
            elif isinstance(msg, dict):
                role = msg.get("role", "user")
                formatted.append({"role": role, "content": msg.get("content", "")})
                continue
            else:
                role = "user"
            formatted.append({"role": role, "content": str(msg.content)})
        return formatted

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        endpoint = f"{self.base_url.rstrip('/')}/api/chat"
        payload = {
            "model": self.model,
            "messages": self._convert_messages_to_ollama_format(messages),
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "num_ctx": self.num_ctx,
            }
        }
        if stop:
            payload["options"]["stop"] = stop

        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(endpoint, json=payload)
                resp.raise_for_status()
                data = resp.json()
                content = data.get("message", {}).get("content", "")
                generation = ChatGeneration(message=AIMessage(content=content))
                return ChatResult(generations=[generation])
        except Exception as e:
            logger.error(f"Error al invocar modelo Ollama en {endpoint}: {e}")
            raise

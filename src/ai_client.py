"""
Módulo cliente de IA para FastAPI / Python con soporte de streaming y fallback.
Compatible de forma nativa con Ollama y con APIs de la nube (Google AI Studio, Groq, OpenAI).
"""

import os
from typing import AsyncGenerator, Optional
from openai import AsyncOpenAI

# Variables de entorno con valores por defecto para la hackathon
AI_SERVER_URL = os.getenv("AI_SERVER_URL", "http://localhost:11434/v1")
AI_API_KEY = os.getenv("AI_API_KEY", "ollama")
PRIMARY_MODEL = os.getenv("AI_MODEL_NAME", "gemma4:e4b")
FALLBACK_MODEL = os.getenv("AI_FALLBACK_MODEL", "gemma4:e2b")

# Cliente OpenAI asíncrono
client = AsyncOpenAI(
    base_url=AI_SERVER_URL,
    api_key=AI_API_KEY,
)


async def generate_stream(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> AsyncGenerator[str, None]:
    """
    Genera una respuesta en streaming token por token.
    Ideal para endpoints Server-Sent Events (SSE) en FastAPI.
    """
    selected_model = model or PRIMARY_MODEL
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        response_stream = await client.chat.completions.create(
            model=selected_model,
            messages=messages,
            stream=True,
            temperature=temperature,
        )

        async for chunk in response_stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    except Exception as e:
        # Si el modelo primario falla por memoria o tiempo, intenta con el de respaldo
        if selected_model != FALLBACK_MODEL:
            print(f"[AI Client] Error con {selected_model}: {e}. Cambiando a fallback {FALLBACK_MODEL}...")
            fallback_stream = await client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=messages,
                stream=True,
                temperature=temperature,
            )
            async for chunk in fallback_stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        else:
            raise e


async def generate_json(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """
    Genera una respuesta garantizada en formato JSON string.
    """
    selected_model = model or PRIMARY_MODEL
    messages = []
    sys_content = system_prompt or "Eres un asistente experto. Tu respuesta debe ser EXCLUSIVAMENTE un objeto JSON válido."
    if "json" not in sys_content.lower():
        sys_content += " Responde estrictamente en formato JSON."

    messages.append({"role": "system", "content": sys_content})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=selected_model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    return response.choices[0].message.content or "{}"

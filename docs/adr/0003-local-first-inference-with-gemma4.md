# ADR-0003: Inferencia Soberana Local-First con Google Gemma 4

## Estado
Aceptado

## Contexto
Los desarrolladores que colaboran en proyectos open source o trabajan en organizaciones bajo estrictas regulaciones de privacidad (banca, salud, defensa) no pueden enviar código fuente confidencial ni propiedad intelectual a APIs públicas en la nube (como OpenAI o Anthropic). Al mismo tiempo, el sistema requiere capacidades avanzadas de razonamiento para interpretar issues y correlacionarlos con el AST.

## Opciones Evaluadas
1. **Modelos Cloud (OpenAI GPT-4o / Claude 3.5 Sonnet):** Alta calidad de código, pero rompe el requisito de soberanía, genera costos por token y requiere conexión constante a internet.
2. **Modelos Locales de 70B+ Parámetros:** Imposibles de ejecutar en laptops de desarrollo estándar durante hackathons o sprints locales sin servidores con múltiples GPUs de alta gama.
3. **Google Gemma 4 (Variantes e4b y e2b):** Modelos de pesos abiertos, ligeros, con soporte de razonamiento nativo (<|think|>), capacidades multimodales de visión y consumo moderado de memoria (3.5 GB a 6.6 GB).

## Decision
Se adopta **Google Gemma 4** ejecutado localmente mediante **Ollama** con la siguiente jerarquía:
* **Modelo Primario:** `gemma4:e4b` (cuantización Q4_K_M). Balance óptimo de razonamiento arquitectónico, seguimiento de esquemas JSON estructurados y velocidad en CPU/GPU.
* **Modelo de Contingencia:** `gemma4:e2b`. Para dispositivos con restricciones térmicas o de memoria RAM (< 8 GB).
* **Parámetros del Servidor Host:** `OLLAMA_ORIGINS=*`, `OLLAMA_KEEP_ALIVE=-1` (para evitar descargas del modelo entre peticiones) y `OLLAMA_NUM_PARALLEL=2`.

## Consecuencias
* Positivo: Cero telemetría externa. Cumplimiento absoluto de soberanía de datos (Air-Gapped Ready).
* Positivo: Costo de inferencia cero dólares para la comunidad open source.
* Positivo: Exposición transparente del proceso de razonamiento del modelo a través de la interfaz de usuario.
* Negativo: La velocidad de generación depende del hardware de la máquina anfitriona (9 a 12 tokens/s en CPU, 30 a 50 tokens/s en GPU).

# Registro de Entrega: US-05 Motor Anti-Drift Arquitectonico y Trazador Multimodal Gemma 4

**ID de la Historia:** US-05  
**Epica:** Course Plotter & Anti Code Drift  
**Responsable:** Daniel Echeverria (Lead Architect & Backend Core)  
**Rama:** `feature/backend-anti-code-drift`  
**Fecha de Completitud:** 24 de Octubre de 2026  

---

## 1. Historia de Usuario y Criterios de Aceptacion

**Como:** Desarrollador u Oficial al mando navegando una base de codigo open source  
**Quiero:** Que el Trazador de Rumbo (Course Plotter) no solo genere waypoints a partir de texto o capturas de pantalla con Google Gemma 4 Vision, sino que valide matematicamente el riesgo de deriva arquitectonica (Anti Code Drift) extrayendo la topografia AST y los arrecifes ciclicos de Tarjan del repositorio local  
**Para:** Prevenir regresiones silenciosas, advertir sobre violaciones de capas hexagonales y alertar sobre el radio de impacto (Blast Radius) antes de fusionar codigo en las ramas principales.

### Criterios de Aceptacion Cumplidos

1. **Topografia AST y Arrecifes en Tiempo Real:** El servicio `AntiDriftService` procesa el repositorio en < 1 segundo utilizando Tree-sitter y el analizador de grafos de dependencia basado en el algoritmo de Tarjan para componentes fuertemente conexos (SCC).
2. **Evaluacion de Radio de Impacto (Blast Radius):** Se calculan los dependientes directos e indirectos de cada archivo tocado por los waypoints, asignando severidades precisas (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
3. **Validacion de Capas Hexagonales (Layer Drift):** Se aplican reglas estrictas de dominio: el nucleo de dominio no puede importar puertos ni adaptadores de infraestructura. Las violaciones se senalizan explicitamente.
4. **Integracion Multimodal con Gemma 4 Vision:** Soporte nativo para envio de imagenes en Base64 a Ollama (`gemma4:e4b` / `gemma4:e2b`), permitiendo trazado de rumbos a partir de capturas de bugs o diagramas.
5. **Streaming Asincrono No Bloqueante:** Se implemento `_agenerate` con `httpx.AsyncClient` en `OllamaChatWrapper` para evitar bloquear el event loop principal de FastAPI.
6. **Enriquecimiento del Endpoint de Rumbo (`POST /api/v1/course/plot`):** Se inyecta la topografia del repositorio en el prompt del sistema y se adjunta la evaluacion completa de deriva (`drift_risk`, `blast_radius`, `reef_warnings`) en la respuesta JSON.
7. **Nuevos Endpoints de Arquitectura:**
   - `GET /api/v1/architecture/{repo_id}/topography`: Retorna el mapa AST y resumen de arrecifes ciclicos.
   - `POST /api/v1/architecture/{repo_id}/drift/evaluate`: Permite evaluar la deriva de cualquier conjunto de waypoints de forma aislada.
8. **Pruebas Automatizadas:** Cobertura total en `backend/tests/test_anti_drift.py` y verificacion con `test_sonar_hub.py` (9 passed).

---

## 2. Detalle de Implementacion Tecnica

- **`backend/app/services/anti_drift_service.py`:**
  - `get_repo_ast_topography(repo_path)`: Extraccion y agrupacion por modulos canónicos.
  - `calculate_blast_radius(repo_path, modified_files)`: Analisis de dependencias inversas y ponderacion de severidad.
  - `validate_layer_drift(repo_path, waypoints)`: Verificacion de reglas de arquitectura limpia/hexagonal.
  - `evaluate_course_drift(repo_path, waypoints)`: Orquestacion integral de evaluacion de riesgo y recomendacion de ADR.
  - `are_modules_coupled_via_tarjan(repo_path, file_a, file_b)`: Consulta rapida para deteccion de colisiones en el Sonar.
- **`backend/app/core/ollama_client.py`:**
  - Soporte de imagenes en `_convert_messages_to_ollama_format` a traves de `additional_kwargs={"images": [...]}`.
  - Implementacion asincrona `_agenerate` con `httpx.AsyncClient` para streaming y llamadas fluidas.
- **`backend/app/api/v1/endpoints/course.py`:**
  - Inyeccion de topografia AST y advertencias de Tarjan en el prompt para Gemma 4.
  - Soporte para recepcion de `image_base64` en el payload de `CoursePlotRequest`.
  - Enriquecimiento de la respuesta con `drift_risk`, `blast_radius` y `reef_warnings`.
- **`backend/app/api/v1/endpoints/sonar.py`:**
  - Verificacion de acoplamiento de modulos contra `AntiDriftService.are_modules_coupled_via_tarjan` para alertas del radar.
- **`backend/app/api/v1/endpoints/architecture.py`:**
  - Rutas REST `/topography` y `/drift/evaluate` para analisis arquitectonico bajo demanda.
- **`backend/app/analyzers/dependency_graph.py`:**
  - Blindaje con defensas null-safe en `_build_module_keys_map` y `build_graph`.

---

## 3. Verificacion y Pruebas Automatizadas

- **Comando Backend:**
  ```bash
  python -m pytest backend/tests/test_anti_drift.py backend/tests/test_sonar_hub.py -v
  ```
- **Resultado:**
  ```
  test_blast_radius_calculation PASSED                 [ 11%]
  test_hexagonal_layer_drift_validation PASSED         [ 22%]
  test_anti_drift_course_evaluation PASSED             [ 33%]
  test_topography_and_drift_endpoints PASSED           [ 44%]
  test_course_plot_endpoint_enriched_with_drift PASSED [ 55%]
  test_sonar_manager_connect_and_disconnect PASSED     [ 66%]
  test_sonar_blueprint_broadcast_and_history PASSED    [ 77%]
  test_sonar_collision_alert_direct PASSED             [ 88%]
  test_sonar_rest_endpoints PASSED                     [100%]
  9 passed in 7.35s
  ```

- **Verificacion de Compilacion Frontend:**
  ```bash
  npm run build --prefix frontend
  ```
  Resultado: Compilacion limpia con Vite en 8.67s sin errores tipograficos ni incompatibilidades.

- **Verificacion de Estilo:**
  0 emojis detectados en todo el codigo y documentacion modificada.

---

## 4. Coordinacion y Concurrencia con el Equipo

- **Brandon Carranza (US-06 / UI Cockpit):**
  - Dispone ahora de `drift_risk`, `blast_radius` y `reef_warnings` en el contrato JSON de `/api/v1/course/plot` para visualizar metricas de riesgo directamente en el Cockpit.
  - Puede invocar `/api/v1/architecture/{repo_id}/drift/evaluate` para validar interactivamente cambios propuestos antes de confirmar el rumbo.
- **Dylan Gamero (US-08 / Radar Sonar):**
  - El backend valida el acoplamiento cruzado de archivos mediante Tarjan SCC real en lugar de comparaciones superficiales de carpetas.
- **GitFlow:**
  - Los cambios se completaron en la rama `feature/backend-anti-code-drift` que parte de `origin/develop`.
  - Se crea Pull Request formal hacia `develop` sin realizar merge directo.

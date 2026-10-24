# ADR-0002: Arquitectura Hexagonal y Modular para Mantenibilidad Open Source

## Estado
Aceptado

## Contexto
Los proyectos de código abierto sufren cuando el acoplamiento entre la capa de presentación (UI/API), la lógica de negocio (trazado de rutas, análisis sintáctico) y la infraestructura (Ollama, SQLite, WebSockets) es estrecho. Los colaboradores externos encuentran difícil contribuir analizadores para nuevos lenguajes o cambiar motores de inferencia sin romper el núcleo.

## Criterios de Decision
* Independencia de frameworks externos y librerías de inferencia.
* Testabilidad aislada de la lógica de análisis topológico sin requerir bases de datos ni servicios externos levantados.
* Facilidad para que contribuidores de la comunidad añadan nuevos parsers de lenguajes de programación.

## Decision
Se adopta una arquitectura modular basada en el patrón de Puertos y Adaptadores (Arquitectura Hexagonal):

1. **Dominio / Analizadores de Código (Core):**
   * Motor AST universal basado en Tree-sitter (`treesitter_engine.py`).
   * Analizador topológico de dependencias y componentes fuertemente conexos con el Algoritmo de Tarjan (`dependency_graph.py`).
   * Totalmente agnóstico del protocolo HTTP, base de datos o modelo de lenguaje.
2. **Servicios de Aplicación (Application Layer):**
   * Servicio de Trazado de Rumbo (`CoursePlotterService`): Orquesta la correlación entre el requerimiento del issue y el AST.
   * Servicio de Sonar de Flota (`FleetSonarManager`): Gestiona presencia y evalúa proximidad topológica.
3. **Adaptadores de Infraestructura (Adapters):**
   * Cliente Ollama (`ChatOllamaLocal`): Adaptador de inferencia local.
   * Repositorio SQLite (`SQLAlchemy`): Persistencia de estado y metadatos de repositorios.
   * Adaptador WebSocket: Transporte en tiempo real sobre FastAPI.
4. **Capa de Presentación (Frontend):**
   * SPA desacoplada en React 18 + Vite que interactúa exclusivamente a través de contratos REST y WebSockets tipados con TypeScript.

## Consecuencias
* Positivo: Alta cohesión y bajo acoplamiento. Cualquier nuevo lenguaje soportado por Tree-sitter puede agregarse sin tocar la API ni la UI.
* Positivo: Pruebas unitarias deterministas ultra-rápidas para el core sin mocks complejos de red.
* Negativo: Mayor número de clases y capas de abstracción en comparación con un script monolítico tradicional.

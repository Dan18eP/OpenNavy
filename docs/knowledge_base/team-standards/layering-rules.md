# Estándar de Equipo: Reglas de Arquitectura por Capas (Layering Rules)

**Identificador:** `layering_rules`  
**Tipo:** `team_standard`  
**Categoría:** Arquitectura y Modularidad  
**Autoridad:** Praxia Engineering Standards Board  
**Rule-ID:** PRAXIA-TEAM-ARCH-01  
**Severidad:** high  
**Versión:** 2.0  

---

## 1. Estructura de Capas de la Aplicación
El backend de Praxia y los servicios analizados siguen un diseño estricto en capas inspirado en Ports & Adapters y Clean Architecture:

```
backend/app/
├── api/            # Capa 1 (Externa): Controladores REST, Endpoints SSE, Webhooks
├── core/           # Capa Transversal: Configuración, Motor de Base de Datos, Criptografía
├── models/         # Capa 2: Modelos de Dominio y Persistencia (SQLAlchemy Entities)
├── schemas/        # Capa 2: Contratos de Datos, DTOs y Estado de Agentes (Pydantic / TypedDict)
├── analyzers/      # Capa 3: Motor de Análisis Estático (Tree-sitter) y Métricas
├── rag/            # Capa 3: Base Vectorial, Indexación y Recuperación de Conocimiento
├── agents/         # Capa 4 (Orquestación): Nodos Atómicos y StateGraph de LangGraph
└── workers/        # Capa Asíncrona: Tareas en Segundo Plano y Canales de Eventos
```

---

## 2. Matriz de Dependencias Permitidas

| Módulo Origen | Módulos Permitidos de Importar | Prohibido Importar | Justificación |
|---|---|---|---|
| `models` | `core` (tipos base) | `api`, `agents`, `analyzers`, `workers` | El dominio es el núcleo y no debe conocer la capa web ni los analizadores. |
| `schemas` | `models` (para validación `from_attributes`), `core` | `api`, `agents`, `workers` | Los DTOs deben ser estables y desacoplados de la orquestación. |
| `analyzers` | `schemas`, `core` | `api`, `agents`, `workers` | Los parsers son motores determinísticos puros. |
| `rag` | `schemas`, `models`, `core` | `api`, `agents` | La base de conocimiento no orquesta agentes ni atiende peticiones HTTP. |
| `agents` | `schemas`, `models`, `analyzers`, `rag`, `core` | `api` | Los agentes orquestan lógica de análisis pero son agnósticos de la API REST. |
| `api` | `schemas`, `models`, `agents`, `core`, `workers` | *Sin restricciones descendentes* | Punto de entrada del sistema. |

---

## 3. Principio de Aislamiento de Ejecución y Seguridad
1. **Modo Solo Lectura:** Los analizadores estáticos y el motor Tree-sitter jamás deben invocar comandos de ejecución arbitraria sobre el código inspeccionado.
2. **Cero Fuga:** Todo fragmento de código debe ser sanitizado por `SecretMasker` antes de salir hacia cualquier nodo o LLM.

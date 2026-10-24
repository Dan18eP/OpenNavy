# Estándar de Equipo: Convenciones de Nomenclatura (Naming Conventions)

**Identificador:** `naming_conventions`  
**Tipo:** `team_standard`  
**Categoría:** Guías de Estilo y Nomenclatura  
**Autoridad:** Praxia Engineering Standards Board  
**Rule-ID:** PRAXIA-TEAM-STYLE-01  
**Severidad:** medium  
**Versión:** 2.0  

---

## 1. Convenciones por Lenguaje y Ámbito

### 1.1 Python (PEP 8 Adaptado a Praxia)
- **Módulos y Paquetes:** `snake_case` en minúsculas (ej. `order_service.py`, `auth_utils/`).
- **Clases y Modelos:** `PascalCase` (ej. `UserRepository`, `AnalysisState`, `HybridVectorStore`).
- **Funciones y Métodos:** `snake_case` descriptivo comenzando con verbo (ej. `calculate_total()`, `find_by_email()`).
- **Constantes de Configuración:** `UPPER_SNAKE_CASE` (ej. `MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE`).
- **Variables privadas/protegidas:** Prefijo simple `_leading_underscore`.

### 1.2 TypeScript / JavaScript
- **Archivos de Componentes React:** `PascalCase.tsx` (ej. `RepoSelector.tsx`, `MetricsDashboard.tsx`).
- **Archivos de utilidades y hooks:** `camelCase.ts` o `kebab-case.ts` (ej. `useAnalysisStream.ts`, `formatters.ts`).
- **Funciones y Variables:** `camelCase` (ej. `fetchRepoMetrics`, `isLoading`).
- **Tipos, Interfaces y Enums:** `PascalCase` (ej. `AnalysisResult`, `FindingItem`).

---

## 2. Reglas de Claridad Semántica y Anti-Olores
1. **Intención Explícita:** Evitar abreviaturas crípticas fuera de dominios matemáticos estándar (preferir `repository` a `repo_mgr_inst`).
2. **Colecciones en Plural:** Listas, conjuntos y diccionarios deben nombrarse en plural (`users`, `active_jobs`).
3. **Booleanos con Prefijo Afirmativo:** Las variables booleanas deben comenzar con `is_`, `has_`, `can_` o `should_` (ej. `is_active`, `has_permission`).

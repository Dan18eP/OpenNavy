# Criterio: Control de Versiones de Dependencias y Compatibilidad

**Identificador:** `dependency_version_control`  
**Tipo:** `metric_threshold`  
**Categoría:** Seguridad, Mantenibilidad y Salud del Ecosistema  
**Versión:** 1.0  

---

## 1. Definición y Propósito
El **Control de Versiones de Dependencias y Compatibilidad** evalúa el estado del grafo de dependencias externas (paquetes y librerías de terceros) declaradas en los manifiestos del proyecto (`package.json`, `requirements.txt`, `Pipfile`, `pom.xml`, `go.mod`, etc.).

Mantener dependencias actualizadas y compatibles garantiza:
- **Reducción de vulnerabilidades de seguridad** (parches contra CVEs conocidos).
- **Mitigación de deuda técnica y obsolescencia**, evitando migraciones traumáticas de múltiples versiones mayores.
- **Interoperabilidad y compatibilidad de runtime**, asegurando que los frameworks y paquetes del ecosistema coexistan sin colisiones ni fallos en producción.

---

## 2. Clasificación SemVer y Niveles de Actualización

Siguiendo el estándar de **Versionado Semántico (SemVer: `MAJOR.MINOR.PATCH`)**:

| Nivel de Cambio | Notación SemVer | Impacto y Riesgo | Acción Recomendada |
|---|---|---|---|
| **Al día (Up to date)** | `vX.Y.Z` | Ninguno. El paquete se encuentra en la versión estable vigente. | Mantener monitoreo continuo. |
| **Parche (Patch)** | `vX.Y.Z` → `vX.Y.Z+1` | **Bajo**. Correcciones de bugs y parches de seguridad retrocompatibles. | Actualización inmediata y automática recomendada. |
| **Menor (Minor)** | `vX.Y.Z` → `vX.Y+1.0` | **Medio-Bajo**. Nuevas funcionalidades retrocompatibles. | Actualizar y ejecutar suite de pruebas automatizadas. |
| **Mayor (Major)** | `vX.Y.Z` → `vX+1.0.0` | **Alto (Breaking Changes)**. Cambios que rompen compatibilidad hacia atrás o reestructuran la API. | Revisar guías de migración y changelogs antes de actualizar. |
| **Incompatible (Critical)** | Versiones en conflicto | **Crítico**. Incompatibilidad conocida entre librerías o con el runtime activo. | Resolver de inmediato para evitar fallos de ejecución. |

---

## 3. Umbrales de Calidad y Clasificación de Salud

| Score de Dependencias | Calificación | Severidad | Acción Requerida |
|---|---|---|---|
| **≥ 80** | **Ecosistema Saludable (Verde)** | `INFO` | Las dependencias están al día o solo requieren parches menores. |
| **50 – 79** | **Riesgo Moderado de Obsolescencia (Amarillo)** | `WARNING` | Existen actualizaciones menores o mayores pendientes. Programar actualización en el sprint. |
| **< 50** | **Riesgo Crítico / Incompatibilidad (Rojo)** | `CRITICAL` | Dependencias gravemente obsoletas o incompatibles. Bloquear despliegue hasta su resolución. |

---

## 4. Fórmula de Puntuación de Dependencias

$$\text{Score}_{\text{deps}} = \max\left(0, 100 - (30 \times N_{\text{incompatibles}} + 15 \times N_{\text{major}} + 5 \times N_{\text{minor}} + 2 \times N_{\text{patch}})\right)$$

Donde:
- $N_{\text{incompatibles}}$: Número de dependencias con conflicto directo o deprecadas.
- $N_{\text{major}}$: Número de dependencias con actualización mayor pendiente.
- $N_{\text{minor}}$: Número de dependencias con actualización menor pendiente.
- $N_{\text{patch}}$: Número de dependencias con parche pendiente.

---

## 5. Estrategias de Remediación y Mejores Prácticas
1. **Fijación Consciente de Versiones**: Evitar `*` o `latest` en entornos de producción. Usar operadores de compatibilidad semántica (`^` o `~` en Node/npm, `~=` o `>=,<` en Python).
2. **Uso de Lockfiles**: Mantener siempre bajo control de versiones `package-lock.json`, `Pipfile.lock`, `pnpm-lock.yaml` o `poetry.lock`.
3. **Automatización de Auditorías**: Integrar herramientas de actualización continua como Dependabot o Renovate.
4. **Verificación de Incompatibilidades en CI/CD**: Ejecutar pruebas de integración tras cada actualización de dependencia.

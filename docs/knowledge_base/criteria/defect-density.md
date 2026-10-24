# Criterio: Densidad de Defectos (Defect Density)

**Identificador:** `defect_density`  
**Tipo:** `process_metric`  
**Categoría:** Calidad de Proceso y Confiabilidad  
**Versión:** 1.0  

---

## 1. Definición y Fórmula
La **Densidad de Defectos** relaciona el número de defectos confirmados (bugs reportados en producción o QA) con el tamaño del código fuente analizado en miles de líneas de código (KLOC).

$$\text{Densidad de Defectos} = \frac{\text{Número de Bugs Reportados}}{\text{KLOC (Miles de Líneas de Código)}} \quad \text{[en ventana de 30 días]}$$

---

## 2. Fuente de Datos e Integración
- **Origen:** Conector API de GitHub Issues / Jira / GitLab Issues filtrando por etiqueta `type: bug` o `priority: high/critical` cerrados en la ventana de tiempo.
- **Requisito:** Si la integración con el issue tracker no está configurada, el sistema marca este criterio como `"no_disponible"` en el panel sin afectar negativamente el cálculo estático.

---

## 3. Umbrales de Calidad

| Defectos / KLOC / Mes | Calificación | Severidad |
|---|---|---|
| **< 1.0** | **Excelente** | `INFO` |
| **1.0 – 3.0** | **Aceptable** | `INFO` |
| **3.1 – 5.0** | **Riesgo Moderado** | `WARNING` |
| **> 5.0** | **Crítico (Inestable)** | `HIGH` / `CRITICAL` |

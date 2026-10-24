# Criterio: Tasa de Fallos en Cambios (Change Failure Rate - CFR)

**Identificador:** `change_failure_rate`  
**Tipo:** `process_metric`  
**Categoría:** Métricas DORA / Estabilidad de Entrega  
**Versión:** 1.0  

---

## 1. Definición y Fórmula DORA
La **Tasa de Fallos en Cambios (CFR)** es una de las 4 métricas clave de DevOps Research and Assessment (DORA). Mide el porcentaje de despliegues a producción o merges a rama principal que resultan en fallas que requieren hotfixes, parches de emergencia o rollbacks inmediatos.

$$\text{CFR (\%)} = \left( \frac{\text{Número de Despliegues Fallidos / Rollbacks / Hotfixes}}{\text{Total de Despliegues Realizados}} \right) \times 100$$

---

## 2. Fuente de Datos e Integración
- **Origen:** Webhooks de CI/CD (GitHub Actions, GitLab CI, ArgoCD, Jenkins) y eventos de deployment.
- **Requisito:** Si el repositorio no cuenta con pipelines integrados o historial de deployments, este valor se marca como `"no_disponible"` en el dashboard.

---

## 3. Umbrales DORA

| Rango de CFR | Nivel de Rendimiento DORA | Severidad |
|---|---|---|
| **0% – 15%** | **Elite / Alto Rendimiento** | `INFO` |
| **16% – 30%** | **Rendimiento Medio** | `WARNING` |
| **> 30%** | **Bajo Rendimiento (Inestable)** | `CRITICAL` |

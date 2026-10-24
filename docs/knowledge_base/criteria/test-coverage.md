# Criterio: Cobertura de Pruebas (Test Coverage)

**Identificador:** `test_coverage`  
**Tipo:** `metric_threshold`  
**Categoría:** Calidad de Pruebas y Confiabilidad  
**Versión:** 1.0  

---

## 1. Definición y Alcance
La **Cobertura de Pruebas** cuantifica el grado en que el código fuente es ejecutado cuando corre la suite de pruebas automatizadas (unitarias, integración y funcionales).

No garantiza por sí sola la ausencia de errores, pero una cobertura insuficiente asegura que existen caminos y estados de error no probados propensos a fallos en producción.

---

## 2. Tipos de Cobertura Analizados
1. **Line / Statement Coverage:** Porcentaje de sentencias ejecutables visitadas al menos una vez durante los tests.
2. **Branch / Decision Coverage:** Porcentaje de ramas booleanas (`true` y `false` en cada `if`, `while`, etc.) evaluadas en las pruebas.
3. **Critical Path Coverage:** Cobertura focalizada en las entidades de dominio y módulos de negocio críticos (pagos, autenticación, procesamiento de transacciones).

---

## 3. Formatos de Reporte Soportados
El sistema busca y parsea de manera autónoma los siguientes artefactos en el repositorio:
- `coverage.xml`, `cobertura.xml` (Python / Cobertura)
- `lcov.info` (JavaScript / TypeScript - Jest, Vitest, NYC)
- `jacoco.xml` (Java - JaCoCo / Maven / Gradle)
- `cover.out` (Go - `go test -coverprofile`)
- `coverage.cobertura.xml` (C# / .NET - Coverlet)

*Nota: Si no se detectan archivos de reporte en el repositorio, la métrica se declara como `"no_disponible"` sin bloquear el análisis.*

---

## 4. Umbrales de Calidad

| % Cobertura de Líneas | Nivel | Severidad | Acción |
|---|---|---|---|
| **≥ 80%** | **Excelente (Verde)** | `INFO` | Suite de pruebas sólida. |
| **60% – 79%** | **Aceptable (Amarillo)** | `WARNING` | Requiere añadir tests unitarios en módulos nuevos. |
| **< 60%** | **Deficiente (Rojo)** | `HIGH` | Riesgo elevado en refactorizaciones y despliegues. |
| **0% / No detectable** | **Sin Pruebas (Crítico)** | `CRITICAL` | Repositorio sin red de seguridad automatizada. |

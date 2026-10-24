# Criterio: Duplicación de Código y Principio DRY (Code Duplication)

**Identificador:** `code_duplication`  
**Tipo:** `metric_threshold`  
**Categoría:** Calidad Estática de Código / DRY  
**Autoridad de Referencia Canónica:** Martin Fowler (*Refactoring: Improving the Design of Existing Code*, Chapter 3: Duplicated Code)  
**Documento Canónico Vinculado:** `knowledge-base/canonical/refactoring.improving.the.design.of.existing.code.2nd.edition.2018.11.md`  
**Rule-ID:** NAVY-DRY-01  
**Severidad:** medium  
**Versión:** 2.0 (Enriquecida con Casos Few-Shot de Auditoría)  

---

## 1. Fundamento Canónico de Martin Fowler
La duplicación de código es el olor de diseño más generalizado. Duplicar una estructura lógica significa que cualquier corrección futura requiere múltiples cambios sincronizados, multiplicando los bugs por omisión.

---

## 2. Casos de Estudio Few-Shot: Duplicación Tipo 1 y 2 vs. Extracción Reutilizable

### ❌ Código con Violación (Clon Tipo 2: Lógica idéntica duplicada en dos funciones):
```python
def export_sales_report(records: list) -> list:
    cleaned = []
    for r in records:
        if r.get("is_valid") and r.get("amount", 0) > 0:
            cleaned.append({"id": r["id"], "total": round(r["amount"] * 1.19, 2)})
    return cleaned

def export_inventory_report(items: list) -> list:
    # Exactamente la misma lógica de filtrado y cálculo de IVA
    cleaned = []
    for item in items:
        if item.get("is_valid") and item.get("amount", 0) > 0:
            cleaned.append({"id": item["id"], "total": round(item["amount"] * 1.19, 2)})
    return cleaned
```

### ✅ Código Refactorizado (Extract Function & Parametrización Funcional):
```python
from typing import List, Dict, Any, Callable

def transform_taxable_records(
    records: List[Dict[str, Any]], 
    tax_rate: float = 1.19
) -> List[Dict[str, Any]]:
    """Función pura reutilizable que centraliza la regla de negocio del cálculo impositivo."""
    return [
        {"id": r["id"], "total": round(r["amount"] * tax_rate, 2)}
        for r in records
        if r.get("is_valid") and r.get("amount", 0) > 0
    ]

def export_sales_report(records: list) -> list:
    return transform_taxable_records(records)

def export_inventory_report(items: list) -> list:
    return transform_taxable_records(items)
```

---

## 3. Umbrales de Aceptabilidad en Auditoría

| Porcentaje de Duplicación en Repositorio | Calificación | Severidad | Acción Requerida |
|---|---|---|---|
| **< 3.0%** | Óptimo (Verde) | `INFO` | Cero intervención. Estructura altamente DRY. |
| **3.0% – 5.0%** | Aceptable (Amarillo claro) | `INFO` | Monitorear en PRs. |
| **5.0% – 10.0%** | Moderada (Amarillo) | `WARNING` | Aplicar *Extract Function* en utilitarios comunes. |
| **> 10.0%** | Crítica (Rojo) | `HIGH` | Bloqueo preventivo. Deuda técnica acumulativa. |

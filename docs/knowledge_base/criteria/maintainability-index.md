# Criterio: Índice de Mantenibilidad (Maintainability Index - MI)

**Identificador:** `maintainability_index`  
**Tipo:** `metric_threshold`  
**Categoría:** Calidad Estática de Código y Mantenibilidad  
**Autoridades de Referencia Canónicas:**  
- ISO/IEC 25010:2023 (*Systems and software Quality Requirements and Evaluation — Maintainability Model*)  
- Software Engineering Institute (SEI CMU / Coleman et al.)  
**Documento Canónico Vinculado:** `knowledge-base/canonical/iso_iec_25010_2023.md`  
**Rule-ID:** PRAXIA-MI-01  
**Severidad:** high  
**Versión:** 2.0 (Enriquecida con Casos Few-Shot de Auditoría)  

---

## 1. Fundamento Canónico e ISO/IEC 25010:2023
La mantenibilidad evalúa el grado de eficacia y eficiencia con el que un activo de software puede ser modificado por desarrolladores. El Índice de Mantenibilidad sintetiza tres dimensiones críticas:
1. **Volumen de Halstead ($V$):** Carga simbólica de operandos y operadores.
2. **Complejidad Ciclomática de McCabe ($G$):** Estructura del grafo de decisión.
3. **Líneas de Código Ejecutables ($\text{LOC}$):** Densidad del cuerpo de la función o módulo.

---

## 2. Casos de Estudio Few-Shot: Baja Mantenibilidad vs. Descomposición Modular

### ❌ Código con Violación ($MI < 40$, Alta Carga Cognitiva):
```python
def generate_client_invoice(client_id, year, month, db, tax_service, pdf_writer):
    # Función de 80 líneas que consulta datos, aplica 7 fórmulas complejas anidadas,
    # manipula buffers binarios de PDF y gestiona transacciones en un solo bloque.
    pass
```

### ✅ Código Refactorizado ($MI > 75$, Composición Desacoplada):
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class BillingPeriod:
    year: int
    month: int

class InvoiceAssembler:
    """Orquestador de alto nivel con baja complejidad y alta analizabilidad."""
    def __init__(self, data_loader, tax_calculator, document_renderer):
        self._data_loader = data_loader
        self._tax_calculator = tax_calculator
        self._document_renderer = document_renderer

    def build_invoice(self, client_id: str, period: BillingPeriod) -> bytes:
        raw_items = self._data_loader.fetch_period_items(client_id, period)
        taxed_items = self._tax_calculator.apply_taxes(raw_items)
        return self._document_renderer.render_pdf(client_id, period, taxed_items)
```

---

## 3. Umbrales de Calificación

| Rango de MI (0 a 100) | Calificación de Calidad | Severidad | Acción Requerida en Praxia |
|---|---|---|---|
| **$\ge 65.0$** | **Alta Mantenibilidad (Verde)** | `INFO` | Aprobado. Código modular y limpio. |
| **$50.0 – 64.9$** | **Mantenibilidad Moderada (Amarillo)** | `WARNING` | Revisar en code review. Evaluar simplificación de expresiones. |
| **$< 50.0$** | **Mantenibilidad Crítica (Rojo)** | `HIGH` | Bloqueo preventivo. Descomposición modular obligatoria. |

# Criterio: Estándares de Código Limpio y Refactorización (Clean Code)

**Identificador:** `clean_code`  
**Tipo:** `qualitative_rubric`  
**Categoría:** Legibilidad, Higiene y Refactorización  
**Autoridad de Referencia Canónica:** Martin Fowler (*Refactoring: Improving the Design of Existing Code*, 2nd Ed. 2018)  
**Documento Canónico Vinculado:** `knowledge-base/canonical/refactoring.improving.the.design.of.existing.code.2nd.edition.2018.11.md`  
**Rule-ID:** PRAXIA-CLEAN-01  
**Severidad:** medium  
**Versión:** 2.0 (Enriquecida con Casos Few-Shot de Auditoría)  

---

## 1. Fundamentos Canónicos
Según Martin Fowler y Kent Beck, un *Code Smell* no es un error de compilación o ejecución, sino una señal estructural que ralentiza el desarrollo y multiplica el riesgo de defectos. Esta guía operativa conecta directamente con el catálogo canónico de refactorizaciones de Fowler.

---

## 2. Casos de Estudio Few-Shot: Olores de Código vs. Refactorizaciones

### 2.1 Arrow Anti-Pattern (Anidamiento Condicional Profundo)
> *Smell: Bloques `if-else` y `for` anidados a más de 3 niveles que saturan la memoria de trabajo cognitiva.*

#### ❌ Código con Violación (Nesting Depth = 4):
```python
def process_refund(user, transaction):
    if user is not None:
        if user.is_active:
            if transaction.status == "settled":
                if transaction.amount <= user.refund_allowance:
                    transaction.execute_refund()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    return False
```

#### ✅ Código Refactorizado (Replace Nested Conditional with Guard Clauses):
```python
def process_refund(user, transaction) -> bool:
    """Cláusulas de guarda tempranas que eliminan la anidación y aplanan el flujo."""
    if not user or not user.is_active:
        return False
    if transaction.status != "settled":
        return False
    if transaction.amount > user.refund_allowance:
        return False

    transaction.execute_refund()
    return True
```

---

### 2.2 Long Parameter List (Firmas con Excesivos Parámetros)
> *Smell: Métodos que reciben más de 3 o 4 parámetros primitivos posicionales sueltos.*

#### ❌ Código con Violación (5 argumentos primitivos):
```python
def create_invoice(client_id: str, amount: float, tax_rate: float, currency: str, due_date: str):
    # Fácil intercambiar el orden accidentalmente entre parámetros del mismo tipo
    pass
```

#### ✅ Código Refactorizado (Introduce Parameter Object / DTO):
```python
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class InvoiceDraft:
    client_id: str
    amount: float
    tax_rate: float
    currency: str
    due_date: date

def create_invoice(draft: InvoiceDraft):
    # Firma limpia, inmutable y autovalidable
    pass
```

---

### 2.3 Excepciones Silenciadas (Catch and Ignore)
> *Smell: Capturar `Exception` de forma genérica y continuar con `pass`.*

#### ❌ Código con Violación:
```python
try:
    load_security_keys()
except Exception:
    pass  # Silencia fallos catastróficos de autenticación o filesystem
```

#### ✅ Código Refactorizado:
```python
import logging

logger = logging.getLogger(__name__)

try:
    load_security_keys()
except FileNotFoundError as err:
    logger.warning("Claves opcionales no encontradas, usando almacén por defecto: %s", err)
except PermissionError as err:
    logger.critical("Error de permisos crítico al leer credenciales del sistema: %s", err)
    raise
```

---

## 3. Umbrales de Calidad

| Indicador | Límite Aceptable | Límite Crítico | Técnica de Refactorización Fowler |
|---|---|---|---|
| **Líneas por Función (SLOC)** | $\le 30$ | $> 50$ | *Extract Function* |
| **Parámetros por Función** | $\le 3$ | $> 4$ | *Introduce Parameter Object* |
| **Profundidad de Anidamiento** | $\le 2$ | $> 3$ | *Replace Nested Conditional with Guard Clauses* |
| **Excepciones Silenciadas** | $0$ | $> 0$ | *Structured Logging / Specific Exception Raising* |

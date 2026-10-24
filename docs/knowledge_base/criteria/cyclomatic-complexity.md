# Criterio: Complejidad Ciclomática y Estructuración de Control (McCabe)

**Identificador:** `cyclomatic_complexity`  
**Tipo:** `metric_threshold`  
**Categoría:** Calidad Estática de Código / Estructura  
**Autoridad de Referencia Canónica:** Thomas J. McCabe (IEEE TSE 1976) / NIST Special Publication 500-235 (SEI)  
**Documento Canónico Vinculado:** `knowledge-base/canonical/nistspecialpublication500_235.md`  
**Rule-ID:** PRAXIA-MCCABE-01  
**Severidad:** high  
**Versión:** 2.0 (Enriquecida con Casos Few-Shot de Auditoría)  

---

## 1. Definición Matemática Canónica (NIST SP 500-235)
La **Complejidad Ciclomática ($V(G)$)** representa el número de caminos linealmente independientes a través de un grafo de flujo de control dirigido $G = (E, N, P)$:

$$V(G) = E - N + 2P$$

Donde $E$ es el número de aristas, $N$ el número de nodos básicos y $P$ el número de componentes conexos.

En términos sintácticos de AST, cada punto de decisión (`if`, `elif`, bucles `while`/`for`, operadores booleanos `and`/`or`, bloques `except`) suma $+1$ a la complejidad base.

---

## 2. Casos de Estudio Few-Shot: Complejidad Ciclomática vs. Despacho Polimórfico

### ❌ Código con Violación Crítica ($CC = 11$, Exceso de Bifurcaciones):
```python
def process_event_payload(event_type: str, payload: dict) -> dict:
    if event_type == "user_created":
        return {"action": "sync_crm", "user": payload["id"]}
    elif event_type == "user_deleted":
        return {"action": "purge_cache", "user": payload["id"]}
    elif event_type == "order_placed":
        if payload.get("is_urgent"):
            return {"action": "priority_dispatch", "order": payload["id"]}
        else:
            return {"action": "standard_dispatch", "order": payload["id"]}
    elif event_type == "payment_received":
        return {"action": "generate_receipt", "amount": payload["amount"]}
    else:
        raise ValueError(f"Evento no soportado: {event_type}")
```

### ✅ Código Refactorizado: Despacho por Diccionario / Handlers ($CC = 2$ por función):
```python
from typing import Callable, Dict

def _handle_order_placed(payload: dict) -> dict:
    action = "priority_dispatch" if payload.get("is_urgent") else "standard_dispatch"
    return {"action": action, "order": payload["id"]}

EVENT_HANDLERS: Dict[str, Callable[[dict], dict]] = {
    "user_created": lambda p: {"action": "sync_crm", "user": p["id"]},
    "user_deleted": lambda p: {"action": "purge_cache", "user": p["id"]},
    "order_placed": _handle_order_placed,
    "payment_received": lambda p: {"action": "generate_receipt", "amount": p["amount"]},
}

def process_event_payload(event_type: str, payload: dict) -> dict:
    handler = EVENT_HANDLERS.get(event_type)
    if not handler:
        raise ValueError(f"Evento no soportado: {event_type}")
    return handler(payload)
```

---

## 3. Umbrales Formales del NIST / SEI

| Rango de Complejidad ($CC$) | Nivel de Riesgo | Cobertura Mínima de Casos de Prueba | Acción en Auditoría Praxia |
|---|---|---|---|
| **1 – 10** | **Bajo Riesgo (Verde)** | 1 a 10 casos de prueba | Aprobado sin observaciones. |
| **11 – 20** | **Riesgo Moderado (Amarillo)** | 11 a 20 casos de prueba | Advertencia. Refactorizar si la función posee cambios frecuentes. |
| **21 – 50** | **Alto Riesgo (Naranja)** | 21 a 50 casos de prueba | Violación. Requiere descomposición funcional antes de producción. |
| **> 50** | **Incontrolable (Rojo)** | Imposible de testear exhaustivamente | Bloqueo estricto de Pull Request. Violación crítica. |

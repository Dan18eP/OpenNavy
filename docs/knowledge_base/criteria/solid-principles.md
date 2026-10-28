# Criterio: Principios SOLID de Diseño Orientado a Objetos

**Identificador:** `solid_principles`  
**Tipo:** `qualitative_rubric`  
**Categoría:** Arquitectura y Diseño de Software  
**Autoridad de Referencia Canónica:** Robert C. Martin (Uncle Bob - *Clean Architecture*, Prentice Hall 2017)  
**Documento Canónico Vinculado:** `knowledge-base/canonical/book___clean_architecture___robert_cecil_martin.md`  
**Rule-ID:** NAVY-SOLID-01  
**Severidad:** high  
**Versión:** 2.0 (Enriquecida con Casos Few-Shot de Auditoría)  

---

## 1. Visión General y Fundamento Canónico
Los principios **SOLID**, formulados por Robert C. Martin, constituyen el pilar fundamental para el diseño de código orientado a objetos y modular. En OpenNavy, este criterio opera como **guía de remediación operativa de 2º nivel**, complementando la teoría formal del libro canónico *Clean Architecture* alojado en `knowledge-base/canonical/`.

El motor evaluador identifica violaciones estructurales en clases y funciones, utilizando los siguientes casos de entrenamiento (*few-shots*) para guiar la refactorización.

---

## 2. Casos de Estudio y Few-Shots de Refactorización

### 2.1 Single Responsibility Principle (SRP) — Responsabilidad Única
> *"Un módulo debe tener una, y solo una, razón para cambiar (un único actor o stakeholder al que responde)."*

#### ❌ Código con Violación (Bad Smell / God Function):
```python
# Violación SRP: La función orquesta validación, consulta SQL, cálculo y despacho de email
class OrderProcessor:
    def process(self, order_data: dict, db_conn, email_client):
        # 1. Validación de entrada
        if not order_data.get("items") or order_data.get("total", 0) <= 0:
            raise ValueError("Orden inválida")
        
        # 2. Persistencia directa en base de datos
        cursor = db_conn.cursor()
        cursor.execute("INSERT INTO orders (id, total) VALUES (?, ?)", 
                       (order_data["id"], order_data["total"]))
        db_conn.commit()
        
        # 3. Notificación externa
        msg = f"Tu orden {order_data['id']} ha sido procesada."
        email_client.send(order_data["customer_email"], "Confirmación", msg)
```

#### ✅ Código Refactorizado (Correct Clean Design):
```python
# Refactorización SRP: Separación en componentes cohesivos y caso de uso
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class Order:
    id: str
    total: float
    customer_email: str

class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...

class NotificationSender(Protocol):
    def notify(self, email: str, message: str) -> None: ...

class ProcessOrderUseCase:
    """Caso de uso con una única razón para cambiar: la regla de negocio de procesamiento."""
    def __init__(self, repo: OrderRepository, notifier: NotificationSender):
        self._repo = repo
        self._notifier = notifier

    def execute(self, order: Order) -> None:
        if order.total <= 0:
            raise ValueError("El total de la orden debe ser positivo.")
        self._repo.save(order)
        self._notifier.notify(order.customer_email, f"Orden {order.id} confirmada.")
```

---

### 2.2 Dependency Inversion Principle (DIP) — Inversión de Dependencias
> *"Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones."*

#### ❌ Código con Violación:
```python
# El servicio de dominio instancia directamente un cliente SQLite concreto
import sqlite3

class BillingService:
    def __init__(self):
        # Acoplamiento directo a un detalle de infraestructura tecnológica
        self.connection = sqlite3.connect("production.db")

    def charge(self, user_id: str, amount: float):
        self.connection.execute("UPDATE balances SET balance = balance - ? WHERE user_id = ?", (amount, user_id))
```

#### ✅ Código Refactorizado:
```python
# Inversión de dependencias mediante abstracción e inyección en constructor
from typing import Protocol

class BalanceLedger(Protocol):
    def deduct(self, user_id: str, amount: float) -> None: ...

class BillingService:
    """Módulo de alto nivel desacoplado de la tecnología de base de datos."""
    def __init__(self, ledger: BalanceLedger):
        self._ledger = ledger

    def charge(self, user_id: str, amount: float):
        if amount <= 0:
            raise ValueError("El monto a cobrar debe ser mayor a cero.")
        self._ledger.deduct(user_id, amount)
```

---

### 2.3 Open/Closed Principle (OCP) — Abierto para Extensión, Cerrado para Modificación

#### ❌ Código con Violación:
```python
# Cadenas if-elif acopladas a tipos que obligan a modificar el código ante nuevos casos
def calculate_discount(customer_type: str, price: float) -> float:
    if customer_type == "regular":
        return price * 0.05
    elif customer_type == "vip":
        return price * 0.15
    elif customer_type == "corporate":
        return price * 0.25
    raise ValueError(f"Tipo desconocido: {customer_type}")
```

#### ✅ Código Refactorizado:
```python
# Patrón Strategy / Polimorfismo: Nuevos tipos se añaden agregando clases sin tocar el despachador
from typing import Protocol

class DiscountPolicy(Protocol):
    def apply(self, price: float) -> float: ...

class RegularDiscount:
    def apply(self, price: float) -> float: return price * 0.05

class VIPDiscount:
    def apply(self, price: float) -> float: return price * 0.15

class CorporateDiscount:
    def apply(self, price: float) -> float: return price * 0.25

def calculate_discount(policy: DiscountPolicy, price: float) -> float:
    return policy.apply(price)
```

---

## 3. Matriz de Severidad para Violaciones SOLID

| Principio | Severidad | Impacto en la Salud del Código | Remediación Obligatoria |
|---|---|---|---|
| **SRP** | `HIGH` | Código espagueti, concurrencia de merge conflicts, testing frágil. | Extraer métodos a clases de servicio especializadas (*Extract Class*). |
| **DIP** | `HIGH` | Imposibilidad de pruebas unitarias aisladas, acoplamiento tecnológico duro. | Inyectar protocolos o interfaces en constructor (*Dependency Injection*). |
| **OCP** | `MEDIUM` | Fragilidad en release: cada nueva feature altera lógica existente probada. | Polimorfismo, despachadores de diccionario o patrón *Strategy*. |
| **LSP** | `CRITICAL` | Excepciones no controladas en tiempo de ejecución, polimorfismo roto. | Asegurar compatibilidad de tipos y no lanzar `NotImplementedError` en subclases. |
| **ISP** | `MEDIUM` | Dependencias fantasma y métodos vacíos (`pass`). | Descomponer interfaces en protocolos específicos (*Interface Segregation*). |

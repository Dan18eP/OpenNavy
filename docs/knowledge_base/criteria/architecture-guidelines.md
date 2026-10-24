# Criterio: Regla de Dependencia y Arquitectura en Capas (Architecture Guidelines)

**Identificador:** `architecture_guidelines`  
**Tipo:** `structural_rubric`  
**Categoría:** Arquitectura de Software, Modularidad e ISO 5055  
**Autoridad de Referencia Canónica:** ISO/IEC 5055:2021 & Robert C. Martin (*Clean Architecture*)  
**Documentos Canónicos Vinculados:**  
- `knowledge-base/canonical/iso_iec_5055_2021.md`  
- `knowledge-base/canonical/book___clean_architecture___robert_cecil_martin.md`  
**Rule-ID:** PRAXIA-ARCH-01  
**Severidad:** critical  
**Versión:** 2.0 (Enriquecida con Casos Few-Shot de Auditoría)  

---

## 1. Fundamento Canónico e ISO/IEC 5055:2021
La norma **ISO/IEC 5055:2021** define reglas automatizadas para la detección de defectos arquitectónicos graves en código fuente, destacando:
1. **ASCRM-RLB-04:** Violación de fronteras de capas de software (ej. el núcleo de negocio dependiendo de bibliotecas de red o frameworks de interfaz).
2. **ASCRM-RLB-06:** Dependencias cíclicas directas e indirectas entre componentes de software.

---

## 2. Casos de Estudio Few-Shot: Violación de Fronteras de Capa vs. Clean Architecture

### ❌ Código con Violación (Capa de Dominio importando Infraestructura y Frameworks Web):
```python
# Archivo: app/domain/user.py
# Violación Crítica: El dominio depende directamente de FastAPI y SQLAlchemy
from fastapi import HTTPException
from app.infrastructure.database import SessionLocal, UserModel

class UserDomainService:
    def verify_account(self, user_id: str):
        db = SessionLocal()
        record = db.query(UserModel).filter_by(id=user_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Usuario no existe")  # Detalle HTTP en el dominio
        record.is_verified = True
        db.commit()
```

### ✅ Código Refactorizado (The Dependency Rule con Interfaces en Dominio):
```python
# Archivo: app/domain/user.py
# El dominio solo depende de tipos de Python puro y contratos abstractos
from dataclasses import dataclass
from typing import Protocol, Optional

class UserNotFoundError(Exception):
    """Excepción de dominio pura, agnóstica de protocolos HTTP."""
    pass

@dataclass
class UserEntity:
    id: str
    is_verified: bool

class UserRepositoryPort(Protocol):
    def get_by_id(self, user_id: str) -> Optional[UserEntity]: ...
    def save(self, user: UserEntity) -> None: ...

class UserVerificationUseCase:
    def __init__(self, repo: UserRepositoryPort):
        self._repo = repo

    def execute(self, user_id: str) -> None:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"Usuario {user_id} no encontrado en el sistema.")
        user.is_verified = True
        self._repo.save(user)
```

---

## 3. Resolución de Ciclos de Dependencia ($A \rightarrow B \rightarrow A$)

Cuando dos módulos se importan mutuamente, el grafo deja de ser un Directed Acyclic Graph (DAG), rompiendo la modularidad y el empaquetado independiente.

### Solución Canónica: Inversión de Dependencias o Extracción a Módulo Común
1. Si $A$ importa $B$ solo para usar un tipo de datos, mover ese tipo a un módulo neutro `types.py` o `models.py`.
2. Si $A$ invoca una operación de $B$, $A$ debe definir una interfaz (Protocol) que $B$ implementa, inyectándola en tiempo de inicio (*Composition Root*).

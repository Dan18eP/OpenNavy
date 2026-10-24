# Rúbrica Normativa: Arquitectura Limpia y Principios SOLID (Robert C. Martin)

**Autoridad:** Robert C. Martin (Uncle Bob - Clean Architecture, Prentice Hall 2017)  
**Rule-ID:** RCM-SOLID-CLEAN-01  
**Categoría:** architecture  
**Severidad:** critical  
**Identificador:** `clean_architecture_solid`

---

## 1. The Dependency Rule (La Regla de Dependencia)
La regla suprema de Clean Architecture establece que las dependencias en el código fuente sólo pueden apuntar hacia adentro, en dirección hacia las políticas de más alto nivel (el Dominio):
- **Entities / Domain:** Reglas de negocio de la empresa. No deben conocer ninguna base de datos, framework, UI ni protocolo de comunicación.
- **Use Cases / Application:** Orquestación de reglas de negocio específicas de la aplicación.
- **Interface Adapters:** Controladores, gateways, presentadores y repositorios concretos.
- **Frameworks & Drivers:** Bases de datos, frameworks web, herramientas externas.

Cualquier importación o referencia desde el núcleo de dominio hacia una capa exterior constituye una violación arquitectónica crítica.

---

## 2. Principios SOLID Fundamentales
1. **Single Responsibility Principle (SRP):** Un módulo o clase debe tener una sola razón para cambiar, satisfaciendo las necesidades de un único actor.
2. **Open/Closed Principle (OCP):** Los artefactos de software deben estar abiertos para la extensión pero cerrados para la modificación.
3. **Liskov Substitution Principle (LSP):** Los subtipos deben ser sustituibles por sus tipos base sin alterar la corrección del programa.
4. **Interface Segregation Principle (ISP):** Los clientes no deben verse obligados a depender de interfaces o métodos que no utilizan.
5. **Dependency Inversion Principle (DIP):** Los módulos de alto nivel no deben depender de los módulos de bajo nivel; ambos deben depender de abstracciones. Las abstracciones no deben depender de los detalles; los detalles deben depender de las abstracciones.

---

## 3. Principios de Paquetes y Acoplamiento
- **Acyclic Dependencies Principle (ADP):** El grafo de dependencias de la estructura de paquetes debe ser un grafo dirigido acíclico (DAG).
- **Stable Dependencies Principle (SDP):** Depende en la dirección de la estabilidad ($I \to 0$, donde la inestabilidad $I = Ce / (Ca + Ce)$).

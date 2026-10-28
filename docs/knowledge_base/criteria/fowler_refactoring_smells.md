# Rúbrica Normativa: Refactorización y Olores de Código (Martin Fowler)

**Autoridad:** Martin Fowler & Kent Beck (Refactoring: Improving the Design of Existing Code, Addison-Wesley 2018)  
**Rule-ID:** FOWLER-REFACTOR-SMELLS-01  
**Categoría:** code_smells  
**Severidad:** high  
**Identificador:** `fowler_refactoring_smells`

---

## 1. Definición de Olor de Código (Code Smell)
Un *Code Smell* es una estructura superficial en el código que usualmente indica un problema más profundo en el diseño o la arquitectura del sistema. No es un bug funcional inmediato, pero ralentiza drásticamente el desarrollo y multiplica el riesgo de defectos futuros.

---

## 2. Catálogo Canónico de Olores de Código
1. **Long Method (Método Largo):** Cuanto más largo sea un método, más difícil será de entender, mantener y testear. Umbral: más de 30-50 líneas efectivas.
2. **Large Class (Clase Demasiado Grande):** Una clase que intenta hacer demasiado suele tener exceso de variables de instancia y métodos no cohesivos.
3. **Primitive Obsession (Obsesión por Primitivos):** Uso reacio de pequeños objetos de valor (Value Objects) para conceptos simples como monedas, rangos, coordenadas o identificadores.
4. **Data Clumps (Grupos de Datos):** Conjuntos de datos que viajan siempre juntos a través de múltiples firmas de métodos deben encapsularse en una clase o estructura.
5. **Divergent Change (Cambio Divergente):** Ocurre cuando una misma clase se modifica comúnmente de diferentes maneras para responder a diferentes tipos de requisitos externos.
6. **Shotgun Surgery (Cirugía de Escopeta):** Cuando cada vez que se realiza un cambio funcional, es necesario modificar pequeños fragmentos dispersos en muchas clases distintas.

---

## 3. Patrones de Refactorización Sistemáticos
- **Extract Function / Extract Method:** La técnica reina para separar intenciones de implementación.
- **Introduce Parameter Object:** Reemplazar largas listas de parámetros por un objeto cohesivo.
- **Replace Conditional with Polymorphism:** Simplificar el control de flujo y distribuir responsabilidades dinámicas.

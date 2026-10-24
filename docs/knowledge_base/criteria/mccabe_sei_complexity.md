# Rúbrica Normativa: Complejidad Ciclomática y Modularidad (McCabe / SEI)

**Autoridad:** Thomas J. McCabe (A Complexity Measure, IEEE TSE 1976) / Software Engineering Institute (SEI CMU)  
**Rule-ID:** SEI-MCCABE-COMPLEXITY-01  
**Categoría:** complexity  
**Severidad:** critical  
**Identificador:** `mccabe_sei_complexity`

---

## 1. Fundamento Matemático y Definición
La Complejidad Ciclomática $v(G)$ mide cuantitativamente el número de caminos linealmente independientes a través del grafo de flujo de control de un módulo:
$$v(G) = E - N + 2P$$
donde:
- $E$: Número de aristas del grafo de flujo de control.
- $N$: Número de nodos del grafo.
- $P$: Número de componentes conectados (típicamente $P = 1$ para una función individual).

De forma equivalente en AST, la complejidad base inicia en 1 y se incrementa en 1 por cada punto de decisión booleana o estructura de bifurcación (`if`, `for`, `while`, `case`, `catch`, `&&`, `||`).

---

## 2. Umbrales de Evaluación de Riesgo (McCabe / SEI)
- **$1 \le v(G) \le 10$:** Procedimiento simple, bajo riesgo, alta comprensibilidad y fácil de testear completamente.
- **$11 \le v(G) \le 20$:** Complejidad moderada, riesgo moderado, requiere pruebas de cobertura exhaustivas de caminos independientes.
- **$21 \le v(G) \le 50$:** Procedimiento complejo, alto riesgo, propenso a defectos y difícil de mantener o modificar.
- **$v(G) > 50$:** Método no testeable ni mantenible, riesgo crítico de estabilidad. Requiere refactorización y división obligatoria.

---

## 3. Estrategias de Mitigación y Descomposición
1. **Extract Method / Function:** Dividir bloques anidados y bucles en subfunciones con responsabilidad única.
2. **Reemplazo de Condicionales por Polimorfismo:** Transformar largas sentencias `switch` o cadenas `if-elif` en patrones Strategy o State.
3. **Guard Clauses:** Utilizar cláusulas de guarda con retorno temprano para aplanar la profundidad de anidamiento sintáctico.

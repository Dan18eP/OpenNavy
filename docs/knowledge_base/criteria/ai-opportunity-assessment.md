# Rúbrica Normativa: Evaluación de Oportunidad de Inteligencia Artificial (Sesión 01)

**Autoridad:** Praxia Engineering Framework / Metodología de Evaluación de Oportunidad de IA (Sesión 01)  
**Rule-ID:** NAVY-AI-OPPORTUNITY-01  
**Categoría:** ai_opportunity  
**Severidad:** high  
**Identificador:** `ai_opportunity_assessment`

---

## 1. Fundamento de la Evaluación de Oportunidad de IA
La incorporación de Inteligencia Artificial en una solución técnica debe justificarse rigurosamente en función del valor de negocio, la viabilidad técnica y los datos, el apetito de riesgo y la existencia de alternativas determinísticas viables. 

Utilizar modelos generativos o LLMs para resolver problemas abordables mediante algoritmos clásicos introduce latencia innecesaria, costes recurrentes elevados, riesgos de alucinación y pérdida de reproducibilidad.

---

## 2. Los 4 Cuadrantes de Clasificación (Matriz Sesión 01)
Cada componente funcional o caso de uso analizado se ubica en uno de cuatro cuadrantes normativos:

1. **AUTOMATIZABLE (Automatización Determinística):**
   - *Criterio:* Tareas estructuradas con reglas fijas, operaciones matemáticas, parsing de gramáticas, validación de formatos o workflows estáticos.
   - *Directriz:* Resolver mediante código clásico, expresiones regulares, parsers sintácticos o scripts deterministas. Prohibido usar LLM.
2. **ASISTIDO POR IA (Copilot / Asistencia Supervisada):**
   - *Criterio:* Tareas cognitivas complejas con contexto rico, síntesis de información ambigua, generación de explicaciones cualitativas o interpretación de lenguaje natural con supervisión humana (Human-in-the-Loop).
   - *Directriz:* Implementar agentes o llamadas a LLM con RAG y validación de salida.
3. **NO RECOMENDADO (Riesgo Alto o Inviable):**
   - *Criterio:* Problemas con tolerancia cero a errores (ej. cálculos financieros exactos, firmas criptográficas), falta total de datos de contexto o riesgo crítico de alucinación no mitigable.
   - *Directriz:* Descartar el uso de IA. Emplear verificaciones deterministas o procesos manuales certificados.
4. **POR VALIDAR (Información Incompleta):**
   - *Criterio:* Casos donde los requisitos funcionales, disponibilidad de datos o especificaciones técnicas son insuficientes para discernir la pertinencia.
   - *Directriz:* Solicitar clarificación de requerimientos de negocio y perfiles de datos antes de comprometer arquitectura de IA.

---

## 3. Algoritmo de Decisión en 6 Pasos
1. **¿Existe ambigüedad en el input o necesidad de lenguaje natural?** Si no, clasificar como `AUTOMATIZABLE`.
2. **¿Existe una solución determinista en $O(1)$ o $O(N)$?** Si sí, clasificar como `AUTOMATIZABLE`.
3. **¿La tolerancia al fallo es nula (misión crítica)?** Si sí y no hay supervisor humano, clasificar como `NO RECOMENDADO`.
4. **¿Se cuenta con corpus de conocimiento o datos para contextualizar (RAG)?** Si no y el dominio es específico, clasificar como `NO RECOMENDADO` o `POR VALIDAR`.
5. **¿La interacción humana supervisa o consume el resultado?** Si sí, clasificar como `ASISTIDO POR IA`.
6. **Si faltan especificaciones funcionales:** Clasificar como `POR VALIDAR`.

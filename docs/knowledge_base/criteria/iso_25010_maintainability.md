# Rúbrica Normativa: Mantenibilidad del Producto Software (ISO/IEC 25010)

**Autoridad:** ISO/IEC 25010:2011 (Systems and software engineering — Systems and software Quality Requirements and Evaluation)  
**Rule-ID:** ISO-25010-MAINT-01  
**Categoría:** maintainability  
**Severidad:** high  
**Identificador:** `iso_25010_maintainability`

---

## 1. Definición y Alcance
La norma ISO/IEC 25010 define la mantenibilidad como el grado de efectividad y eficiencia con el que un producto o sistema puede ser modificado por los desarrolladores designados. Comprende cinco subcaracterísticas críticas:
1. **Modularidad:** Grado en el que un sistema se compone de componentes discretos tales que un cambio en uno tiene un impacto mínimo en los demás.
2. **Reusabilidad:** Grado en que un activo puede usarse en más de un sistema o en la construcción de otros activos.
3. **Analizabilidad:** Facilidad para diagnosticar deficiencias o causas de fallas, o para identificar las partes que deben modificarse.
4. **Modificabilidad:** Grado en que un producto puede ser modificado eficazmente sin introducir defectos ni degradar la calidad existente.
5. **Comprobabilidad (Testability):** Facilidad con la que se pueden establecer criterios de prueba para un sistema o componente y realizar pruebas para determinar si se cumplen dichos criterios.

---

## 2. Umbrales y Métricas Cuantitativas
- **Índice de Mantenibilidad (Maintainability Index - MI):**
  - `MI >= 85`: Código altamente mantenible y limpio (Óptimo / Verde).
  - `65 <= MI < 85`: Mantenibilidad moderada, requiere atención en funciones críticas (Amarillo).
  - `MI < 65`: Código difícil de mantener, alto riesgo técnico y deuda arquitectónica acumulada (Crítico / Rojo).
- **Líneas de Código por Módulo (SLOC):**
  - Módulos con más de 500 SLOC sin descomposición modular violan la directriz de modularidad ISO/IEC 25010.

---

## 3. Directrices de Remediación y Buenas Prácticas
1. **Desacoplamiento Modular:** Separar responsabilidades en componentes independientes comunicados mediante contratos e interfaces estables.
2. **Encapsulamiento Riguroso:** Ocultar detalles de implementación internos y exponer únicamente APIs o firmas públicas coherentes.
3. **Refactorización Continua:** Monitorear el declive del MI en cada Pull Request para impedir la degradación acumulativa de la base de código.

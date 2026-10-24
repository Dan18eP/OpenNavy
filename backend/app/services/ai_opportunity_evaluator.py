"""
Evaluador de Oportunidad de Inteligencia Artificial (Sesión 01 - HU-RAG-02).

Audita módulos y componentes del repositorio clasificándolos en 4 cuadrantes:
- AUTOMATIZABLE (Reglas determinísticas / algoritmos clásicos)
- ASISTIDO POR IA (Copilot / supervisión humana)
- NO RECOMENDADO (Riesgo alto de alucinación / datos insuficientes)
- POR VALIDAR (Especificación incompleta)
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
from pydantic import BaseModel, Field


class OpportunityItem(BaseModel):
    module: str
    cuadrante: str  # AUTOMATIZABLE, ASISTIDO POR IA, NO RECOMENDADO, POR VALIDAR
    viabilidad_datos: str  # alta, media, baja, desconocida
    apetito_riesgo: str  # bajo, medio, alto
    valor_negocio: str  # alto, medio, bajo
    justificacion: str
    recomendacion_arquitectura: str


class AIOpportunityAssessmentResult(BaseModel):
    total_evaluados: int
    resumen_cuadrantes: Dict[str, int]
    matriz: List[OpportunityItem]
    ahorro_potencial_computo: str
    recomendacion_estrategica: str


# Patrones y palabras clave deterministas
DETERMINISTIC_PATTERNS = {
    "auth": ("Autenticación y tokens criptográficos deben resolverse con librerías estándar HMAC/JWT.", "AUTOMATIZABLE"),
    "security": ("Cálculo de firmas y enmascaramiento de secretos es 100% determinístico.", "AUTOMATIZABLE"),
    "parser": ("El parsing de código debe realizarse con Tree-sitter o gramáticas formales.", "AUTOMATIZABLE"),
    "ast": ("El análisis sintáctico y conteo de nodos AST es una operación matemática determinística.", "AUTOMATIZABLE"),
    "crypto": ("Operaciones criptográficas tienen tolerancia cero a fallos. Prohibido usar IA generativa.", "NO RECOMENDADO"),
    "finance": ("Cálculos contables y balance financiero requieren exactitud numérica determinística.", "NO RECOMENDADO"),
    "billing": ("Facturación e impuestos deben ejecutarse mediante motores de reglas deterministas.", "AUTOMATIZABLE"),
    "crud": ("Operaciones de base de datos CRUD no requieren IA.", "AUTOMATIZABLE"),
    "database": ("Consultas y persistencia relacional deben ser deterministas.", "AUTOMATIZABLE"),
}

AI_ASSISTED_PATTERNS = {
    "chat": ("Asistente conversacional con recuperación RAG y supervisor humano.", "ASISTIDO POR IA"),
    "evaluator": ("Evaluación cualitativa de diseño y explicaciones de arquitectura con RAG.", "ASISTIDO POR IA"),
    "agent": ("Orquestación de decisiones semánticas de arquitectura.", "ASISTIDO POR IA"),
    "summary": ("Síntesis de documentación técnica y generación de borradores de ADR.", "ASISTIDO POR IA"),
    "recommend": ("Motor de sugerencias y recomendaciones adaptativas.", "ASISTIDO POR IA"),
    "nlp": ("Procesamiento de texto libre y comprensión de requerimientos.", "ASISTIDO POR IA"),
}


class AIOpportunityEvaluator:
    """Motor de evaluación de oportunidad de IA según la rúbrica formal de la Sesión 01."""

    def evaluate_component(
        self,
        component_name: str,
        description: str = "",
        code_sample: str = "",
    ) -> OpportunityItem:
        """Clasifica un componente específico en los 4 cuadrantes."""
        comp_lower = component_name.lower()
        desc_lower = description.lower()
        code_lower = code_sample.lower()
        combined = f"{comp_lower} {desc_lower} {code_lower}"

        # 1. Chequeo de riesgo crítico no recomendado
        if any(k in combined for k in ["crypto", "encryption", "hash", "password", "secret", "private_key"]):
            return OpportunityItem(
                module=component_name,
                cuadrante="NO RECOMENDADO",
                viabilidad_datos="baja",
                apetito_riesgo="bajo",
                valor_negocio="medio",
                justificacion="Componente de seguridad criptográfica con tolerancia cero a fallos y alucinaciones.",
                recomendacion_arquitectura="Utilizar primitivas criptográficas certificadas y algoritmos estándar en tiempo constante.",
            )

        # 2. Chequeo determinista
        for kw, (just, quad) in DETERMINISTIC_PATTERNS.items():
            if kw in combined:
                return OpportunityItem(
                    module=component_name,
                    cuadrante=quad,
                    viabilidad_datos="alta",
                    apetito_riesgo="medio",
                    valor_negocio="medio",
                    justificacion=just,
                    recomendacion_arquitectura="Implementar algoritmos determinísticos y código clásico (O(1) o O(N)) sin costo de inferencia.",
                )

        # 3. Chequeo de asistido por IA
        for kw, (just, quad) in AI_ASSISTED_PATTERNS.items():
            if kw in combined:
                return OpportunityItem(
                    module=component_name,
                    cuadrante=quad,
                    viabilidad_datos="alta",
                    apetito_riesgo="medio",
                    valor_negocio="alto",
                    justificacion=just,
                    recomendacion_arquitectura="Integrar modelo LLM asistido por RAG y validación estructurada de salida (Human-in-the-Loop).",
                )

        # 4. Si la descripción es muy pobre o vacía
        if len(description.strip()) < 10 and len(code_sample.strip()) < 10:
            return OpportunityItem(
                module=component_name,
                cuadrante="POR VALIDAR",
                viabilidad_datos="desconocida",
                apetito_riesgo="medio",
                valor_negocio="medio",
                justificacion="Información funcional insuficiente para discernir la pertinencia técnica y de negocio de IA.",
                recomendacion_arquitectura="Definir especificación funcional formal y perfil de datos antes de comprometer arquitectura.",
            )

        # Por defecto, tareas generales de código
        return OpportunityItem(
            module=component_name,
            cuadrante="AUTOMATIZABLE",
            viabilidad_datos="alta",
            apetito_riesgo="medio",
            valor_negocio="medio",
            justificacion="Lógica de negocio estándar resoluble mediante programación clásica.",
            recomendacion_arquitectura="Desarrollo determinístico orientado a objetos o funcional.",
        )

    def evaluate_repository(
        self,
        modules_info: List[Dict[str, Any]],
    ) -> AIOpportunityAssessmentResult:
        """Evalúa un conjunto de módulos de un repositorio y compila la matriz de la Sesión 01."""
        items: List[OpportunityItem] = []
        counts = {
            "AUTOMATIZABLE": 0,
            "ASISTIDO POR IA": 0,
            "NO RECOMENDADO": 0,
            "POR VALIDAR": 0,
        }

        for m in modules_info:
            name = m.get("name", m.get("path", "unnamed_module"))
            desc = m.get("description", "")
            code = m.get("code", "")
            item = self.evaluate_component(name, desc, code)
            items.append(item)
            counts[item.cuadrante] = counts.get(item.cuadrante, 0) + 1

        total = len(items)
        det_ratio = (counts["AUTOMATIZABLE"] / max(1, total)) * 100

        savings = f"{det_ratio:.0f}% de las capacidades evaluadas pueden resolverse mediante código determinístico sin costos de token."
        strategy = (
            "Priorizar modelos LLM exclusivamente en componentes generativos, explicativos o de síntesis (ASISTIDO POR IA), "
            "manteniendo el núcleo matemático, criptográfico y de análisis en motores deterministas."
        )

        return AIOpportunityAssessmentResult(
            total_evaluados=total,
            resumen_cuadrantes=counts,
            matriz=items,
            ahorro_potencial_computo=savings,
            recomendacion_estrategica=strategy,
        )

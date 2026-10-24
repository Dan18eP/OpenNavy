from typing import Dict, Any, List
from app.schemas.state import AnalysisState
from app.agents.nodes.llm_evaluator_node import _calculate_criterion_scores, _evaluate_architecture_findings, _evaluate_file_findings, _evaluate_duplication_findings, _evaluate_dependency_findings


def offline_synthesizer_node(state: AnalysisState) -> Dict[str, Any]:
    """
    Nodo Circuit Breaker / Offline Fallback (HU-CORE-03):
    Sintetiza los hallazgos exclusivamente mediante el motor matemático y determinístico
    cuando el LLM no está disponible, no hay claves configuradas o se activa --offline.
    Garantiza cero llamadas a la nube y cero excepciones no controladas.
    """
    files = state.get("files", [])
    static_metrics = state.get("static_metrics", {})
    arch_diff = state.get("architecture_diff", {})
    deps_info = state.get("dependencies", {})
    detected_secrets = state.get("detected_secrets", []) or []

    findings: List[Dict[str, Any]] = []

    # 1. Hallazgos determinísticos de secretos
    for sec in detected_secrets:
        findings.append({
            "file": sec.get("file", "unknown"),
            "function": None,
            "line": 1,
            "criterio": "security_secrets",
            "veredicto": "violacion",
            "explicacion": f"Credencial sensible en texto plano detectada ({sec.get('type')}: {sec.get('sample')}). Enmascarada forzosamente.",
            "fragmento_rag_citado": "security-privacy.md#secret-detection",
            "severidad": "critical",
            "sugerencia": "Eliminar la credencial y usar gestor de secretos.",
        })

    # 2. Hallazgos determinísticos de arquitectura (ciclos y capas)
    findings.extend(_evaluate_architecture_findings(arch_diff))

    # 3. Métricas AST por archivo (SOLID determinístico, CC, Clean Code)
    for file_info in files:
        findings.extend(_evaluate_file_findings(file_info))

    # 4. Duplicación y dependencias
    findings.extend(_evaluate_duplication_findings(static_metrics))
    findings.extend(_evaluate_dependency_findings(deps_info))

    # 5. Cálculo determinístico de scores
    eval_report = _calculate_criterion_scores(static_metrics, deps_info, findings)
    eval_report["mode"] = "deterministic_offline"
    eval_report["banner"] = "Generado en Modo Determinístico Offline (Motor Matemático OpenNavy)"

    return {
        "findings": findings,
        "solid_violations": findings,
        "evaluation_report": eval_report,
        "offline_mode": True,
        "current_step": "offline_synthesis_completed",
    }

from typing import Dict, Any, List, Optional
from app.schemas.state import AnalysisState
from app.core.config import settings


def _evaluate_architecture_findings(arch_diff: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Evalúa violaciones arquitectónicas de dependencias circulares y capas."""
    findings: List[Dict[str, Any]] = []
    if not arch_diff:
        return findings

    # Dependencias circulares
    if arch_diff.get("has_cycles"):
        for cycle in arch_diff.get("circular_dependencies", []):
            cycle_str = " → ".join(cycle)
            findings.append({
                "file": cycle[0] if cycle else "architecture",
                "function": None,
                "line": 1,
                "criterio": "architecture_guidelines",
                "veredicto": "violacion",
                "explicacion": (
                    f"Dependencia circular detectada: {cycle_str}. "
                    "Los módulos intermedios se referencian mutuamente, impidiendo la compilación/carga aislada, "
                    "generando acoplamiento bidireccional y aumentando la fragilidad ante cambios."
                ),
                "fragmento_rag_citado": "architecture-guidelines.md#acyclic-dependencies",
                "severidad": "critical",
                "sugerencia": (
                    "Romper el ciclo aplicando el Principio de Inversión de Dependencias (DIP): "
                    "extraer interfaces o tipos de datos compartidos a un módulo de abstracciones común "
                    "o inyectar la dependencia en tiempo de ejecución."
                ),
            })

    # Violaciones de capas
    for viol in arch_diff.get("layer_violations", []):
        src_m = viol.get("source_module", "architecture")
        tgt_m = viol.get("target_module", "internals")
        findings.append({
            "file": src_m,
            "function": None,
            "line": 1,
            "criterio": "architecture_guidelines",
            "veredicto": "violacion",
            "explicacion": (
                f"Violación de capas: El módulo '{src_m}' importa directamente '{tgt_m}', "
                "quebrando la regla de aislamiento de capas (presentación → dominio → infraestructura)."
            ),
            "fragmento_rag_citado": "ISO/IEC 5055:2021 & Clean Architecture (Robert C. Martin) | The Dependency Rule",
            "severidad": viol.get("severity", "high"),
            "sugerencia": "Reubicar la dependencia hacia la capa correspondiente o acceder mediante un puerto/interfaz en la capa de aplicación.",
        })

    return findings


def _check_srp_violation(file_path: str, fn: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Evalúa si una función viola el principio de responsabilidad única."""
    fn_name = fn.get("name", "")
    fn_loc = fn.get("lines_of_code", 0)
    fn_cc = fn.get("cyclomatic_complexity", 1)
    if fn_loc <= 45 and not (fn_loc > 25 and fn_cc > 7):
        return None

    return {
        "file": file_path,
        "function": fn_name,
        "line": fn.get("start_line", 1),
        "criterio": "solid_principles",
        "veredicto": "violacion",
        "explicacion": (
            f"La función '{fn_name}' acumula {fn_loc} líneas de código y CC={fn_cc}. "
            "Esto indica que asume múltiples responsabilidades (orquestación, transformación y persistencia/manejo de errores simultáneamente)."
        ),
        "fragmento_rag_citado": "Clean Architecture (Robert C. Martin) | Chapter 7: Single Responsibility Principle (SRP)",
        "severidad": "high" if fn_loc > 70 or fn_cc > 12 else "warning",
        "sugerencia": (
            "Extraer subtareas a métodos privados o clases colaboradoras especializadas (patrón Extract Method / Service Layer). "
            "Asegurar que cada función tenga una única razón para cambiar."
        ),
    }


def _check_cyclomatic_complexity(file_path: str, fn: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Evalúa si una función supera el umbral máximo de complejidad ciclomática."""
    fn_name = fn.get("name", "")
    fn_cc = fn.get("cyclomatic_complexity", 1)
    if fn_cc <= 10:
        return None

    return {
        "file": file_path,
        "function": fn_name,
        "line": fn.get("start_line", 1),
        "criterio": "cyclomatic_complexity",
        "veredicto": "violacion",
        "explicacion": (
            f"La función '{fn_name}' posee una Complejidad Ciclomática de {fn_cc} (umbral máximo: 10). "
            "El alto número de bifurcaciones independientes multiplica exponencialmente los caminos de prueba requeridos y el riesgo de bugs en producción."
        ),
        "fragmento_rag_citado": "NIST SP 500-235 / McCabe (SEI) | Section 3: Cyclomatic Complexity Risk Thresholds",
        "severidad": "critical" if fn_cc > 20 else "high",
        "sugerencia": "Reemplazar cascadas de 'if-elif-else' con un despachador de diccionario, polimorfismo o el patrón Strategy.",
    }


def _check_clean_code_standards(file_path: str, fn: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Evalúa violaciones a estándares Clean Code (parámetros y anidamiento)."""
    findings: List[Dict[str, Any]] = []
    fn_name = fn.get("name", "")
    fn_params = fn.get("parameters_count", 0)
    fn_nesting = fn.get("nesting_depth", 0)
    start_l = fn.get("start_line", 1)

    if fn_params > 3:
        findings.append({
            "file": file_path,
            "function": fn_name,
            "line": start_l,
            "criterio": "clean_code",
            "veredicto": "advertencia",
            "explicacion": (
                f"La función '{fn_name}' recibe {fn_params} argumentos posicionales (límite recomendado: ≤ 3). "
                "Firmas extensas aumentan el acoplamiento y la probabilidad de errores de orden en invocaciones."
            ),
            "fragmento_rag_citado": "Martin Fowler: Refactoring (2nd Ed.) | Chapter 3: Long Parameter List & Preserve Whole Object",
            "severidad": "warning",
            "sugerencia": "Empaquetar los parámetros cohesivos en un DTO (Data Transfer Object), Pydantic Model o Dataclass.",
        })

    if fn_nesting > 3:
        findings.append({
            "file": file_path,
            "function": fn_name,
            "line": start_l,
            "criterio": "clean_code",
            "veredicto": "advertencia",
            "explicacion": (
                f"La función '{fn_name}' alcanza una profundidad de anidamiento de {fn_nesting} niveles. "
                "Los bloques condicionales profundamente anidados saturan la carga cognitiva del desarrollador (Arrow Anti-pattern)."
            ),
            "fragmento_rag_citado": "Martin Fowler: Refactoring (2nd Ed.) | Replace Nested Conditional with Guard Clauses",
            "severidad": "warning",
            "sugerencia": "Aplicar Cláusulas de Guarda tempranas (Guard Clauses / Return Early) para aplanar la estructura del código.",
        })

    return findings


def _evaluate_file_findings(file_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Evalúa la mantenibilidad y funciones de un archivo específico."""
    findings: List[Dict[str, Any]] = []
    file_path = file_info.get("path", "")
    file_mi = file_info.get("maintainability_index", 100.0)

    if file_mi < 50.0:
        findings.append({
            "file": file_path,
            "function": None,
            "line": 1,
            "criterio": "maintainability_index",
            "veredicto": "violacion",
            "explicacion": (
                f"El archivo '{file_path}' presenta un Índice de Mantenibilidad crítico ({file_mi:.1f}/100). "
                "Combina un volumen Halstead elevado con múltiples ramas lógicas, lo que dificulta la comprensión y eleva el costo de modificación."
            ),
            "fragmento_rag_citado": "ISO/IEC 25010:2023 (Maintainability) & ISO/IEC 5055:2021 | Maintainability Index Thresholds",
            "severidad": "high",
            "sugerencia": "Dividir el archivo en submódulos especializados cohesivos y simplificar las expresiones booleanas y de control.",
        })

    for fn in file_info.get("functions", []):
        srp_res = _check_srp_violation(file_path, fn)
        if srp_res:
            findings.append(srp_res)

        cc_res = _check_cyclomatic_complexity(file_path, fn)
        if cc_res:
            findings.append(cc_res)

        findings.extend(_check_clean_code_standards(file_path, fn))

    return findings


def _evaluate_duplication_findings(static_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Evalúa métricas de duplicación de código en la base de código."""
    findings: List[Dict[str, Any]] = []
    dup_pct = static_metrics.get("duplication_percentage", 0.0)
    dup_lines = static_metrics.get("total_duplicated_lines", 0)

    if dup_pct > 5.0:
        findings.append({
            "file": "codebase",
            "function": None,
            "line": 1,
            "criterio": "code_duplication",
            "veredicto": "advertencia",
            "explicacion": (
                f"Se detectó un {dup_pct:.1f}% de código duplicado ({dup_lines} líneas clonadas en subárboles sintácticos Tipo 1 y 2). "
                "La redundancia de lógica multiplica el esfuerzo de mantenimiento y la probabilidad de correcciones inconsistentes."
            ),
            "fragmento_rag_citado": "Martin Fowler: Refactoring (2nd Ed.) | Chapter 3: Duplicated Code & Extract Function",
            "severidad": "high" if dup_pct > 15.0 else "warning",
            "sugerencia": "Centralizar la lógica común en funciones utilitarias o clases base compartidas aplicando el principio DRY (Don't Repeat Yourself).",
        })

    return findings


def _evaluate_single_dependency(dep: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Evalúa y construye el hallazgo correspondiente para una dependencia."""
    pkg_name = dep.get("package_name", "")
    status = dep.get("status", "up_to_date")
    cur_v = dep.get("current_version", "unspecified")
    rec_v = dep.get("recommended_version", "")
    reason = dep.get("reason", "")
    src_f = dep.get("source_file", "manifest")

    if status == "incompatible":
        return {
            "file": src_f,
            "function": None,
            "line": 1,
            "criterio": "dependency_version_control",
            "veredicto": "violacion",
            "explicacion": f"Incompatibilidad crítica en dependencia '{pkg_name}' (versión actual: {cur_v}): {reason}",
            "fragmento_rag_citado": "OWASP Top 10:2021 | A06: Vulnerable and Outdated Components (Incompatible Dependencies)",
            "severidad": "critical",
            "sugerencia": f"Actualizar a versión compatible '{rec_v}' ejecutando: {dep.get('upgrade_command', '')}",
        }
    elif status == "major_update":
        return {
            "file": src_f,
            "function": None,
            "line": 1,
            "criterio": "dependency_version_control",
            "veredicto": "advertencia",
            "explicacion": f"Dependencia '{pkg_name}' con versión mayor obsoleta (v{cur_v} → v{rec_v}). {reason}",
            "fragmento_rag_citado": "OWASP Top 10:2021 | A06: Vulnerable and Outdated Components & Semantic Versioning",
            "severidad": "high",
            "sugerencia": f"Planificar migración a v{rec_v} validando breaking changes: {dep.get('upgrade_command', '')}",
        }
    elif status in ("minor_update", "patch_update") and dep.get("risk_level") in ("medium", "high"):
        return {
            "file": src_f,
            "function": None,
            "line": 1,
            "criterio": "dependency_version_control",
            "veredicto": "sugerencia",
            "explicacion": f"Actualización disponible para '{pkg_name}' (v{cur_v} → v{rec_v}): {reason}",
            "fragmento_rag_citado": "OpenNavy Engineering Standard | Dependency Lifecycle Management",
            "severidad": "info",
            "sugerencia": f"Ejecutar: {dep.get('upgrade_command', '')}",
        }
    return None


def _evaluate_dependency_findings(deps_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Evalúa el listado de dependencias detectadas."""
    findings: List[Dict[str, Any]] = []
    deps_list = deps_info.get("dependencies", []) if deps_info else []
    for dep in deps_list:
        f = _evaluate_single_dependency(dep)
        if f:
            findings.append(f)
    return findings


def _calculate_criterion_scores(
    static_metrics: Dict[str, Any],
    deps_info: Dict[str, Any],
    findings: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Calcula las puntuaciones numéricas por criterio y el reporte global de evaluación."""
    avg_mi = static_metrics.get("average_maintainability_index", 75.0)
    avg_cc = static_metrics.get("average_cyclomatic_complexity", 2.0)
    dup_pct = static_metrics.get("duplication_percentage", 0.0)
    score_deps = float(deps_info.get("score", 100.0)) if deps_info else 100.0

    crit_count = sum(1 for f in findings if f.get("severidad") == "critical")
    high_count = sum(1 for f in findings if f.get("severidad") == "high")
    warn_count = sum(1 for f in findings if f.get("severidad") == "warning")

    score_mi = min(100.0, max(0.0, avg_mi))
    score_cc = min(100.0, max(0.0, 100.0 - (max(0.0, avg_cc - 3.0) * 10.0)))
    score_dup = min(100.0, max(0.0, 100.0 - (dup_pct * 8.0)))
    score_arch = min(100.0, max(0.0, 100.0 - (crit_count * 25.0 + high_count * 10.0)))
    score_solid = min(100.0, max(0.0, 100.0 - (high_count * 15.0 + warn_count * 5.0)))
    score_clean = min(100.0, max(0.0, 100.0 - (warn_count * 8.0)))
    score_coverage = 85.0

    criterion_scores = {
        "maintainability_index": round(score_mi, 1),
        "cyclomatic_complexity": round(score_cc, 1),
        "solid_principles": round(score_solid, 1),
        "code_duplication": round(score_dup, 1),
        "test_coverage": round(score_coverage, 1),
        "architecture": round(score_arch, 1),
        "clean_code": round(score_clean, 1),
        "dependency_version_control": round(score_deps, 1),
    }

    global_score = sum(
        criterion_scores.get(crit, 75.0) * weight
        for crit, weight in settings.CRITERIA_WEIGHTS.items()
    )
    global_score = round(min(100.0, max(0.0, global_score)), 1)

    return {
        "global_score": global_score,
        "criterion_scores": criterion_scores,
        "total_findings": len(findings),
        "critical_findings": crit_count,
        "high_findings": high_count,
        "warning_findings": warn_count,
        "is_healthy": global_score >= settings.CRITICAL_SCORE_THRESHOLD,
    }


def llm_evaluator_node(state: AnalysisState) -> Dict[str, Any]:
    """
    Nodo 4: Agente Evaluador RAG.
    Evalúa el código contra la rúbrica recuperada y genera hallazgos cualitativos estructurados y específicos.
    """
    files = state.get("files", [])
    static_metrics = state.get("static_metrics", {})
    arch_diff = state.get("architecture_diff", {})
    deps_info = state.get("dependencies", {})

    findings: List[Dict[str, Any]] = []

    # 1. Hallazgos de Seguridad (Secretos enmascarados forzosamente)
    detected_secrets = state.get("detected_secrets", []) or []
    for sec in detected_secrets:
        sec_file = sec.get("file", "unknown")
        sec_type = sec.get("type", "Secret")
        sec_sample = sec.get("sample", "****")
        findings.append({
            "file": sec_file,
            "function": None,
            "line": 1,
            "criterio": "security_secrets",
            "veredicto": "violacion",
            "explicacion": (
                f"Se detectó una credencial sensible en texto plano ({sec_type}: {sec_sample}). "
                "OpenNavy ha enmascarado forzosamente este valor para evitar fugas de información antes de cualquier interacción con modelos LLM."
            ),
            "fragmento_rag_citado": "OWASP Top 10:2021 | A02: Cryptographic Failures & A07: Identification and Authentication Failures (Hardcoded Credentials)",
            "severidad": "critical",
            "sugerencia": "Eliminar inmediatamente la credencial del código fuente, rotarla y utilizar variables de entorno o un gestor de secretos (ej. Vault, AWS Secrets Manager).",
        })

    # 2. Arquitectura
    findings.extend(_evaluate_architecture_findings(arch_diff))

    # 3. Archivos y funciones (SOLID, Clean Code, Mantenibilidad, McCabe)
    for file_info in files:
        findings.extend(_evaluate_file_findings(file_info))

    # 4. Duplicación de Código
    findings.extend(_evaluate_duplication_findings(static_metrics))

    # 5. Control de Versiones de Dependencias
    findings.extend(_evaluate_dependency_findings(deps_info))

    # 6. Evaluación Cualitativa con LLM (si está disponible y hay archivos)
    llm = None
    try:
        from app.core.llm import get_llm
        llm = get_llm(temperature=0.2)
    except Exception:
        pass

    if llm and files:
        rag_context = state.get("rag_context", [])
        rag_summary = "\n".join([f"- {c.get('criterion', '')}: {c.get('content', '')[:180]}..." for c in rag_context])
        try:
            # Invocar LLM sobre los primeros 3 archivos más complejos
            target_files = sorted(files, key=lambda f: f.get("cyclomatic_complexity_total", 0), reverse=True)[:3]
            for tf in target_files:
                code_snippet = (tf.get("raw_content") or "")[:1200]
                if code_snippet:
                    from app.analyzers.prompt_shield import wrap_untrusted_code
                    wrapped = wrap_untrusted_code(code_snippet, file_path=tf.get("path", "file"), language=tf.get("language", ""))
                    prompt_user = (
                        f"Evalúa este módulo contra la rúbrica RAG:\n{rag_summary}\n\n"
                        f"{wrapped}\n"
                        "Retorna hallazgos técnicos en formato conciso."
                    )
                    ai_resp = llm.invoke([
                        {"role": "system", "content": "Eres el Almirante de OpenNavy, auditor senior de arquitectura. Evalúa modularidad y principios de diseño."},
                        {"role": "user", "content": prompt_user}
                    ])
                    resp_text = ai_resp.content if hasattr(ai_resp, "content") else str(ai_resp)
                    if resp_text and len(resp_text) > 30:
                        findings.append({
                            "file": tf.get("path", "file"),
                            "function": None,
                            "line": 1,
                            "criterio": "llm_contextual_review",
                            "veredicto": "sugerencia",
                            "explicacion": resp_text[:350],
                            "fragmento_rag_citado": "ISO/IEC 25010:2023 (Modularity) & Clean Architecture | Domain Boundaries",
                            "severidad": "info",
                            "sugerencia": "Revisar la modularidad y cohesión funcional según el análisis contextual del LLM.",
                        })
        except Exception:
            pass

    # 7. Cálculo de Scores
    eval_report = _calculate_criterion_scores(static_metrics, deps_info, findings)

    return {
        "findings": findings,
        "solid_violations": findings,
        "evaluation_report": eval_report,
        "current_step": "rag_evaluation_completed",
    }

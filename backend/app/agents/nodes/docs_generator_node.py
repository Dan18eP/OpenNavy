from datetime import datetime
from typing import Dict, Any, List
from app.schemas.state import AnalysisState


def _build_circular_dependencies_adr(repo_name: str, now_str: str, cycles: List[List[str]]) -> Dict[str, Any]:
    """Genera el documento de Architecture Decision Record (ADR) para dependencias circulares."""
    cycles_desc = "\n".join([f"- `{' -> '.join(c)}`" for c in cycles])
    adr_content = f"""# ADR-0001: Ruptura de Dependencias Circulares en {repo_name}

**Fecha:** {now_str}  
**Estado:** Propuesto (Autogenerado por Praxia)  
**Severidad:** Crítica  

---

## Contexto y Problemática
Durante el análisis estático y de arquitectura del repositorio `{repo_name}`, se detectaron ciclos de importación cerrados entre los siguientes módulos:
{cycles_desc}

Las dependencias circulares violan el principio **Acyclic Dependencies Principle (ADP)**, impiden el testing unitario desacoplado y provocan errores de importación en tiempo de ejecución.

---

## Decisión Técnica Recomendada
1. Extraer las interfaces, contratos o tipos compartidos a un módulo de nivel inferior (ej. `core/types` o `domain/contracts`).
2. Aplicar el principio de **Inversión de Dependencias (DIP)**: hacer que los módulos de alto nivel dependan de abstracciones y no de implementaciones concretas.

---

## Consecuencias
- **Positivas:** Desacoplamiento total entre subsistemas, mayor testabilidad con mocks independientes, prevención de fallos de inicialización.
- **Riesgos:** Requiere refactorizar las firmas de importación de los módulos afectados.
"""
    return {
        "tipo": "adr",
        "path": f"adrs/ADR-0001-breaking-circular-dependencies-{repo_name}.md",
        "titulo": f"ADR-0001: Ruptura de Dependencias Circulares en {repo_name}",
        "contenido": adr_content,
    }


def _build_architecture_summary(repo_name: str, now_str: str, eval_report: Dict[str, Any]) -> Dict[str, Any]:
    """Genera el documento resumen de salud de arquitectura en formato Markdown."""
    scores = eval_report.get("criterion_scores", {})
    summary_content = f"""# Resumen de Salud de Arquitectura: {repo_name}

**Identificador:** `module_doc_{repo_name.lower().replace('-', '_')}`  
**Tipo:** `module_doc`  
**Categoría:** Documentación Viva de Repositorio  
**Autoridad:** Praxia Architecture Synthesizer  
**Rule-ID:** PRAXIA-LIVE-DOC-01  
**Fecha:** {now_str}  
**Score Global de Calidad:** {eval_report.get('global_score', 0.0)} / 100  
**Estado:** {"SALUDABLE" if eval_report.get('is_healthy') else "REQUIERE ATENCIÓN"}  

---

## 📊 Desglose de Criterios
| Criterio | Puntaje |
|---|---|
| Índice de Mantenibilidad | {scores.get('maintainability_index', 0)} / 100 |
| Complejidad Ciclomática | {scores.get('cyclomatic_complexity', 0)} / 100 |
| Principios SOLID | {scores.get('solid_principles', 0)} / 100 |
| Duplicación de Código | {scores.get('code_duplication', 0)} / 100 |
| Directrices de Arquitectura | {scores.get('architecture', 0)} / 100 |
| Clean Code | {scores.get('clean_code', 0)} / 100 |

---

## 🔍 Hallazgos Principales
- **Total de Hallazgos:** {eval_report.get('total_findings', 0)}
- **Hallazgos Críticos:** {eval_report.get('critical_findings', 0)}
- **Hallazgos de Severidad Alta:** {eval_report.get('high_findings', 0)}
- **Advertencias:** {eval_report.get('warning_findings', 0)}
"""
    return {
        "tipo": "summary",
        "path": f"module-docs/{repo_name}-architecture-summary.md",
        "titulo": f"Resumen de Arquitectura: {repo_name}",
        "contenido": summary_content,
    }


def docs_generator_node(state: AnalysisState) -> Dict[str, Any]:
    """Nodo 5: Genera automáticamente ADRs y resúmenes técnicos en Markdown."""
    repo_url = state.get("repo_url", "repo")
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    arch_diff = state.get("architecture_diff", {})
    eval_report = state.get("evaluation_report", {})
    now_str = datetime.utcnow().strftime("%Y-%m-%d")

    generated_docs: List[Dict[str, Any]] = []

    # 1. Generar ADR si hay dependencias circulares detectadas (Tarjan)
    if arch_diff.get("has_cycles"):
        prelim_adr = arch_diff.get("preliminary_adr")
        if prelim_adr and prelim_adr.get("content"):
            generated_docs.append({
                "tipo": "adr",
                "path": prelim_adr.get("filename", f"adrs/ADR-0001-breaking-circular-dependencies-{repo_name}.md"),
                "titulo": prelim_adr.get("title", f"ADR-0001: Ruptura de Dependencias Circulares en {repo_name}"),
                "contenido": prelim_adr.get("content"),
            })
        else:
            cycles = arch_diff.get("circular_dependencies", [])
            generated_docs.append(_build_circular_dependencies_adr(repo_name, now_str, cycles))

    # 2. Generar Resumen General del Análisis de Arquitectura
    generated_docs.append(_build_architecture_summary(repo_name, now_str, eval_report))

    return {
        "generated_docs": generated_docs,
        "current_step": "generating_docs_completed",
    }

from typing import Dict, Any
from app.schemas.state import AnalysisState
from app.analyzers.manager import AnalyzerManager


def static_analysis_node(state: AnalysisState) -> Dict[str, Any]:
    """Nodo 2: Ejecuta el análisis estático universal (AST, métricas, duplicación y arquitectura)."""
    local_path = state.get("local_path")
    if not local_path:
        errors = list(state.get("errors", []))
        errors.append("No se encontró local_path para análisis estático.")
        return {"errors": errors, "current_step": "failed"}

    manager = AnalyzerManager()
    try:
        results = manager.analyze_repository(local_path)

        # Convertir FileNode objects a diccionarios para serialización en LangGraph
        serializable_files = [node.model_dump() for node in results.get("file_nodes", [])]

        return {
            "languages_detected": results.get("languages", []),
            "files": serializable_files,
            "static_metrics": results.get("summary_metrics", {}),
            "complexity_findings": results.get("complex_functions", []),
            "architecture_diff": results.get("architecture", {}),
            "architecture_profile": results.get("architecture_profile", {}),
            "dependencies": results.get("dependencies", {}),
            "detected_secrets": results.get("detected_secrets", []),
            "current_step": "static_analysis_completed",
        }
    except Exception as e:
        errors = list(state.get("errors", []))
        errors.append(f"Error en análisis estático: {str(e)}")
        return {"errors": errors, "current_step": "failed"}

from typing import Dict, Any
from pathlib import Path
from app.schemas.state import AnalysisState
from app.analyzers.architecture_detector import ArchitecturePatternDetector


def architecture_inference_node(state: AnalysisState) -> Dict[str, Any]:
    """
    Nodo Atómico: Inferencia de Patrones de Arquitectura y Regla de Dependencia (HU-ANALYSIS-02).
    Clasifica el estilo arquitectónico dominante (Clean, Hexagonal, MVC, Layered, etc.),
    identifica las capas formales y valida el cumplimiento estricto de la Dependency Rule.
    """
    local_path = state.get("local_path")
    files = state.get("files", [])
    arch_diff = state.get("architecture_diff", {})

    if not local_path or not files:
        return {
            "current_step": "architecture_inference_skipped",
        }

    detector = ArchitecturePatternDetector()
    root_path = Path(local_path)

    # Reconstruir FileNode ligeros a partir de los diccionarios de archivos si es necesario
    from app.schemas.state import FileNode
    file_nodes = []
    for f in files:
        try:
            file_nodes.append(FileNode(**f))
        except Exception:
            pass

    graph = arch_diff.get("graph", {})
    arch_profile = detector.analyze_architecture(file_nodes, graph, root_path)

    # Si se detectaron violaciones adicionales de la Dependency Rule, agregarlas a layer_violations
    layer_violations = list(arch_diff.get("layer_violations", []))
    for viol in arch_profile.get("dependency_rule_violations", []):
        layer_violations.append({
            "source_module": viol.get("source_module", viol.get("source_file")),
            "target_module": viol.get("target_module", viol.get("target_file")),
            "rule": viol.get("rule"),
            "severity": viol.get("severity", "high"),
            "suggestion": viol.get("suggestion"),
        })

    arch_diff["layer_violations"] = layer_violations

    return {
        "architecture_profile": arch_profile,
        "architecture_diff": arch_diff,
        "current_step": "architecture_inference_completed",
    }

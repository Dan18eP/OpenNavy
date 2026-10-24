"""
Detector e inferidor de patrones arquitectónicos y cumplimiento de Dependency Rule (HU-ANALYSIS-02).

Clasifica el estilo arquitectónico dominante entre:
- Clean Architecture
- Ports & Adapters (Hexagonal)
- Layered / 3-Tier
- MVC
- Microservices / Modular

Identifica las capas de dominio, aplicación, infraestructura y presentación.
Detecta violaciones de la Dependency Rule y calcula la métrica:
`dependency_rule_compliance` (porcentaje de 0.0 a 100.0).
"""

from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple
from app.schemas.state import FileNode


DOMAINS_KEYWORDS = {
    "domain", "entities", "entity", "model", "models", "core/domain",
    "business", "aggregates", "value_objects"
}
APPLICATION_KEYWORDS = {
    "application", "use_cases", "usecase", "usecases", "services",
    "service", "handlers", "commands", "queries", "interactors"
}
INFRASTRUCTURE_KEYWORDS = {
    "infrastructure", "infra", "adapters", "database", "db", "repositories",
    "repository", "external", "persistence", "gateways", "clients"
}
PRESENTATION_KEYWORDS = {
    "api", "controllers", "controller", "endpoints", "views", "view",
    "routes", "router", "web", "graphql", "rest", "ui", "interfaces"
}

# Firmas de patrones arquitectónicos dominantes
PATTERN_SIGNATURES = {
    "Clean Architecture": {
        "required_layers": {"domain", "application", "infrastructure"},
        "path_indicators": {"domain", "application", "infrastructure", "entities", "use_cases"},
    },
    "Ports & Adapters (Hexagonal)": {
        "required_layers": {"domain", "infrastructure"},
        "path_indicators": {"ports", "adapters", "hexagonal", "inbound", "outbound", "driven", "driving"},
    },
    "MVC": {
        "required_layers": {"domain", "presentation"},
        "path_indicators": {"models", "views", "controllers", "mvc"},
    },
    "Layered / 3-Tier": {
        "required_layers": {"domain", "presentation"},
        "path_indicators": {"layers", "tier", "services", "dao", "dto", "dal"},
    },
    "Microservices / Modular": {
        "required_layers": set(),
        "path_indicators": {"modules", "packages", "services", "subservices", "microservices"},
    },
}


class ArchitecturePatternDetector:
    """Motor de inferencia de topología arquitectónica y validación de Dependency Rule."""

    def classify_layer(self, path_str: str) -> str:
        """
        Clasifica un archivo o módulo en una capa arquitectónica formal:
        - 'domain'
        - 'application'
        - 'infrastructure'
        - 'presentation'
        - 'cross_cutting' / 'unknown'
        """
        clean_path = path_str.replace("\\", "/").lower()
        parts = [p for p in clean_path.split("/") if p]

        # Priorizar coincidencias directas en segmentos de ruta
        for part in parts:
            if part in DOMAINS_KEYWORDS:
                return "domain"
            if part in APPLICATION_KEYWORDS:
                return "application"
            if part in INFRASTRUCTURE_KEYWORDS:
                return "infrastructure"
            if part in PRESENTATION_KEYWORDS:
                return "presentation"

        # Coincidencias en sufijos o nombres
        for kw in DOMAINS_KEYWORDS:
            if kw in clean_path:
                return "domain"
        for kw in APPLICATION_KEYWORDS:
            if kw in clean_path:
                return "application"
        for kw in INFRASTRUCTURE_KEYWORDS:
            if kw in clean_path:
                return "infrastructure"
        for kw in PRESENTATION_KEYWORDS:
            if kw in clean_path:
                return "presentation"

        return "unknown"

    def infer_pattern(
        self,
        file_paths: List[str],
        layers_detected: Dict[str, List[str]]
    ) -> Tuple[str, float]:
        """
        Determina el patrón dominante y el grado de confianza (0.0 a 1.0).
        """
        all_text = " ".join([p.replace("\\", "/").lower() for p in file_paths])
        scores: Dict[str, float] = {}

        present_layers = {layer for layer, files in layers_detected.items() if len(files) > 0 and layer != "unknown"}

        for pattern_name, sig in PATTERN_SIGNATURES.items():
            score = 0.0
            indicators = sig["path_indicators"]
            req_layers = sig["required_layers"]

            # Evaluación de capas presentes
            if req_layers:
                layer_overlap = len(req_layers.intersection(present_layers))
                score += (layer_overlap / len(req_layers)) * 50.0

            # Evaluación de palabras clave en rutas
            matched_indicators = sum(1 for ind in indicators if ind in all_text)
            score += min(50.0, matched_indicators * 12.0)

            scores[pattern_name] = score

        # Patrón dominante
        best_pattern = max(scores, key=scores.get)
        best_score = scores[best_pattern]
        confidence = round(min(1.0, max(0.2, best_score / 100.0)), 2)

        if best_score < 20.0:
            return "Layered / 3-Tier", 0.50

        return best_pattern, confidence

    def detect_dependency_rule_violations(
        self,
        file_nodes: List[FileNode],
        adjacency_list: Dict[str, List[str]],
        module_to_file: Dict[str, str],
    ) -> List[Dict[str, Any]]:
        """
        Evalúa la Dependency Rule de Clean Architecture / Hexagonal:
        - Domain NO debe depender de Application, Infrastructure ni Presentation.
        - Application NO debe depender de Infrastructure ni Presentation.
        - Regla fundamental: Las dependencias solo pueden apuntar HACIA EL INTERIOR (hacia Domain).
        """
        violations: List[Dict[str, Any]] = []

        for src_mod, targets in adjacency_list.items():
            src_file = module_to_file.get(src_mod, src_mod)
            src_layer = self.classify_layer(src_file)

            for tgt_mod in targets:
                tgt_file = module_to_file.get(tgt_mod, tgt_mod)
                tgt_layer = self.classify_layer(tgt_file)

                # Regla 1: Dominio nunca depende de capas externas
                if src_layer == "domain" and tgt_layer in ("infrastructure", "presentation", "application"):
                    violations.append({
                        "source_file": src_file,
                        "source_module": src_mod,
                        "source_layer": src_layer,
                        "target_file": tgt_file,
                        "target_module": tgt_mod,
                        "target_layer": tgt_layer,
                        "severity": "critical",
                        "rule": f"El núcleo de dominio ({src_mod}) no debe importar la capa externa {tgt_layer} ({tgt_mod}).",
                        "suggestion": (
                            "Invertir la dependencia: declarar una interfaz (puerto) en el dominio "
                            "e implementar el adaptador en la infraestructura."
                        ),
                    })
                # Regla 2: Aplicación no debe depender directamente de Infraestructura o Presentación
                elif src_layer == "application" and tgt_layer in ("infrastructure", "presentation"):
                    violations.append({
                        "source_file": src_file,
                        "source_module": src_mod,
                        "source_layer": src_layer,
                        "target_file": tgt_file,
                        "target_module": tgt_mod,
                        "target_layer": tgt_layer,
                        "severity": "high",
                        "rule": f"La capa de aplicación ({src_mod}) no debe depender directamente de {tgt_layer} ({tgt_mod}).",
                        "suggestion": "Utilizar inyección de dependencias a través de interfaces de abstracción.",
                    })

        return violations

    def analyze_architecture(
        self,
        file_nodes: List[FileNode],
        adjacency_list: Dict[str, List[str]],
        repo_root: Path,
    ) -> Dict[str, Any]:
        """
        Ejecuta el análisis completo de topología arquitectónica.
        """
        # Mapeo de módulo a archivo
        module_to_file: Dict[str, str] = {}
        for node in file_nodes:
            try:
                rel = str(Path(node.path).relative_to(repo_root)).replace("\\", "/")
            except ValueError:
                rel = str(node.path).replace("\\", "/")
            # Registrar canonical
            clean_rel = rel
            for ext in (".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java"):
                if clean_rel.endswith(ext):
                    clean_rel = clean_rel[:-len(ext)]
                    break
            module_to_file[clean_rel] = rel

        # Clasificación de archivos por capas
        layers_map: Dict[str, List[str]] = {
            "domain": [],
            "application": [],
            "infrastructure": [],
            "presentation": [],
            "unknown": [],
        }

        all_paths = []
        for node in file_nodes:
            rel = module_to_file.get(node.path, node.path)
            all_paths.append(rel)
            layer = self.classify_layer(rel)
            layers_map.setdefault(layer, []).append(rel)

        pattern, confidence = self.infer_pattern(all_paths, layers_map)
        violations = self.detect_dependency_rule_violations(file_nodes, adjacency_list, module_to_file)

        # Cálculo de métrica de cumplimiento de la Regla de Dependencia
        total_cross_layer_dependencies = 0
        for src_mod, targets in adjacency_list.items():
            src_file = module_to_file.get(src_mod, src_mod)
            src_layer = self.classify_layer(src_file)
            for tgt_mod in targets:
                tgt_file = module_to_file.get(tgt_mod, tgt_mod)
                tgt_layer = self.classify_layer(tgt_file)
                if src_layer != tgt_layer and src_layer != "unknown" and tgt_layer != "unknown":
                    total_cross_layer_dependencies += 1

        if total_cross_layer_dependencies == 0:
            compliance = 100.0
        else:
            invalid_count = len(violations)
            compliance = round(max(0.0, 100.0 - ((invalid_count / total_cross_layer_dependencies) * 100.0)), 1)

        return {
            "dominant_pattern": pattern,
            "pattern_confidence": confidence,
            "layers": {
                "domain_files_count": len(layers_map.get("domain", [])),
                "application_files_count": len(layers_map.get("application", [])),
                "infrastructure_files_count": len(layers_map.get("infrastructure", [])),
                "presentation_files_count": len(layers_map.get("presentation", [])),
                "unknown_files_count": len(layers_map.get("unknown", [])),
            },
            "layers_breakdown": layers_map,
            "dependency_rule_violations": violations,
            "dependency_rule_violations_count": len(violations),
            "dependency_rule_compliance": compliance,
        }

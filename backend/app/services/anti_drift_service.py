import os
import logging
from pathlib import Path
from typing import Dict, List, Set, Any, Optional

from app.schemas.state import FileNode
from app.analyzers.treesitter_engine import TreeSitterEngine
from app.analyzers.dependency_graph import DependencyGraphAnalyzer

logger = logging.getLogger(__name__)

# Extensiones de archivos soportadas para analisis topologico
SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".go": "go",
    ".java": "java",
}

# Definicion de capas para Arquitectura Hexagonal
HEXAGONAL_LAYERS = {
    "domain": ["domain", "entities", "models"],
    "application": ["services", "usecases", "workflows"],
    "analyzers": ["analyzers", "parsers", "engine"],
    "infrastructure": ["infrastructure", "adapters", "database", "storage"],
    "api": ["api", "endpoints", "routers", "controllers", "webhooks"],
}


class AntiDriftService:
    """
    Motor Anti Code Drift (Prevencion de la Deriva Arquitectonica).
    Supervisa la topografia del codigo, calcula el radio de impacto (Blast Radius),
    valida limites de capas hexagonales y detecta arrecifes de dependencias ciclicas con Tarjan.
    """

    def __init__(self):
        self.ts_engine = TreeSitterEngine()
        self.graph_analyzer = DependencyGraphAnalyzer()
        # Cache en memoria de grafos de repositorios: repo_id/path -> topografia
        self._topography_cache: Dict[str, Dict[str, Any]] = {}

    def get_repo_ast_topography(self, repo_path: str, max_files: int = 50) -> Dict[str, Any]:
        """
        Escanea el directorio local del repositorio y compila su topografia AST
        y componentes fuertemente conexos (SCC) mediante Tarjan en menos de 1 segundo.
        """
        cache_key = str(Path(repo_path).resolve())
        if cache_key in self._topography_cache:
            return self._topography_cache[cache_key]

        root = Path(repo_path)
        if not root.exists() or not root.is_dir():
            logger.warning(f"[AntiDrift] Ruta de repositorio no valida o inexistente: {repo_path}")
            return {"files": [], "symbols": {}, "scc_cycles": [], "adjacency": {}, "total_modules": 0}

        file_nodes: List[FileNode] = []
        symbols_map: Dict[str, List[str]] = {}
        scanned_count = 0

        # Directorios a excluir de la exploracion
        ignored_dirs = {
            ".git", "node_modules", ".venv", "venv", "env", "__pycache__",
            "dist", "build", ".pytest_cache", ".next", "coverage", "assets"
        }

        for path in root.rglob("*"):
            if scanned_count >= max_files:
                break
            suffix = path.suffix.lower()
            if path.is_file() and suffix in SUPPORTED_EXTENSIONS:
                if any(ignored in path.parts for ignored in ignored_dirs):
                    continue

                try:
                    rel_path = str(path.relative_to(root)).replace("\\", "/")
                    content = path.read_text(encoding="utf-8", errors="ignore")
                    lang = SUPPORTED_EXTENSIONS[suffix]

                    # Parseo exacto de imports, clases y funciones con Tree-sitter
                    node = self.ts_engine.parse_source(rel_path, content, lang)
                    if node:
                        file_nodes.append(node)

                        # Registrar nombres de clases y funciones para alimentar contexto
                        syms = [c.name for c in node.classes] + [f.name for f in node.functions]
                        if syms:
                            symbols_map[rel_path] = syms[:6]

                        scanned_count += 1
                except Exception as e:
                    logger.debug(f"[AntiDrift] Error parseando archivo {path}: {e}")

        # Ejecutar Algoritmo de Tarjan para detectar ciclos fuertemente conexos
        graph_data = self.graph_analyzer.build_graph(file_nodes, root)
        scc_cycles = graph_data.get("cycles_detailed", [])
        adjacency = graph_data.get("graph", {})

        topography = {
            "repo_path": str(root),
            "total_modules": len(file_nodes),
            "files": [n.path for n in file_nodes],
            "symbols": symbols_map,
            "scc_cycles": scc_cycles,
            "adjacency": adjacency,
            "timestamp": graph_data.get("timestamp"),
        }

        self._topography_cache[cache_key] = topography
        return topography

    def calculate_blast_radius(
        self,
        adjacency: Dict[str, List[str]],
        target_files: List[str],
    ) -> Dict[str, Any]:
        """
        Calcula el radio de impacto aguas arriba.
        Determina que otros modulos del sistema colapsarian o requeririan re-testing
        si los archivos objetivo sufren modificaciones o cambios en sus contratos publicos.
        """
        # Normalizar paths objetivo
        normalized_targets = {f.replace("\\", "/").rstrip("/") for f in target_files}

        # Construir grafo inverso (quien depende de quien)
        reverse_graph: Dict[str, Set[str]] = {}
        for source, targets in adjacency.items():
            norm_source = source.replace("\\", "/")
            for tgt in targets:
                norm_tgt = tgt.replace("\\", "/")
                if norm_tgt not in reverse_graph:
                    reverse_graph[norm_tgt] = set()
                reverse_graph[norm_tgt].add(norm_source)

        direct_dependents: Set[str] = set()
        indirect_dependents: Set[str] = set()

        for target in normalized_targets:
            # Buscar coincidencia exacta o por subcadena de modulo
            matching_keys = [k for k in reverse_graph.keys() if target in k or k in target]
            for key in matching_keys:
                dependents = reverse_graph[key]
                for dep in dependents:
                    if dep not in normalized_targets:
                        direct_dependents.add(dep)

        # Calculo de dependientes indirectos (segundo grado)
        for dep in list(direct_dependents):
            if dep in reverse_graph:
                for second_dep in reverse_graph[dep]:
                    if second_dep not in normalized_targets and second_dep not in direct_dependents:
                        indirect_dependents.add(second_dep)

        total_impact = len(direct_dependents) + len(indirect_dependents)
        if total_impact == 0:
            severity = "LOW"
        elif total_impact <= 3:
            severity = "MEDIUM"
        elif total_impact <= 8:
            severity = "HIGH"
        else:
            severity = "CRITICAL"

        return {
            "severity": severity,
            "total_affected_count": total_impact,
            "direct_dependents": sorted(list(direct_dependents)),
            "indirect_dependents": sorted(list(indirect_dependents)),
        }

    def validate_layer_drift(
        self,
        source_file: str,
        imported_modules: List[str],
    ) -> List[Dict[str, Any]]:
        """
        Valida que las importaciones no violen las reglas de dependencia de la Arquitectura Hexagonal.
        Regla central: Las capas internas (dominio) jamas deben depender de capas externas (infra/api).
        """
        source_norm = source_file.replace("\\", "/").lower()
        source_layer = self._detect_layer(source_norm)
        violations = []

        if not source_layer:
            return violations

        for imp in imported_modules:
            imp_norm = imp.replace("\\", "/").replace(".", "/").lower()
            target_layer = self._detect_layer(imp_norm)

            if not target_layer or target_layer == source_layer:
                continue

            # Regla 1: Dominio no puede importar aplicacion, infraestructura ni api
            if source_layer == "domain" and target_layer in ("application", "infrastructure", "api"):
                violations.append({
                    "source_file": source_file,
                    "target_import": imp,
                    "rule": f"Layer Violation: Domain cannot import from {target_layer.capitalize()}.",
                    "severity": "CRITICAL",
                    "suggestion": f"Invertir la dependencia (DIP): definir una interfaz o puerto en dominio e implementar en {target_layer}."
                })

            # Regla 2: Servicios de aplicacion no pueden importar infraestructura directa ni api
            elif source_layer == "application" and target_layer == "api":
                violations.append({
                    "source_file": source_file,
                    "target_import": imp,
                    "rule": "Layer Violation: Application services cannot import API drivers.",
                    "severity": "HIGH",
                    "suggestion": "La capa de API debe llamar a la capa de Aplicacion, no en reversa."
                })

        return violations

    def evaluate_course_drift(
        self,
        repo_name: str,
        waypoints: List[Dict[str, Any]],
        repo_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Evalua integralmente el plan de navegacion de waypoints generado por Gemma 4.
        Cruza los waypoints con la topografia de Tarjan y el calculo de Blast Radius
        para alertar riesgo de deriva de codigo antes de su ejecucion.
        """
        target_files = [w.get("file", "") for w in waypoints if w.get("file")]

        # Obtener topografia si hay ruta disponible o en cache
        topography = {}
        if repo_path and Path(repo_path).exists():
            topography = self.get_repo_ast_topography(repo_path)
        elif self._topography_cache:
            topography = next(iter(self._topography_cache.values()))

        adjacency = topography.get("adjacency", {})
        scc_cycles = topography.get("scc_cycles", [])

        # 1. Calculo de Blast Radius
        blast_radius = self.calculate_blast_radius(adjacency, target_files)

        # 2. Deteccion de Arrecifes de Tarjan (si los waypoints tocan archivos en ciclos existentes)
        reef_warnings: List[str] = []
        for cycle_info in scc_cycles:
            cycle_nodes = cycle_info.get("cycle", [])
            for target in target_files:
                norm_target = target.replace("\\", "/")
                matched = any(norm_target in node or node in norm_target for node in cycle_nodes)
                if matched:
                    cycle_preview = " -> ".join(cycle_nodes[:4])
                    reef_warnings.append(
                        f"Arrecife de Codigo Detectado: El waypoint '{target}' forma parte de un ciclo de dependencias fuertemente conexo (Tarjan SCC): [{cycle_preview}]. Modificarlo sin precaucion puede causar efectos colaterales."
                    )

        # 3. Determinacion del Nivel de Riesgo Global de Deriva
        drift_risk = blast_radius.get("severity", "LOW")
        if reef_warnings and drift_risk in ("LOW", "MEDIUM"):
            drift_risk = "HIGH"

        # 4. Generacion de Recomendacion Arquitectonica (ADR preliminar)
        adr_rec = ""
        if reef_warnings or drift_risk in ("HIGH", "CRITICAL"):
            adr_rec = (
                f"Recomendacion Anti-Deriva: Aplicar el Principio de Inversion de Dependencias (DIP) "
                f"sobre los waypoints acoplados. Extraer contratos de interfaz para aislar '{', '.join(target_files[:3])}' "
                f"y ejecutar pruebas de regresion sobre los {blast_radius.get('total_affected_count', 0)} modulos en su radio de impacto."
            )

        return {
            "drift_risk": drift_risk,
            "blast_radius": blast_radius,
            "reef_warnings": reef_warnings if reef_warnings else ["No se detectaron arrecifes de acoplamiento critico en estos waypoints."],
            "adr_recommendation": adr_rec,
        }

    def are_modules_coupled_via_tarjan(self, file_a: str, file_b: str) -> bool:
        """
        Determina si dos archivos estan acoplados topologicamente segun la matriz de Tarjan
        o si comparten aristas directas en el grafo de dependencias.
        """
        norm_a = file_a.replace("\\", "/").rstrip("/")
        norm_b = file_b.replace("\\", "/").rstrip("/")

        for topo in self._topography_cache.values():
            # 1. Comprobar si comparten un ciclo fuertemente conexo de Tarjan
            for cycle in topo.get("scc_cycles", []):
                nodes = cycle.get("cycle", [])
                in_a = any(norm_a in n or n in norm_a for n in nodes)
                in_b = any(norm_b in n or n in norm_b for n in nodes)
                if in_a and in_b:
                    return True

            # 2. Comprobar aristas directas en la adyacencia
            adj = topo.get("adjacency", {})
            for src, targets in adj.items():
                if norm_a in src:
                    if any(norm_b in tgt for tgt in targets):
                        return True
                if norm_b in src:
                    if any(norm_a in tgt for tgt in targets):
                        return True

        return False

    def _detect_layer(self, file_path: str) -> Optional[str]:
        """Identifica la capa arquitectonica aproximada de un archivo."""
        parts = file_path.lower().split("/")
        for layer_name, keywords in HEXAGONAL_LAYERS.items():
            if any(k in parts for k in keywords):
                return layer_name
        return None


# Instancia singleton del servicio Anti-Drift
anti_drift_service = AntiDriftService()

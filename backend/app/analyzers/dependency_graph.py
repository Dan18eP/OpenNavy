from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple
from app.schemas.state import FileNode


SUPPORTED_EXTENSIONS = (".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java")


class DependencyGraphAnalyzer:
    """
    Construye el grafo dirigido de dependencias del repositorio y detecta
    ciclos fuertemente conexos mediante el algoritmo de Tarjan (HU-ANALYSIS-03)
    y violaciones de capas.
    """

    def _get_canonical_module_name(self, file_path: str, repo_root: Path) -> str:
        """Determina el nombre canónico normalizado del módulo sin extensión."""
        try:
            rel_path = Path(file_path).relative_to(repo_root)
        except ValueError:
            rel_path = Path(file_path)

        clean_rel = str(rel_path).replace("\\", "/")
        for ext in SUPPORTED_EXTENSIONS:
            if clean_rel.endswith(ext):
                clean_rel = clean_rel[:-len(ext)]
                break
        return clean_rel

    def _build_module_keys_map(
        self,
        file_nodes: List[FileNode],
        repo_root: Path,
    ) -> Tuple[Dict[str, str], Set[str]]:
        """Construye el mapeo de alias y submódulos hacia nombres canónicos."""
        module_keys: Dict[str, str] = {}
        canonical_modules: Set[str] = set()

        for node in file_nodes:
            if not node or not getattr(node, "path", None):
                continue
            canonical = self._get_canonical_module_name(node.path, repo_root)
            canonical_modules.add(canonical)

            dot_canonical = canonical.replace("/", ".")
            module_keys[canonical] = canonical
            module_keys[dot_canonical] = canonical

            parts = dot_canonical.split(".")
            for i in range(len(parts)):
                sub_import = ".".join(parts[i:])
                if sub_import:
                    module_keys[sub_import] = canonical
                sub_slash = "/".join(parts[i:])
                if sub_slash:
                    module_keys[sub_slash] = canonical

        return module_keys, canonical_modules

    def _resolve_import_target(self, imp: str, module_keys: Dict[str, str]) -> Optional[str]:
        """Resuelve el nombre canónico correspondiente a una sentencia de import."""
        imp_clean = imp.replace("\\", "/").strip()
        if imp_clean in module_keys:
            return module_keys[imp_clean]

        imp_dots = imp_clean.replace("/", ".")
        for key, canonical in module_keys.items():
            if imp_dots == key or imp_dots.endswith(f".{key}") or key.endswith(f".{imp_dots}"):
                return canonical
        return None

    def _find_import_line(self, raw_content: Optional[str], imp: str) -> int:
        """Busca el número de línea exacto (1-based) de la declaración import."""
        if not raw_content:
            return 1
        lines = raw_content.splitlines()
        clean_imp = imp.replace("\\", "/").strip()
        last_part = clean_imp.split("/")[-1].split(".")[-1]

        for idx, line in enumerate(lines, 1):
            if ("import" in line or "require" in line or "using" in line) and (clean_imp in line or last_part in line):
                return idx
        return 1

    def _build_adjacency_list_and_edges(
        self,
        file_nodes: List[FileNode],
        repo_root: Path,
        module_keys: Dict[str, str],
        canonical_modules: Set[str],
    ) -> Tuple[Dict[str, List[str]], Dict[Tuple[str, str], Dict[str, Any]]]:
        """
        Construye la lista de adyacencias del grafo de dependencias
        y un mapa de metadatos de aristas (línea exacta y texto de importación).
        """
        adjacency_list: Dict[str, List[str]] = {mod: [] for mod in canonical_modules}
        edge_details: Dict[Tuple[str, str], Dict[str, Any]] = {}

        for node in file_nodes:
            if not node or not getattr(node, "path", None):
                continue
            src_canonical = self._get_canonical_module_name(node.path, repo_root)
            for imp in node.imports:
                target_canonical = self._resolve_import_target(imp, module_keys)
                if target_canonical and target_canonical != src_canonical:
                    if target_canonical not in adjacency_list.setdefault(src_canonical, []):
                        adjacency_list[src_canonical].append(target_canonical)
                    line_no = self._find_import_line(node.raw_content, imp)
                    edge_details[(src_canonical, target_canonical)] = {
                        "source_file": node.path,
                        "line": line_no,
                        "import_statement": imp,
                    }

        return adjacency_list, edge_details

    def tarjan_scc(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """
        Algoritmo de Tarjan para encontrar componentes fuertemente conexos (SCC).
        Identifica todos los SCC de tamaño > 1 (ciclos de dependencias).
        Complejidad temporal óptima O(V + E).
        """
        index = 0
        stack: List[str] = []
        indices: Dict[str, int] = {}
        lowlinks: Dict[str, int] = {}
        on_stack: Set[str] = set()
        sccs: List[List[str]] = []

        def strongconnect(v: str):
            nonlocal index
            indices[v] = index
            lowlinks[v] = index
            index += 1
            stack.append(v)
            on_stack.add(v)

            for w in graph.get(v, []):
                if w not in indices:
                    # w no ha sido visitado aún
                    strongconnect(w)
                    lowlinks[v] = min(lowlinks[v], lowlinks[w])
                elif w in on_stack:
                    # w está en el stack y por tanto en el SCC actual
                    lowlinks[v] = min(lowlinks[v], indices[w])

            # Si v es la raíz del SCC
            if lowlinks[v] == indices[v]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    scc.append(w)
                    if w == v:
                        break
                if len(scc) > 1:
                    sccs.append(scc)

        for node in sorted(graph.keys()):
            if node not in indices:
                strongconnect(node)

        return sccs

    def _extract_cycles_from_scc(
        self,
        scc: List[str],
        graph: Dict[str, List[str]],
        edge_details: Dict[Tuple[str, str], Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Reconstruye los ciclos elementales cerrados dentro de un SCC con detalle de líneas."""
        scc_set = set(scc)
        cycles_with_details: List[Dict[str, Any]] = []

        for start_node in scc:
            visited_in_path = [start_node]
            rec_set = {start_node}

            def dfs_scc(curr: str):
                for nxt in graph.get(curr, []):
                    if nxt not in scc_set:
                        continue
                    if nxt == start_node and len(visited_in_path) >= 2:
                        cycle_path = visited_in_path + [start_node]
                        # Construir detalle de aristas del ciclo
                        steps = []
                        for i in range(len(cycle_path) - 1):
                            u, v = cycle_path[i], cycle_path[i + 1]
                            edge_info = edge_details.get((u, v), {"line": 1, "import_statement": v})
                            steps.append({
                                "from_module": u,
                                "to_module": v,
                                "line": edge_info.get("line", 1),
                                "import_statement": edge_info.get("import_statement", v),
                            })

                        # Evitar duplicados por rotación
                        nodes_cycle = set(cycle_path[:-1])
                        exists = any(set(c["cycle"][:-1]) == nodes_cycle for c in cycles_with_details)
                        if not exists:
                            cycles_with_details.append({
                                "cycle": cycle_path,
                                "steps": steps,
                                "length": len(cycle_path) - 1,
                            })
                    elif nxt not in rec_set:
                        rec_set.add(nxt)
                        visited_in_path.append(nxt)
                        dfs_scc(nxt)
                        visited_in_path.pop()
                        rec_set.remove(nxt)

            dfs_scc(start_node)

        return cycles_with_details

    def generate_preliminary_adr(self, cycles_detailed: List[Dict[str, Any]], repo_name: str = "Repository") -> Dict[str, Any]:
        """
        Genera automáticamente un ADR preliminar sugiriendo la inversión de dependencias (DIP)
        para romper cada ciclo de importación detectado (HU-ANALYSIS-03).
        """
        if not cycles_detailed:
            return {}

        descriptions = []
        for idx, item in enumerate(cycles_detailed, 1):
            cycle_str = " -> ".join(item.get("cycle", []))
            descriptions.append(f"### Ciclo #{idx}: `{cycle_str}`")
            for step in item.get("steps", []):
                descriptions.append(f"- Módulo `{step['from_module']}` importa a `{step['to_module']}` en la **línea {step['line']}** (`{step['import_statement']}`)")
            descriptions.append("")

        cycle_list_text = "\n".join(descriptions)

        adr_content = f"""# ADR-0002: Inversión de Dependencias para Eliminación de Ciclos de Importación en {repo_name}

**Estado:** Propuesto (Generacion Automatica de OpenNavy - Algoritmo de Tarjan)  
**Severidad:** Crítica  
**Regla:** Acyclic Dependencies Principle (ADP) & Dependency Inversion Principle (DIP)  

---

## 1. Contexto y Diagnóstico
El análisis topológico determinístico identificó {len(cycles_detailed)} ciclo(s) de dependencias circulares fuertemente conexos:

{cycle_list_text}

Las dependencias cíclicas impiden el testing modular aislado, generan acoplamiento bidireccional nocivo, dificultan la evolución de versiones y causan `ImportError` / excepciones en tiempo de arranque o ejecución.

---

## 2. Decisión Técnica Recomendada
1. **Extracción de Abstracciones / Interfaces:** Mover las estructuras compartidas, interfaces o DTOs a un submódulo neutral de menor nivel (ej. `contracts` o `core/interfaces`).
2. **Aplicar Dependency Inversion (DIP):** Inyectar la dependencia de alto nivel en tiempo de construcción o inicialización en lugar de importar la implementación concreta directamente.
3. **Puntos de Corte Inmediatos:**
   - Para cada paso reportado con número de línea, reemplazar la llamada a import directo por una referencia a la abstracción común.

---

## 3. Consecuencias
- **Positivas:** Estricto cumplimiento del principio acíclico (ADP), desacoplamiento total en pruebas unitarias e inmunidad a fallos circulares de runtime.
- **Negativas / Riesgos:** Requiere refactorización localizada en las líneas señaladas.
"""

        return {
            "title": f"ADR-0002: Inversión de Dependencias para Eliminación de Ciclos en {repo_name}",
            "filename": "adrs/ADR-0002-dependency-inversion-cycles.md",
            "content": adr_content,
        }

    def build_graph(self, file_nodes: List[FileNode], repo_root: str | Path) -> Dict[str, Any]:
        """
        Construye el grafo dirigido de dependencias entre los módulos del repositorio.
        Utiliza el algoritmo de Tarjan para detectar componentes fuertemente conexos (SCCs).
        Retorna:
            - graph: Adyacencias { "modulo_a": ["modulo_b", "modulo_c"] }
            - circular_dependencies: Lista de ciclos detectados [ ["a", "b", "a"] ]
            - circular_dependencies_details: Detalles con línea exacta de importación
            - sccs: Strongly Connected Components identificados por Tarjan
            - preliminary_adr: Propuesta técnica automática de inversión de dependencias
            - layer_violations: Lista de violaciones de capas detectadas
            - coupling_metrics: Fan-in, Fan-out e inestabilidad por módulo
        """
        root = Path(repo_root)
        file_nodes = [n for n in file_nodes if n and getattr(n, "path", None)]
        module_keys, canonical_modules = self._build_module_keys_map(file_nodes, root)
        adjacency_list, edge_details = self._build_adjacency_list_and_edges(file_nodes, root, module_keys, canonical_modules)

        # Algoritmo de Tarjan para SCCs
        sccs = self.tarjan_scc(adjacency_list)

        # Reconstruir ciclos elementales y pasos con líneas
        circular_dependencies: List[List[str]] = []
        circular_dependencies_details: List[Dict[str, Any]] = []

        for scc in sccs:
            extracted = self._extract_cycles_from_scc(scc, adjacency_list, edge_details)
            for c in extracted:
                circular_dependencies.append(c["cycle"])
                circular_dependencies_details.append(c)

        # Si Tarjan detectó SCC pero la búsqueda elemental no cerró ciclo por algún caso de borde
        if sccs and not circular_dependencies:
            for scc in sccs:
                fallback_cycle = scc + [scc[0]]
                circular_dependencies.append(fallback_cycle)
                circular_dependencies_details.append({
                    "cycle": fallback_cycle,
                    "steps": [{"from_module": scc[i], "to_module": scc[(i + 1) % len(scc)], "line": 1} for i in range(len(scc))],
                    "length": len(scc),
                })

        layer_violations = self._check_layering_rules(adjacency_list)
        coupling_metrics = self._calculate_coupling(adjacency_list)

        # Generar ADR preliminar si hay ciclos
        repo_name = root.name if root.name else "OpenNavy"
        preliminary_adr = self.generate_preliminary_adr(circular_dependencies_details, repo_name)

        return {
            "graph": adjacency_list,
            "total_modules": len(adjacency_list),
            "sccs": sccs,
            "circular_dependencies": circular_dependencies,
            "circular_dependencies_details": circular_dependencies_details,
            "has_cycles": len(circular_dependencies) > 0,
            "preliminary_adr": preliminary_adr,
            "layer_violations": layer_violations,
            "coupling_metrics": coupling_metrics,
        }

    def _check_layering_rules(self, graph: Dict[str, List[str]]) -> List[Dict[str, str]]:
        """
        Valida que módulos internos no importen capas externas prohibidas.
        Regla:
          - domain / models / entities NO debe importar api / controllers / views / endpoints.
        """
        violations = []
        forbidden_rules = [
            {"from_layer": "models", "to_layer": "api", "severity": "high"},
            {"from_layer": "domain", "to_layer": "api", "severity": "high"},
            {"from_layer": "domain", "to_layer": "controllers", "severity": "high"},
            {"from_layer": "models", "to_layer": "endpoints", "severity": "high"},
        ]

        for src, targets in graph.items():
            for target in targets:
                for rule in forbidden_rules:
                    if rule["from_layer"] in src.lower() and rule["to_layer"] in target.lower():
                        violations.append({
                            "source_module": src,
                            "target_module": target,
                            "rule": f"Módulo de datos/dominio ({src}) no debe importar capa superior ({target})",
                            "severity": rule["severity"],
                        })

        return violations

    def _calculate_coupling(self, graph: Dict[str, List[str]]) -> Dict[str, Dict[str, Any]]:
        """Calcula Fan-in (Acoplamiento Aferente - Ca) y Fan-out (Acoplamiento Eferente - Ce)."""
        metrics: Dict[str, Dict[str, Any]] = {}
        all_nodes = set(graph.keys())
        for targets in graph.values():
            all_nodes.update(targets)

        for node in all_nodes:
            fan_out = len(graph.get(node, []))
            fan_in = sum(1 for src, targets in graph.items() if node in targets)
            total = fan_in + fan_out
            instability = round(fan_out / total, 2) if total > 0 else 0.0

            metrics[node] = {
                "fan_in": fan_in,
                "fan_out": fan_out,
                "instability": instability,
            }

        return metrics

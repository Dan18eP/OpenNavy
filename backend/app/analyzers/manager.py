import os
from pathlib import Path
from typing import Dict, List, Any, Optional

from app.analyzers.language_detector import LanguageDetector, EXTENSION_TO_LANGUAGE
from app.analyzers.ast_parser import UniversalASTParser
from app.analyzers.duplication_detector import DuplicationDetector
from app.analyzers.dependency_graph import DependencyGraphAnalyzer
from app.analyzers.dependency_version_analyzer import DependencyVersionAnalyzer
from app.analyzers.architecture_detector import ArchitecturePatternDetector
from app.analyzers.secret_masker import SecretMasker
from app.schemas.state import FileNode, FunctionMetadata


class AnalyzerManager:
    """Coordinador general de análisis estático y sintáctico multi-lenguaje."""

    def __init__(self):
        self.language_detector = LanguageDetector()
        self.ast_parser = UniversalASTParser()
        self.duplication_detector = DuplicationDetector()
        self.dependency_analyzer = DependencyGraphAnalyzer()
        self.dependency_version_analyzer = DependencyVersionAnalyzer()
        self.architecture_detector = ArchitecturePatternDetector()
        self.secret_masker = SecretMasker()

    def analyze_repository(self, repo_path: str | Path) -> Dict[str, Any]:
        """
        Ejecuta el pipeline completo de análisis estático sobre un directorio de código.
        Retorna un diccionario completo con:
            - languages: Lista de lenguajes detectados y estadísticas
            - file_nodes: Lista de FileNode con funciones, clases y métricas
            - summary_metrics: Métricas consolidadas (CC media, MI medio, etc.)
            - duplication: Resultados de detección de clones
            - architecture: Grafo de dependencias, ciclos y violaciones
            - complex_functions: Funciones con CC > 10
        """
        base_path = Path(repo_path)
        if not base_path.exists() or not base_path.is_dir():
            raise ValueError(f"Directorio inválido: {repo_path}")

        # 1. Detección de Lenguajes
        languages, lang_stats = self.language_detector.detect_languages(base_path)

        # 2. Parseo de Archivos AST
        file_nodes: List[FileNode] = []
        complex_functions: List[Dict[str, Any]] = []
        detected_secrets: List[Dict[str, Any]] = []
        total_loc = 0
        total_cc = 0
        total_mi = 0.0

        for root, dirs, files in os.walk(base_path):
            dirs[:] = [d for d in dirs if not self.language_detector.is_ignored(Path(root) / d)]

            for file_name in files:
                file_path = Path(root) / file_name
                if self.language_detector.is_ignored(file_path):
                    continue

                ext = file_path.suffix.lower()
                lang = EXTENSION_TO_LANGUAGE.get(ext)

                # Analizar solo archivos de código soportados (ignorar JSON/YAML/Markdown de cálculo AST pesado)
                if lang and lang not in ("json", "yaml", "markdown", "html", "css"):
                    try:
                        node = self.ast_parser.parse_file(file_path, lang)
                        # Enmascarar secretos de raw_content antes de que fluya al estado o prompts
                        if node.raw_content:
                            masked_content, file_secrets = self.secret_masker.mask_secrets(node.raw_content)
                            node.raw_content = masked_content
                            for sec in file_secrets:
                                try:
                                    rel_path = str(file_path.relative_to(base_path)).replace("\\", "/")
                                except ValueError:
                                    rel_path = str(file_path)
                                detected_secrets.append({
                                    "file": rel_path,
                                    "type": sec.get("type", "Secret"),
                                    "sample": sec.get("sample", "****"),
                                })
                        file_nodes.append(node)

                        total_loc += node.lines_of_code
                        total_cc += node.cyclomatic_complexity_total
                        total_mi += node.maintainability_index

                        # Filtrar funciones complejas para el reporte
                        for fn in node.functions:
                            if fn.cyclomatic_complexity > 10:
                                try:
                                    rel_file = str(Path(node.path).relative_to(base_path)).replace("\\", "/")
                                except ValueError:
                                    rel_file = node.path

                                complex_functions.append({
                                    "file": rel_file,
                                    "function": fn.name,
                                    "line": fn.start_line,
                                    "lines_of_code": fn.lines_of_code,
                                    "cyclomatic_complexity": fn.cyclomatic_complexity,
                                    "nesting_depth": fn.nesting_depth,
                                    "severity": "critical" if fn.cyclomatic_complexity > 20 else "warning",
                                })
                    except Exception:
                        pass

        files_count = len(file_nodes)
        avg_cc = round(total_cc / max(1, files_count), 2)
        avg_mi = round(total_mi / max(1, files_count), 2)

        # 3. Detección de Duplicación
        duplication_result = self.duplication_detector.analyze_duplication(file_nodes)

        # 4. Grafo de Dependencias y Ciclos
        architecture_result = self.dependency_analyzer.build_graph(file_nodes, base_path)

        # 5. Inferencia de Patrón Arquitectónico y Validación de Regla de Dependencia (HU-ANALYSIS-02)
        arch_profile = self.architecture_detector.analyze_architecture(
            file_nodes,
            architecture_result.get("graph", {}),
            base_path
        )
        # Combinar violaciones de capas de architecture_detector con las de dependency_analyzer
        if arch_profile.get("dependency_rule_violations"):
            for viol in arch_profile["dependency_rule_violations"]:
                architecture_result["layer_violations"].append({
                    "source_module": viol["source_module"],
                    "target_module": viol["target_module"],
                    "rule": viol["rule"],
                    "severity": viol["severity"],
                })

        # 6. Control de Versiones de Dependencias y Compatibilidad
        dependencies_result = self.dependency_version_analyzer.analyze_dependencies(base_path)

        # 7. Cálculo Preliminar de Score Estático (0 a 100)
        # Basado en MI (30%), CC (25%), Duplicación (15%), Arquitectura/Compliance (15%) y Salud de Dependencias (15%)
        score_mi = avg_mi
        score_cc = max(0.0, 100.0 - (max(0.0, avg_cc - 5.0) * 10.0))
        score_dup = max(0.0, 100.0 - (duplication_result["duplication_percentage"] * 10.0))
        score_arch = arch_profile.get("dependency_rule_compliance", 100.0)
        score_deps = dependencies_result.get("score", 100.0)

        preliminary_static_score = round(
            (0.30 * score_mi) + (0.25 * score_cc) + (0.15 * score_dup) + (0.15 * score_arch) + (0.15 * score_deps),
            1
        )

        return {
            "languages": languages,
            "language_stats": lang_stats,
            "file_nodes": file_nodes,
            "total_files": files_count,
            "total_lines": total_loc,
            "summary_metrics": {
                "average_cyclomatic_complexity": avg_cc,
                "average_maintainability_index": avg_mi,
                "total_cyclomatic_complexity": total_cc,
                "duplication_percentage": duplication_result["duplication_percentage"],
                "total_duplicated_lines": duplication_result["total_duplicated_lines"],
                "has_circular_dependencies": architecture_result["has_cycles"],
                "circular_dependencies_count": len(architecture_result["circular_dependencies"]),
                "layer_violations_count": len(architecture_result["layer_violations"]),
                "dominant_architecture_pattern": arch_profile.get("dominant_pattern", "Layered / 3-Tier"),
                "pattern_confidence": arch_profile.get("pattern_confidence", 0.5),
                "dependency_rule_compliance": arch_profile.get("dependency_rule_compliance", 100.0),
                "complex_functions_count": len(complex_functions),
                "dependency_score": dependencies_result.get("score", 100.0),
                "total_dependencies": dependencies_result.get("total_dependencies", 0),
                "outdated_dependencies_count": dependencies_result.get("outdated_count", 0),
                "incompatible_dependencies_count": dependencies_result.get("incompatible_count", 0),
                "preliminary_static_score": min(100.0, max(0.0, preliminary_static_score)),
            },
            "duplication": duplication_result,
            "architecture": architecture_result,
            "architecture_profile": arch_profile,
            "dependencies": dependencies_result,
            "detected_secrets": detected_secrets,
            "complex_functions": sorted(
                complex_functions,
                key=lambda f: f["cyclomatic_complexity"],
                reverse=True
            ),
        }


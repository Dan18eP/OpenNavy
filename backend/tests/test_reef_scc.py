import pytest
from pathlib import Path

from app.analyzers.ast_parser import UniversalASTParser
from app.analyzers.dependency_graph import DependencyGraphAnalyzer


def test_reef_synthetic_circular_dependencies():
    root = Path(__file__).resolve().parents[2]
    sample_dir = root / "fixtures" / "reef_sample"

    files = [
        sample_dir / "module_a.py",
        sample_dir / "module_b.py",
        sample_dir / "module_c.py",
    ]

    ast_parser = UniversalASTParser()
    nodes = [ast_parser.parse_file(f, "python") for f in files]

    dep_analyzer = DependencyGraphAnalyzer()
    graph_res = dep_analyzer.build_graph(nodes, repo_root=root)

    assert graph_res["has_cycles"] is True
    assert len(graph_res["circular_dependencies"]) >= 1

    detected_cycle = graph_res["circular_dependencies"][0]
    # Verify all 3 modules are in the detected cycle
    modules_in_cycle = [m.replace("\\", "/") for m in detected_cycle]
    assert any("module_a" in m for m in modules_in_cycle)
    assert any("module_b" in m for m in modules_in_cycle)
    assert any("module_c" in m for m in modules_in_cycle)

    # Verify ADR generation
    assert "preliminary_adr" in graph_res
    assert graph_res["preliminary_adr"] != {}

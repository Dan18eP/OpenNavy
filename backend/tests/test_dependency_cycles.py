import pytest
from pathlib import Path
from app.analyzers.dependency_graph import DependencyGraphAnalyzer
from app.schemas.state import FileNode


def test_tarjan_acyclic_graph():
    """Grafo dirigido acíclico no produce SCCs con tamaño > 1."""
    analyzer = DependencyGraphAnalyzer()
    graph = {
        "a": ["b", "c"],
        "b": ["c"],
        "c": ["d"],
        "d": [],
    }
    sccs = analyzer.tarjan_scc(graph)
    assert len(sccs) == 0


def test_tarjan_direct_cycle():
    """Detecta ciclo directo A -> B -> A."""
    analyzer = DependencyGraphAnalyzer()
    graph = {
        "mod_a": ["mod_b"],
        "mod_b": ["mod_a"],
    }
    sccs = analyzer.tarjan_scc(graph)
    assert len(sccs) == 1
    assert set(sccs[0]) == {"mod_a", "mod_b"}


def test_tarjan_transitive_cycle():
    """Detecta ciclo transitivo A -> B -> C -> A."""
    analyzer = DependencyGraphAnalyzer()
    graph = {
        "service_a": ["service_b"],
        "service_b": ["service_c"],
        "service_c": ["service_a"],
        "leaf": [],
    }
    sccs = analyzer.tarjan_scc(graph)
    assert len(sccs) == 1
    assert set(sccs[0]) == {"service_a", "service_b", "service_c"}


def test_dependency_graph_full_cycle_with_lines_and_adr():
    """Construcción del grafo de dependencias con nodos de archivo, líneas y ADR preliminar."""
    code_a = """
import app.services.service_b
from app.utils.helper import helper_fn

def do_a():
    pass
"""
    code_b = """
import app.services.service_c

def do_b():
    pass
"""
    code_c = """
import app.services.service_a

def do_c():
    pass
"""

    node_a = FileNode(
        path="app/services/service_a.py",
        language="python",
        lines_of_code=10,
        imports=["app.services.service_b", "app.utils.helper"],
        raw_content=code_a,
    )
    node_b = FileNode(
        path="app/services/service_b.py",
        language="python",
        lines_of_code=8,
        imports=["app.services.service_c"],
        raw_content=code_b,
    )
    node_c = FileNode(
        path="app/services/service_c.py",
        language="python",
        lines_of_code=8,
        imports=["app.services.service_a"],
        raw_content=code_c,
    )

    analyzer = DependencyGraphAnalyzer()
    result = analyzer.build_graph([node_a, node_b, node_c], repo_root="app")

    assert result["has_cycles"] is True
    assert len(result["circular_dependencies"]) >= 1

    # Verificar que las líneas de importación están mapeadas
    details = result["circular_dependencies_details"]
    assert len(details) >= 1
    first_cycle = details[0]
    assert len(first_cycle["steps"]) == 3
    # Cada paso debe tener la línea reportada
    for step in first_cycle["steps"]:
        assert step["line"] >= 1
        assert "from_module" in step
        assert "to_module" in step

    # Verificar generación automática de ADR preliminar
    adr = result["preliminary_adr"]
    assert adr is not None
    assert "ADR-0002" in adr["title"]
    assert "Inversión de Dependencias" in adr["title"]
    assert "Algoritmo de Tarjan" in adr["content"]
    assert "service_a" in adr["content"]
    assert "service_b" in adr["content"]
    assert "service_c" in adr["content"]

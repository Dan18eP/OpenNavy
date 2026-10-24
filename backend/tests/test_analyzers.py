import tempfile
from pathlib import Path
import pytest

from app.analyzers.language_detector import LanguageDetector
from app.analyzers.ast_parser import UniversalASTParser, calculate_maintainability_index
from app.analyzers.duplication_detector import DuplicationDetector
from app.analyzers.dependency_graph import DependencyGraphAnalyzer
from app.analyzers.manager import AnalyzerManager
from app.schemas.state import FileNode


def test_language_detector_ignores_hidden():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        # Crear archivos normales
        (tmp_path / "main.py").write_text("print('hello')", encoding="utf-8")
        (tmp_path / "app.ts").write_text("console.log('hi');", encoding="utf-8")

        # Crear carpeta ignorada
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config.py").write_text("secret", encoding="utf-8")

        venv_dir = tmp_path / ".venv"
        venv_dir.mkdir()
        (venv_dir / "lib.py").write_text("pass", encoding="utf-8")

        detector = LanguageDetector()
        languages, stats = detector.detect_languages(tmp_path)

        assert "python" in languages
        assert "typescript" in languages
        assert stats["python"]["files"] == 1
        assert stats["typescript"]["files"] == 1


def test_ast_parser_python_metrics():
    sample_code = '''"""Módulo de prueba."""

class Calculator:
    """Clase calculadora."""
    def add(self, a: int, b: int) -> int:
        """Suma dos números."""
        return a + b

def complex_decision(x: int, y: int, flag: bool) -> int:
    result = 0
    if x > 10 and y < 5:
        for i in range(x):
            if i % 2 == 0:
                result += i
    elif x <= 0 or not flag:
        while y > 0:
            y -= 1
            result += 1
    else:
        try:
            result = x // y
        except ZeroDivisionError:
            result = -1
    return result
'''
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(sample_code)
        f_path = f.name

    try:
        parser = UniversalASTParser()
        node = parser.parse_file(f_path, "python")

        assert node.language == "python"
        assert len(node.classes) == 1
        assert node.classes[0].name == "Calculator"
        assert node.classes[0].docstring == "Clase calculadora."

        # Funciones
        func_names = [fn.name for fn in node.functions]
        assert "add" in func_names
        assert "complex_decision" in func_names

        add_fn = next(fn for fn in node.functions if fn.name == "add")
        assert add_fn.cyclomatic_complexity == 1
        assert add_fn.parameters_count == 3  # self, a, b

        complex_fn = next(fn for fn in node.functions if fn.name == "complex_decision")
        # Base 1 + If(1) + BoolOp 'and'(1) + For(1) + If(1) + Elif/If(1) + BoolOp 'or'(1) + While(1) + Except(1) = 9
        assert complex_fn.cyclomatic_complexity >= 7
        assert complex_fn.nesting_depth >= 3

        assert 0.0 <= node.maintainability_index <= 100.0
    finally:
        Path(f_path).unlink(missing_ok=True)


def test_duplication_detector():
    duplicate_code = """
def process_data(items):
    cleaned = []
    for item in items:
        if item is not None:
            formatted = str(item).strip().lower()
            cleaned.append(formatted)
    return cleaned
"""
    node_a = FileNode(
        path="src/service_a.py",
        language="python",
        lines_of_code=15,
        raw_content=duplicate_code,
    )
    node_b = FileNode(
        path="src/service_b.py",
        language="python",
        lines_of_code=15,
        raw_content=duplicate_code,
    )

    detector = DuplicationDetector(min_block_lines=5)
    result = detector.analyze_duplication([node_a, node_b])

    assert result["duplication_percentage"] > 0
    assert result["clones_count"] >= 1
    assert result["clones"][0]["file_a"] == "src/service_a.py"
    assert result["clones"][0]["file_b"] == "src/service_b.py"


def test_dependency_graph_cycle_detection():
    # Simular 3 archivos con ciclo circular: mod_a -> mod_b -> mod_c -> mod_a
    node_a = FileNode(
        path="app/orders/service.py",
        language="python",
        lines_of_code=10,
        imports=["app.billing.invoice"],
    )
    node_b = FileNode(
        path="app/billing/invoice.py",
        language="python",
        lines_of_code=10,
        imports=["app.shipping.delivery"],
    )
    node_c = FileNode(
        path="app/shipping/delivery.py",
        language="python",
        lines_of_code=10,
        imports=["app.orders.service"],
    )

    analyzer = DependencyGraphAnalyzer()
    result = analyzer.build_graph([node_a, node_b, node_c], repo_root="app")

    assert result["has_cycles"] is True
    assert len(result["circular_dependencies"]) >= 1


def test_analyzer_manager_self_analysis():
    # Ejecutar el manager sobre el código propio del backend
    backend_dir = Path(__file__).resolve().parent.parent / "app"
    manager = AnalyzerManager()
    analysis = manager.analyze_repository(backend_dir)

    assert analysis["total_files"] >= 5
    assert "python" in analysis["languages"]
    assert "summary_metrics" in analysis
    assert analysis["summary_metrics"]["average_maintainability_index"] > 0
    assert analysis["summary_metrics"]["preliminary_static_score"] > 0

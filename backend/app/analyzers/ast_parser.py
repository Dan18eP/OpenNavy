import ast
import math
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from app.schemas.state import FileNode, FunctionMetadata, ClassMetadata


GENERIC_IMPORT_PATTERNS = [
    r'import\s+.*?from\s+[\'"](.*?)[\'"]',  # JS/TS ES6
    r'require\s*\(\s*[\'"](.*?)[\'"]\s*\)',  # JS CommonJS
    r'import\s+([a-zA-Z0-9_\.]+);?',       # Java
    r'import\s+[\'"](.*?)[\'"]',            # Go
    r'using\s+([a-zA-Z0-9_\.]+);',          # C#
    r'#include\s+[<"](.*?)[\>"]',          # C/C++
]

GENERIC_FUNC_PATTERNS = [
    r'(?:function\s+([a-zA-Z0-9_]+)|(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)',  # JS/TS
    r'(?:public|private|protected|static|\s)+[a-zA-Z0-9_<>[\]]+\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*(?:\{|throws)',  # Java/C#
    r'func\s+(?:\([^)]+\)\s+)?([a-zA-Z0-9_]+)\s*\(',  # Go
    r'fn\s+([a-zA-Z0-9_]+)\s*\(',                      # Rust
    r'def\s+([a-zA-Z0-9_]+)',                          # Ruby/Python
]

DECISION_KEYWORDS = [
    r'\bif\b',
    r'\belse\s+if\b',
    r'\belif\b',
    r'\bfor\b',
    r'\bwhile\b',
    r'\bcase\b',
    r'\bcatch\b',
    r'\bexcept\b',
    r'&&',
    r'\|\|',
    r'\band\b',
    r'\bor\b',
    r'\s+\?\s+',
]


class CyclomaticComplexityVisitor(ast.NodeVisitor):
    """Calcula la Complejidad Ciclomática (McCabe) de una función o bloque AST en Python."""

    def __init__(self):
        self.complexity = 1

    def visit_If(self, node: ast.If):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        self.complexity += 1
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp):
        self.complexity += 1
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension):
        self.complexity += len(node.ifs)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match):
        self.complexity += max(0, len(node.cases) - 1)
        self.generic_visit(node)


def calculate_nesting_depth(node: ast.AST, current_depth: int = 0) -> int:
    """Calcula la profundidad máxima de anidamiento dentro de un nodo AST."""
    max_depth = current_depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With, ast.AsyncWith, ast.Match)):
            depth = calculate_nesting_depth(child, current_depth + 1)
            max_depth = max(max_depth, depth)
        else:
            depth = calculate_nesting_depth(child, current_depth)
            max_depth = max(max_depth, depth)
    return max_depth


def calculate_maintainability_index(sloc: int, cyclomatic_complexity: int, comment_ratio: float = 0.1) -> float:
    """
    Calcula el Índice de Mantenibilidad (MI) normalizado (0 a 100).
    Fórmula estándar del Software Engineering Institute (SEI) / Radon.
    """
    if sloc <= 0:
        return 100.0

    halstead_volume = max(1.0, sloc * math.log2(max(2.0, sloc)))

    try:
        raw_mi = (
            171.0
            - 5.2 * math.log(halstead_volume)
            - 0.23 * cyclomatic_complexity
            - 16.2 * math.log(max(1.0, float(sloc)))
            + 50.0 * math.sin(math.sqrt(2.4 * comment_ratio))
        )
        normalized_mi = (raw_mi / 171.0) * 100.0
        return round(max(0.0, min(100.0, normalized_mi)), 2)
    except Exception:
        fallback = 100.0 - (0.4 * cyclomatic_complexity + 0.3 * (sloc / 2.0))
        return round(max(0.0, min(100.0, fallback)), 2)


from app.analyzers.treesitter_engine import TreeSitterEngine


class UniversalASTParser:
    """Parser multi-lenguaje de AST y métricas estáticas."""

    def __init__(self):
        self._treesitter_engine = TreeSitterEngine()

    def parse_file(self, file_path: str | Path, language: str) -> FileNode:
        """Parsea un archivo individual y retorna un FileNode con todas sus métricas."""
        path_obj = Path(file_path)
        raw_content = ""
        try:
            with open(path_obj, "r", encoding="utf-8", errors="ignore") as f:
                raw_content = f.read()
        except Exception:
            pass

        loc = len(raw_content.splitlines())
        if language == "python":
            return self._parse_python(str(path_obj), raw_content, loc)

        # Si el lenguaje es soportado por Tree-sitter (TS, JS, Java, Go, etc.), usar TreeSitterEngine
        if self._treesitter_engine.is_language_supported(language):
            parsed = self._treesitter_engine.parse_source(str(path_obj), raw_content, language)
            if parsed:
                return parsed

        return self._parse_generic_source(str(path_obj), raw_content, language, loc)

    # ── Módulos de Parseo Python ────────────────────────────────────────

    def _extract_python_imports(self, tree: ast.AST) -> List[str]:
        """Extrae la lista de dependencias e imports desde el AST de Python."""
        imports: List[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    full_name = f"{module}.{alias.name}" if module else alias.name
                    imports.append(full_name)
        return list(set(imports))

    def _extract_python_classes(self, tree: ast.AST) -> List[ClassMetadata]:
        """Extrae metadatos de las clases definidas en el AST de Python."""
        classes: List[ClassMetadata] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                end_line = getattr(node, "end_lineno", node.lineno)
                methods_count = sum(1 for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)))
                classes.append(ClassMetadata(
                    name=node.name,
                    start_line=node.lineno,
                    end_line=end_line,
                    methods_count=methods_count,
                    docstring=ast.get_docstring(node),
                ))
        return classes

    def _extract_python_function_entry(self, node: ast.AST) -> Tuple[FunctionMetadata, int]:
        """Extrae métricas estáticas de una única función de Python."""
        end_line = getattr(node, "end_lineno", node.lineno)
        func_loc = max(1, end_line - node.lineno + 1)

        args = node.args
        param_count = len(args.args) + (1 if args.vararg else 0) + (1 if args.kwarg else 0) + len(args.kwonlyargs)

        visitor = CyclomaticComplexityVisitor()
        visitor.visit(node)
        func_cc = visitor.complexity
        nesting = calculate_nesting_depth(node)

        meta = FunctionMetadata(
            name=node.name,
            start_line=node.lineno,
            end_line=end_line,
            lines_of_code=func_loc,
            parameters_count=param_count,
            cyclomatic_complexity=func_cc,
            nesting_depth=nesting,
            docstring=ast.get_docstring(node),
        )
        return meta, func_cc

    def _extract_python_functions(self, tree: ast.AST) -> Tuple[List[FunctionMetadata], int]:
        """Extrae metadatos y complejidad total de todas las funciones del AST de Python."""
        functions: List[FunctionMetadata] = []
        total_cc = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn_meta, cc = self._extract_python_function_entry(node)
                functions.append(fn_meta)
                total_cc += cc
        return functions, total_cc

    def _parse_python(self, file_path: str, content: str, loc: int) -> FileNode:
        """Parseo profundo de código Python usando el módulo nativo AST."""
        try:
            tree = ast.parse(content, filename=file_path)
        except SyntaxError:
            return self._parse_generic_source(file_path, content, "python", loc)

        imports = self._extract_python_imports(tree)
        classes = self._extract_python_classes(tree)
        functions, total_cc = self._extract_python_functions(tree)

        comment_lines = sum(1 for line in content.splitlines() if line.strip().startswith("#"))
        comment_ratio = comment_lines / max(1, loc)
        file_cc = total_cc if total_cc > 0 else 1
        mi = calculate_maintainability_index(loc, file_cc, comment_ratio)

        return FileNode(
            path=file_path,
            language="python",
            lines_of_code=loc,
            functions=functions,
            classes=classes,
            imports=imports,
            cyclomatic_complexity_total=file_cc,
            maintainability_index=mi,
            raw_content=content,
        )

    # ── Módulos de Parseo Genérico ──────────────────────────────────────

    def _extract_generic_imports(self, content: str) -> List[str]:
        """Extrae imports mediante patrones de expresiones regulares."""
        imports: List[str] = []
        for pattern in GENERIC_IMPORT_PATTERNS:
            for match in re.finditer(pattern, content):
                imports.append(match.group(1))
        return list(set(imports))

    def _count_generic_decisions(self, content: str) -> int:
        """Cuenta bifurcaciones de control en código genérico."""
        total_decisions = 0
        for pattern in DECISION_KEYWORDS:
            total_decisions += len(re.findall(pattern, content))
        return total_decisions

    def _extract_generic_functions(self, lines: List[str], loc: int) -> List[FunctionMetadata]:
        """Detecta firmas de funciones y calcula su complejidad localized en código genérico."""
        functions: List[FunctionMetadata] = []
        for i, line in enumerate(lines, 1):
            for pattern in GENERIC_FUNC_PATTERNS:
                match = re.search(pattern, line)
                if match:
                    func_name = next(g for g in match.groups() if g)
                    has_params = "(" in line and ")" in line and line.split("(")[1].split(")")[0].strip()
                    param_count = line.count(",") + 1 if has_params else 0
                    
                    # Extraer bloque de líneas representativo de la función
                    end_idx = min(loc, i + 30)
                    fn_body = "\n".join(lines[i-1:end_idx])
                    func_decisions = self._count_generic_decisions(fn_body)
                    func_cc = max(1, 1 + func_decisions)

                    functions.append(FunctionMetadata(
                        name=func_name,
                        start_line=i,
                        end_line=end_idx,
                        lines_of_code=max(1, end_idx - i + 1),
                        parameters_count=param_count,
                        cyclomatic_complexity=func_cc,
                        nesting_depth=1,
                    ))
                    break
        return functions

    def _extract_generic_classes(self, lines: List[str], loc: int, func_count: int) -> List[ClassMetadata]:
        """Detecta clases en código genérico."""
        classes: List[ClassMetadata] = []
        class_pattern = r'\bclass\s+([a-zA-Z0-9_]+)'
        for i, line in enumerate(lines, 1):
            match = re.search(class_pattern, line)
            if match:
                classes.append(ClassMetadata(
                    name=match.group(1),
                    start_line=i,
                    end_line=min(loc, i + 50),
                    methods_count=func_count,
                ))
        return classes

    def _parse_generic_source(self, file_path: str, content: str, language: str, loc: int) -> FileNode:
        """Parseo heurístico para JavaScript, TypeScript, Java, Go, C#, etc."""
        lines = content.splitlines()
        imports = self._extract_generic_imports(content)
        total_decisions = self._count_generic_decisions(content)
        file_cc = max(1, 1 + total_decisions)

        functions = self._extract_generic_functions(lines, loc)
        classes = self._extract_generic_classes(lines, loc, len(functions))

        comment_lines = sum(1 for line in lines if line.strip().startswith(("//", "/*", "*", "#", "<!--")))
        comment_ratio = comment_lines / max(1, loc)
        mi = calculate_maintainability_index(loc, file_cc, comment_ratio)

        return FileNode(
            path=file_path,
            language=language,
            lines_of_code=loc,
            functions=functions,
            classes=classes,
            imports=imports,
            cyclomatic_complexity_total=file_cc,
            maintainability_index=mi,
            raw_content=content,
        )

"""
Motor de parsing sintáctico y métricas AST multilenguaje impulsado por Tree-sitter.

Soporta análisis AST de alta fidelidad para:
- Python
- TypeScript
- JavaScript
- Java
- Go

Elimina por completo las heurísticas de regex para decisiones de control de flujo,
garantizando que comentarios y cadenas de texto no alteren la Complejidad Ciclomática (McCabe).
"""

from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import tree_sitter_language_pack as tslp

from app.schemas.state import ClassMetadata, FileNode, FunctionMetadata
from app.analyzers.ast_parser import calculate_maintainability_index

# Mapeo de identificadores de lenguaje soportados por tree-sitter
LANGUAGE_MAPPING = {
    "typescript": "typescript",
    "javascript": "javascript",
    "java": "java",
    "go": "go",
    "python": "python",
}

# Tipos de nodo de bifurcación de control de flujo para McCabe por lenguaje
DECISION_NODE_TYPES: Dict[str, Set[str]] = {
    "typescript": {
        "if_statement",
        "for_statement",
        "for_in_statement",
        "while_statement",
        "do_statement",
        "catch_clause",
        "switch_case",
        "ternary_expression",
    },
    "javascript": {
        "if_statement",
        "for_statement",
        "for_in_statement",
        "while_statement",
        "do_statement",
        "catch_clause",
        "switch_case",
        "ternary_expression",
    },
    "java": {
        "if_statement",
        "for_statement",
        "enhanced_for_statement",
        "while_statement",
        "do_statement",
        "catch_clause",
        "switch_rule",
        "switch_block_statement_group",
        "ternary_expression",
    },
    "go": {
        "if_statement",
        "for_statement",
        "communication_case",
        "expression_case",
        "type_case",
    },
    "python": {
        "if_statement",
        "for_statement",
        "while_statement",
        "except_clause",
        "match_case",
        "conditional_expression",
    },
}

# Nodos de función/método por lenguaje
FUNCTION_NODE_TYPES: Dict[str, Set[str]] = {
    "typescript": {
        "function_declaration",
        "method_definition",
        "arrow_function",
        "function_expression",
    },
    "javascript": {
        "function_declaration",
        "method_definition",
        "arrow_function",
        "function_expression",
    },
    "java": {
        "method_declaration",
        "constructor_declaration",
    },
    "go": {
        "function_declaration",
        "method_declaration",
    },
    "python": {
        "function_definition",
    },
}

# Nodos de clase/estructura por lenguaje
CLASS_NODE_TYPES: Dict[str, Set[str]] = {
    "typescript": {"class_declaration", "interface_declaration"},
    "javascript": {"class_declaration"},
    "java": {"class_declaration", "interface_declaration", "record_declaration", "enum_declaration"},
    "go": {"type_declaration"},
    "python": {"class_definition"},
}


class TreeSitterEngine:
    """Motor universal de parsing sintáctico basado en Tree-sitter."""

    def __init__(self):
        self._parsers: Dict[str, any] = {}

    def get_parser(self, language: str):
        """Obtiene o inicializa el parser de Tree-sitter para el lenguaje solicitado."""
        normalized_lang = LANGUAGE_MAPPING.get(language.lower())
        if not normalized_lang:
            return None

        if normalized_lang not in self._parsers:
            try:
                self._parsers[normalized_lang] = tslp.get_parser(normalized_lang)
            except Exception:
                return None
        return self._parsers[normalized_lang]

    def is_language_supported(self, language: str) -> bool:
        """Verifica si el lenguaje dispone de gramática Tree-sitter."""
        return language.lower() in LANGUAGE_MAPPING

    def parse_source(self, file_path: str, content: str, language: str) -> Optional[FileNode]:
        """
        Parsea el código fuente usando Tree-sitter y genera un FileNode
        con métricas exactas libres de falsos positivos en comentarios/strings.
        """
        parser = self.get_parser(language)
        if not parser:
            return None

        raw_bytes = content.encode("utf-8", errors="ignore")
        tree = parser.parse(raw_bytes)
        root = tree.root_node

        lines = content.splitlines()
        loc = len(lines)

        imports = self._extract_imports(root, language)
        classes, class_func_count = self._extract_classes(root, language)
        functions = self._extract_functions(root, language)
        
        # Complejidad Ciclomática a nivel de archivo
        file_cc = self.calculate_cyclomatic_complexity(root, language)

        # Cálculo de líneas de comentarios mediante nodos AST reales
        comment_lines = self._count_ast_comment_lines(root)
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

    def calculate_cyclomatic_complexity(self, node, language: str) -> int:
        """
        Calcula la Complejidad Ciclomática (McCabe) navegando los nodos de decisión del AST.
        Base = 1 + bifurcaciones (if, loops, cases, operadores lógicos &&, ||).
        Comentarios y strings no son evaluados jamás como nodos de decisión.
        """
        normalized_lang = LANGUAGE_MAPPING.get(language.lower(), "typescript")
        decision_types = DECISION_NODE_TYPES.get(normalized_lang, set())
        
        decisions = 0

        def traverse(current):
            nonlocal decisions
            # Si el nodo es comentario o string, sus hijos no son evaluados
            if "comment" in current.type or "string" in current.type:
                return

            if current.type in decision_types:
                decisions += 1
            elif current.type in ("binary_expression", "logical_expression"):
                # Operadores lógicos de cortocircuito (&&, ||, and, or)
                operator_node = current.child_by_field_name("operator")
                if operator_node:
                    op_text = operator_node.text.decode("utf-8", errors="ignore").strip()
                    if op_text in ("&&", "||", "and", "or"):
                        decisions += 1
                else:
                    # En algunas gramáticas no está etiquetado con field_name
                    for child in current.children:
                        if child.type in ("&&", "||", "and", "or"):
                            decisions += 1
                            break

            for child in current.children:
                traverse(child)

        traverse(node)
        return max(1, 1 + decisions)

    def _calculate_nesting_depth(self, node, current_depth: int = 0) -> int:
        """Calcula la profundidad máxima de anidamiento de estructuras de control."""
        max_depth = current_depth
        block_types = {
            "if_statement",
            "for_statement",
            "for_in_statement",
            "while_statement",
            "do_statement",
            "switch_statement",
            "try_statement",
            "catch_clause",
        }

        for child in node.children:
            if child.type in block_types:
                depth = self._calculate_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, depth)
            else:
                depth = self._calculate_nesting_depth(child, current_depth)
                max_depth = max(max_depth, depth)

        return max_depth

    def _count_ast_comment_lines(self, root_node) -> int:
        """Cuenta líneas ocupadas por comentarios inspeccionando los nodos reales de comentarios."""
        comment_lines_set = set()

        def find_comments(node):
            if "comment" in node.type:
                start_row = node.start_point[0]
                end_row = node.end_point[0]
                for r in range(start_row, end_row + 1):
                    comment_lines_set.add(r)
            for child in node.children:
                find_comments(child)

        find_comments(root_node)
        return len(comment_lines_set)

    def _extract_imports(self, root_node, language: str) -> List[str]:
        """Extrae las dependencias e imports según la gramática del lenguaje."""
        imports: List[str] = []
        normalized_lang = LANGUAGE_MAPPING.get(language.lower(), "")

        def traverse(node):
            if normalized_lang in ("typescript", "javascript"):
                if node.type == "import_statement":
                    source_node = node.child_by_field_name("source")
                    if source_node:
                        raw = source_node.text.decode("utf-8", errors="ignore").strip("'\"`")
                        imports.append(raw)
                elif node.type == "call_expression":
                    # Detectar require('pkg')
                    fn_node = node.child_by_field_name("function")
                    if fn_node and fn_node.text.decode("utf-8", errors="ignore") == "require":
                        args = node.child_by_field_name("arguments")
                        if args and args.named_children:
                            first_arg = args.named_children[0]
                            imports.append(first_arg.text.decode("utf-8", errors="ignore").strip("'\"`"))
            elif normalized_lang == "java":
                if node.type == "import_declaration":
                    # Buscar el identificador o scoped_identifier
                    for child in node.named_children:
                        if child.type in ("scoped_identifier", "identifier"):
                            imports.append(child.text.decode("utf-8", errors="ignore").strip())
            elif normalized_lang == "go":
                if node.type == "import_spec":
                    path_node = node.child_by_field_name("path") or node
                    clean_path = path_node.text.decode("utf-8", errors="ignore").strip('"')
                    if clean_path:
                        imports.append(clean_path)
            elif normalized_lang == "python":
                if node.type in ("import_statement", "import_from_statement"):
                    for child in node.named_children:
                        if child.type in ("dotted_name", "aliased_import", "identifier"):
                            imports.append(child.text.decode("utf-8", errors="ignore").strip())

            for child in node.children:
                traverse(child)

        traverse(root_node)
        return list(dict.fromkeys([imp for imp in imports if imp]))

    def _extract_classes(self, root_node, language: str) -> Tuple[List[ClassMetadata], int]:
        """Extrae metadatos de clases y estructuras."""
        classes: List[ClassMetadata] = []
        normalized_lang = LANGUAGE_MAPPING.get(language.lower(), "")
        class_types = CLASS_NODE_TYPES.get(normalized_lang, set())

        def find_classes(node):
            if node.type in class_types:
                # Extraer nombre
                name_node = node.child_by_field_name("name")
                name = ""
                if name_node:
                    name = name_node.text.decode("utf-8", errors="ignore").strip()
                elif normalized_lang == "go" and node.type == "type_declaration":
                    for child in node.named_children:
                        if child.type == "type_spec":
                            tnode = child.child_by_field_name("name") or child.named_children[0]
                            name = tnode.text.decode("utf-8", errors="ignore").strip()
                
                if not name:
                    name = "AnonymousClass"

                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1

                # Contar métodos contenidos
                methods_count = 0
                func_types = FUNCTION_NODE_TYPES.get(normalized_lang, set())
                for child in node.named_children:
                    if child.type in ("class_body", "field_declaration_list"):
                        for inner in child.named_children:
                            if inner.type in func_types:
                                methods_count += 1

                classes.append(ClassMetadata(
                    name=name,
                    start_line=start_line,
                    end_line=end_line,
                    methods_count=methods_count,
                ))

            for child in node.children:
                find_classes(child)

        find_classes(root_node)
        return classes, len(classes)

    def _extract_functions(self, root_node, language: str) -> List[FunctionMetadata]:
        """Extrae funciones y calcula sus métricas sintácticas individuales."""
        functions: List[FunctionMetadata] = []
        normalized_lang = LANGUAGE_MAPPING.get(language.lower(), "")
        func_types = FUNCTION_NODE_TYPES.get(normalized_lang, set())

        def find_functions(node):
            if node.type in func_types:
                name_node = node.child_by_field_name("name")
                name = ""
                if name_node:
                    name = name_node.text.decode("utf-8", errors="ignore").strip()
                elif normalized_lang == "go" and node.type == "method_declaration":
                    fn_name_node = node.child_by_field_name("name")
                    name = fn_name_node.text.decode("utf-8", errors="ignore").strip() if fn_name_node else "method"
                elif node.parent and node.parent.type == "variable_declarator":
                    var_name_node = node.parent.child_by_field_name("name")
                    if var_name_node:
                        name = var_name_node.text.decode("utf-8", errors="ignore").strip()
                
                if not name:
                    name = "anonymous"

                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                loc = max(1, end_line - start_line + 1)

                # Parámetros
                param_count = 0
                params_node = node.child_by_field_name("parameters")
                if params_node:
                    param_count = len([c for c in params_node.named_children if "comment" not in c.type])

                # Complejidad ciclomática localizada
                cc = self.calculate_cyclomatic_complexity(node, language)
                nesting = self._calculate_nesting_depth(node)

                functions.append(FunctionMetadata(
                    name=name,
                    start_line=start_line,
                    end_line=end_line,
                    lines_of_code=loc,
                    parameters_count=param_count,
                    cyclomatic_complexity=cc,
                    nesting_depth=nesting,
                ))

            for child in node.children:
                find_functions(child)

        find_functions(root_node)
        return functions

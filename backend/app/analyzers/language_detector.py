import os
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Mapeo de extensiones a nombres normalizados de lenguaje
EXTENSION_TO_LANGUAGE: Dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".h": "c",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "css",
    ".sql": "sql",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
}

# Directorios ignorados por defecto
IGNORED_DIRECTORIES: Set[str] = {
    ".git",
    ".svn",
    ".hg",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".env",
    "dist",
    "build",
    "out",
    ".next",
    ".nuxt",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".agents",
    "coverage",
    ".gemini",
    "target",
    "vendor",
    "bin",
    "obj",
}


class LanguageDetector:
    """Detecta los lenguajes presentes en un directorio y recolecta estadísticas de archivos."""

    def __init__(self, ignored_dirs: Set[str] = None):
        self.ignored_dirs = ignored_dirs or IGNORED_DIRECTORIES

    def is_ignored(self, path: Path) -> bool:
        """Verifica si un archivo o directorio debe ser ignorado."""
        for part in path.parts:
            if part in self.ignored_dirs:
                return True
        return False

    def detect_languages(self, repo_path: str | Path) -> Tuple[List[str], Dict[str, Dict[str, int]]]:
        """
        Escanea el directorio del repositorio.
        Retorna:
            - Lista ordenada de lenguajes detectados (por número de líneas descendente).
            - Diccionario con estadísticas por lenguaje: {'python': {'files': 12, 'lines': 1500}}
        """
        base_path = Path(repo_path)
        if not base_path.exists() or not base_path.is_dir():
            return [], {}

        stats: Dict[str, Dict[str, int]] = {}

        for root, dirs, files in os.walk(base_path):
            # Modificar dirs in-place para que os.walk no entre a carpetas ignoradas
            dirs[:] = [d for d in dirs if d not in self.ignored_dirs]

            for file_name in files:
                file_path = Path(root) / file_name
                if self.is_ignored(file_path):
                    continue

                ext = file_path.suffix.lower()
                lang = EXTENSION_TO_LANGUAGE.get(ext)

                if lang:
                    if lang not in stats:
                        stats[lang] = {"files": 0, "lines": 0}

                    stats[lang]["files"] += 1
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            lines_count = sum(1 for _ in f)
                            stats[lang]["lines"] += lines_count
                    except Exception:
                        pass

        # Ordenar lenguajes por mayor cantidad de líneas
        sorted_languages = sorted(
            stats.keys(),
            key=lambda l: stats[l]["lines"],
            reverse=True
        )

        return sorted_languages, stats

import hashlib
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from app.schemas.state import FileNode


class DuplicationDetector:
    """Detecta clones de código (Tipo 1 y Tipo 2) mediante hashing de bloques normalizados."""

    def __init__(self, min_block_lines: int = 6):
        self.min_block_lines = min_block_lines

    def normalize_line(self, line: str) -> str:
        """Normaliza una línea eliminando comentarios, espacios redundantes e identificadores literales básicos."""
        # Eliminar comentarios
        line = re.sub(r'#.*|//.*|/\*.*?\*/', '', line)
        # Compactar espacios en blanco
        line = re.sub(r'\s+', ' ', line).strip()
        return line

    def analyze_duplication(self, file_nodes: List[FileNode]) -> Dict[str, Any]:
        """
        Analiza todos los archivos analizados en busca de bloques de código duplicados.
        Retorna:
            - duplication_percentage: Porcentaje de código duplicado (0.0 - 100.0)
            - total_duplicated_lines: Conteo total de líneas en clones
            - total_sloc: Total de líneas analizadas
            - clones: Lista de fragmentos duplicados detectados con archivo y líneas
        """
        block_hashes: Dict[str, List[Tuple[str, int, str]]] = {}
        total_sloc = 0

        for node in file_nodes:
            if not node.raw_content:
                continue

            lines = node.raw_content.splitlines()
            total_sloc += len(lines)

            # Filtrar líneas normalizadas con su índice original (1-indexed)
            indexed_normalized = []
            for i, line in enumerate(lines, 1):
                norm = self.normalize_line(line)
                if norm and len(norm) > 2:  # Ignorar llaves/paréntesis solos
                    indexed_normalized.append((i, norm))

            # Ventana deslizante sobre bloques
            for idx in range(len(indexed_normalized) - self.min_block_lines + 1):
                block = indexed_normalized[idx: idx + self.min_block_lines]
                start_line = block[0][0]
                block_text = "\n".join(b[1] for b in block)

                block_hash = hashlib.md5(block_text.encode('utf-8')).hexdigest()

                if block_hash not in block_hashes:
                    block_hashes[block_hash] = []

                block_hashes[block_hash].append((node.path, start_line, block_text))

        # Filtrar solo bloques con más de 1 aparición
        clones = []
        duplicated_lines_set = set()

        for block_hash, occurrences in block_hashes.items():
            if len(occurrences) > 1:
                # Registrar líneas duplicadas
                for path, start_line, _ in occurrences:
                    for offset in range(self.min_block_lines):
                        duplicated_lines_set.add((path, start_line + offset))

                # Registrar reporte de clon
                primary = occurrences[0]
                for duplicate in occurrences[1:]:
                    clones.append({
                        "file_a": primary[0],
                        "line_a": primary[1],
                        "file_b": duplicate[0],
                        "line_b": duplicate[1],
                        "lines_count": self.min_block_lines,
                        "sample_snippet": primary[2][:200],
                    })

        total_duplicated_lines = len(duplicated_lines_set)
        duplication_pct = (
            round((total_duplicated_lines / max(1, total_sloc)) * 100.0, 2)
            if total_sloc > 0 else 0.0
        )

        return {
            "duplication_percentage": min(100.0, duplication_pct),
            "total_duplicated_lines": total_duplicated_lines,
            "total_sloc": total_sloc,
            "clones_count": len(clones),
            "clones": clones[:30],  # Limitar a top 30 clones para no sobrecargar estado
        }

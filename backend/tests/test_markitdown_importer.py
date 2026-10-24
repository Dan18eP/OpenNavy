import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from app.rag.importer import DocumentIngestor
from app.rag.knowledge_loader import KnowledgeLoader


class TestMarkItDownImporter:
    """Pruebas del pipeline de ingesta automatizado con MarkItDown (ADR-002)."""

    def test_document_ingestor_initialization(self, tmp_path):
        raw_dir = tmp_path / "raw"
        out_dir = tmp_path / "criteria"
        ingestor = DocumentIngestor(raw_dir=raw_dir, output_dir=out_dir)

        assert ingestor.raw_dir == raw_dir
        assert ingestor.output_dir == out_dir
        assert out_dir.exists()

    def test_ingest_txt_or_html_file_with_mocked_markitdown(self, tmp_path):
        raw_dir = tmp_path / "raw"
        out_dir = tmp_path / "criteria"
        raw_dir.mkdir(parents=True, exist_ok=True)

        sample_pdf = raw_dir / "iso_25010_standard_2023.pdf"
        sample_pdf.write_bytes(b"%PDF-1.4 simulated pdf binary content")

        ingestor = DocumentIngestor(raw_dir=raw_dir, output_dir=out_dir)

        # Mockear conversion de MarkItDown
        mock_res = MagicMock()
        mock_res.text_content = "# ISO 25010 Standards\n\n| Metrica | Umbral |\n|---|---|\n| MI | 85 |\n\nTexto oficial."
        ingestor.md_converter = MagicMock()
        ingestor.md_converter.convert.return_value = mock_res

        out_file = ingestor.ingest_file(sample_pdf)

        assert out_file is not None
        assert out_file.exists()
        assert out_file.name == "iso_25010_standard_2023.md"

        content = out_file.read_text(encoding="utf-8")
        assert "**Autoridad:** ISO/IEC" in content
        assert "**Rule-ID:** ISO-25010-2023" in content
        assert "Microsoft MarkItDown" in content
        assert "| Metrica | Umbral |" in content

    def test_ingest_directory_end_to_end_and_loader_extraction(self, tmp_path):
        raw_dir = tmp_path / "raw"
        out_dir = tmp_path / "criteria"
        raw_dir.mkdir(parents=True, exist_ok=True)

        f1 = raw_dir / "owasp_top_10_2024.docx"
        f1.write_bytes(b"PK mock docx")
        f2 = raw_dir / "fowler_refactorings.txt"
        f2.write_text("Martin Fowler Catalog", encoding="utf-8")

        ingestor = DocumentIngestor(raw_dir=raw_dir, output_dir=out_dir)

        def side_effect(path_str):
            mock_res = MagicMock()
            if "owasp" in path_str:
                mock_res.text_content = "## OWASP Directives\nReglas de seguridad criticas para API."
            else:
                mock_res.text_content = "## Fowler Catalog\nExtract Method para reducir longitud."
            return mock_res

        ingestor.md_converter = MagicMock()
        ingestor.md_converter.convert.side_effect = side_effect

        summary = ingestor.ingest_directory(reindex_after=False)
        assert summary["total_processed"] == 2
        assert len(summary["processed_files"]) == 2

        # Verificar que KnowledgeLoader puede cargar los chunks generados
        loader = KnowledgeLoader(knowledge_base_dir=tmp_path)
        chunks = loader.load_all_chunks()
        assert len(chunks) >= 2
        authorities = {c["authority"] for c in chunks}
        assert "OWASP Foundation" in authorities or "Martin Fowler" in authorities

    def test_unsupported_file_extension_ignored(self, tmp_path):
        raw_dir = tmp_path / "raw"
        out_dir = tmp_path / "criteria"
        raw_dir.mkdir(parents=True, exist_ok=True)

        unsupported = raw_dir / "script.exe"
        unsupported.write_bytes(b"binary")

        ingestor = DocumentIngestor(raw_dir=raw_dir, output_dir=out_dir)
        res = ingestor.ingest_file(unsupported)
        assert res is None

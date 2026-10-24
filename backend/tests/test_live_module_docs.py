import pytest
from pathlib import Path
from app.agents.nodes.docs_generator_node import docs_generator_node
from app.agents.nodes.persist_node import persist_node
from app.core.config import settings
from app.rag.knowledge_loader import KnowledgeLoader


class TestLiveModuleDocsAndTeamStandards:
    """Pruebas de gobierno y explotación de module-docs y team-standards."""

    def test_team_standards_loaded_with_correct_tier(self):
        loader = KnowledgeLoader()
        chunks = loader.load_all_chunks()

        team_chunks = [c for c in chunks if c.get("source_tier") == "team_standard"]
        assert len(team_chunks) >= 3, f"Se esperaban al menos 3 chunks de team_standard, encontrados: {len(team_chunks)}"

        criteria_found = {c["criterion"] for c in team_chunks}
        assert "layering_rules" in criteria_found
        assert "naming_conventions" in criteria_found
        assert "git_workflow_standards" in criteria_found

        # Validar autoría de equipo
        authorities = {c["authority"] for c in team_chunks}
        assert "Praxia Engineering Standards Board" in authorities

    def test_docs_generator_and_persist_node_materializes_markdown_in_module_docs(self, tmp_path, monkeypatch):
        # Configurar un KNOWLEDGE_BASE_PATH temporal
        monkeypatch.setattr(settings, "KNOWLEDGE_BASE_PATH", tmp_path)
        (tmp_path / "module-docs").mkdir(parents=True, exist_ok=True)
        (tmp_path / "adrs").mkdir(parents=True, exist_ok=True)

        fake_state = {
            "run_id": 999,
            "repo_id": 1,
            "repo_url": "https://github.com/Dan18eP/sample-service.git",
            "architecture_diff": {
                "has_cycles": True,
                "circular_dependencies": [["service_a", "service_b", "service_a"]],
            },
            "evaluation_report": {
                "global_score": 88.5,
                "is_healthy": True,
                "total_findings": 2,
                "critical_findings": 0,
                "high_findings": 1,
                "warning_findings": 1,
                "criterion_scores": {"architecture": 85.0, "clean_code": 90.0},
            },
        }

        # 1. Generar documentación
        docs_res = docs_generator_node(fake_state)
        generated_docs = docs_res["generated_docs"]
        assert len(generated_docs) >= 2

        summary_doc = next(d for d in generated_docs if d["tipo"] == "summary")
        assert "module-docs/sample-service-architecture-summary.md" == summary_doc["path"]
        assert "**Identificador:** `module_doc_sample_service`" in summary_doc["contenido"]

        # 2. Persistir (debe escribir físicamente en disco)
        persist_state = {**fake_state, "generated_docs": generated_docs}
        persist_node(persist_state)

        # 3. Validar que el archivo físico existe en module-docs/
        target_file = tmp_path / "module-docs" / "sample-service-architecture-summary.md"
        assert target_file.exists(), "El archivo de resumen de arquitectura no se materializó en module-docs/"

        # 4. Validar que KnowledgeLoader puede cargar el nuevo module-doc autogenerado
        loader = KnowledgeLoader(knowledge_base_dir=tmp_path)
        chunks = loader.load_all_chunks()
        module_doc_chunks = [c for c in chunks if c.get("source_tier") == "module_doc"]
        assert len(module_doc_chunks) >= 1
        assert module_doc_chunks[0]["criterion"] == "module_doc_sample_service"

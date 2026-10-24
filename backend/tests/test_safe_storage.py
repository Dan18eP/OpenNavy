import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.core.config import settings
from app.analyzers.repo_cloner import (
    RepoCloner,
    is_safe_ephemeral_dir,
    PRAXIA_SENTINEL_FILE,
)
from app.agents.nodes.clone_node import clone_node
from app.agents.nodes.persist_node import persist_node
from app.schemas.state import AnalysisState


class TestSafeStorageEphemeralValidation:
    """Pruebas de validación estricta para is_safe_ephemeral_dir."""

    def test_valid_ephemeral_dir(self, tmp_path):
        """Un directorio dentro de storage_path con el centinela es válido."""
        storage = tmp_path / "storage"
        storage.mkdir()
        repo_dir = storage / "repo_123"
        repo_dir.mkdir()
        (repo_dir / PRAXIA_SENTINEL_FILE).touch()

        assert is_safe_ephemeral_dir(repo_dir, base_storage=storage) is True

    def test_missing_sentinel_is_rejected(self, tmp_path):
        """Un directorio dentro de storage_path sin centinela es rechazado."""
        storage = tmp_path / "storage"
        storage.mkdir()
        repo_dir = storage / "repo_123"
        repo_dir.mkdir()

        assert is_safe_ephemeral_dir(repo_dir, base_storage=storage) is False

    def test_outside_storage_is_rejected(self, tmp_path):
        """Un directorio fuera de storage_path es rechazado incluso si tiene el centinela."""
        storage = tmp_path / "storage"
        storage.mkdir()
        outside_dir = tmp_path / "user_project"
        outside_dir.mkdir()
        (outside_dir / PRAXIA_SENTINEL_FILE).touch()

        assert is_safe_ephemeral_dir(outside_dir, base_storage=storage) is False

    def test_storage_root_itself_is_rejected(self, tmp_path):
        """La raíz de almacenamiento jamás puede ser eliminada."""
        storage = tmp_path / "storage"
        storage.mkdir()
        (storage / PRAXIA_SENTINEL_FILE).touch()

        assert is_safe_ephemeral_dir(storage, base_storage=storage) is False

    def test_nonexistent_path_is_rejected(self, tmp_path):
        """Rutas no existentes devuelven False."""
        storage = tmp_path / "storage"
        storage.mkdir()
        nonexistent = storage / "does_not_exist"

        assert is_safe_ephemeral_dir(nonexistent, base_storage=storage) is False


class TestRepoClonerCleanup:
    """Pruebas de limpieza segura en RepoCloner."""

    def test_cleanup_deletes_valid_ephemeral_dir(self, tmp_path):
        """Cleanup elimina correctamente un directorio efímero autenticado."""
        storage = tmp_path / "storage"
        storage.mkdir()
        repo_dir = storage / "repo_abc"
        repo_dir.mkdir()
        (repo_dir / PRAXIA_SENTINEL_FILE).touch()
        (repo_dir / "sample.py").write_text("print('hello')")

        cloner = RepoCloner(base_storage_path=storage)
        result = cloner.cleanup(str(repo_dir))

        assert result is True
        assert not repo_dir.exists()

    def test_cleanup_refuses_unsafe_directory(self, tmp_path):
        """Cleanup rechaza eliminar un directorio que no cumple con las reglas."""
        storage = tmp_path / "storage"
        storage.mkdir()
        user_dir = tmp_path / "user_code"
        user_dir.mkdir()
        (user_dir / "main.py").write_text("critical user code")

        cloner = RepoCloner(base_storage_path=storage)
        result = cloner.cleanup(str(user_dir))

        assert result is False
        assert user_dir.exists()
        assert (user_dir / "main.py").is_file()

    def test_prepare_repo_local_is_never_temporary(self, tmp_path):
        """Rutas locales existentes no son marcadas como temporales ni llevan centinela."""
        local_repo = tmp_path / "my_local_repo"
        local_repo.mkdir()
        (local_repo / "app.py").write_text("code")

        cloner = RepoCloner()
        path, sha, is_temp = cloner.prepare_repo(str(local_repo))

        assert is_temp is False
        assert path == str(local_repo)
        assert not (local_repo / PRAXIA_SENTINEL_FILE).exists()


class TestNodeIntegrationSafeStorage:
    """Pruebas de integración de nodos clone_node y persist_node."""

    def test_clone_node_propagates_is_temporary_false_for_local(self, tmp_path):
        """clone_node propaga is_temporary=False para repositorios locales."""
        local_repo = tmp_path / "local_repo"
        local_repo.mkdir()

        state: AnalysisState = {
            "run_id": "test_run",
            "repo_id": "test_repo",
            "repo_url": str(local_repo),
            "branch": "main",
            "local_path": "",
            "is_temporary": None,
            "languages_detected": [],
            "files": [],
            "static_metrics": {},
            "complexity_findings": [],
            "solid_violations": [],
            "architecture_diff": None,
            "dependencies": None,
            "rag_context": [],
            "evaluation_report": {},
            "generated_docs": [],
            "errors": [],
            "retry_count": 0,
            "current_step": "init",
        }

        output = clone_node(state)
        assert output["is_temporary"] is False
        assert output["local_path"] == str(local_repo)

    def test_persist_node_does_not_delete_local_repo_even_with_temp_repos_in_path(self, tmp_path):
        """
        ESCENARIO CRÍTICO:
        Un usuario tiene un repositorio local en una ruta como '/home/user/temp_repos/my_app'.
        persist_node NUNCA debe eliminar esta carpeta porque is_temporary es False.
        """
        temp_repos_folder = tmp_path / "temp_repos"
        temp_repos_folder.mkdir()
        user_project = temp_repos_folder / "precious_user_project"
        user_project.mkdir()
        (user_project / "important.py").write_text("DO NOT DELETE THIS")

        state: AnalysisState = {
            "run_id": "test_run",
            "repo_id": "test_repo",
            "repo_url": str(user_project),
            "branch": "main",
            "local_path": str(user_project),
            "is_temporary": False,  # No es efímero
            "languages_detected": [],
            "files": [],
            "static_metrics": {},
            "complexity_findings": [],
            "solid_violations": [],
            "architecture_diff": None,
            "dependencies": None,
            "rag_context": [],
            "evaluation_report": {},
            "generated_docs": [],
            "errors": [],
            "retry_count": 0,
            "current_step": "evaluating",
        }

        with patch("app.agents.nodes.persist_node.SessionLocal") as mock_session_cls:
            mock_session = MagicMock()
            mock_session_cls.return_value = mock_session

            output = persist_node(state)

            assert output["current_step"] == "completed"
            # Verificar que el proyecto del usuario sigue intacto
            assert user_project.exists()
            assert (user_project / "important.py").is_file()
            assert (user_project / "important.py").read_text() == "DO NOT DELETE THIS"

    def test_persist_node_safely_cleans_when_is_temporary_true(self, tmp_path):
        """Cuando is_temporary=True y es un clon efímero válido, persist_node lo limpia."""
        storage = settings.CLONE_STORAGE_PATH
        storage.mkdir(parents=True, exist_ok=True)

        ephemeral_repo = storage / f"test_ephemeral_{os.getpid()}"
        ephemeral_repo.mkdir()
        (ephemeral_repo / PRAXIA_SENTINEL_FILE).touch()
        (ephemeral_repo / "cloned.py").write_text("temp clone")

        state: AnalysisState = {
            "run_id": "test_run",
            "repo_id": "test_repo",
            "repo_url": "https://github.com/example/repo.git",
            "branch": "main",
            "local_path": str(ephemeral_repo),
            "is_temporary": True,  # Es efímero
            "languages_detected": [],
            "files": [],
            "static_metrics": {},
            "complexity_findings": [],
            "solid_violations": [],
            "architecture_diff": None,
            "dependencies": None,
            "rag_context": [],
            "evaluation_report": {},
            "generated_docs": [],
            "errors": [],
            "retry_count": 0,
            "current_step": "evaluating",
        }

        with patch("app.agents.nodes.persist_node.SessionLocal") as mock_session_cls:
            mock_session = MagicMock()
            mock_session_cls.return_value = mock_session

            output = persist_node(state)

            assert output["current_step"] == "completed"
            # Verificar que el clon efímero sí fue limpiado
            assert not ephemeral_repo.exists()

from typing import Dict, Any
from app.schemas.state import AnalysisState
from app.analyzers.repo_cloner import RepoCloner


def clone_node(state: AnalysisState) -> Dict[str, Any]:
    """Nodo 1: Clona o valida la existencia del repositorio en disco."""
    repo_url = state.get("repo_url", "")
    branch = state.get("branch", "main")
    cloner = RepoCloner()

    try:
        local_path, commit_sha, is_temp = cloner.prepare_repo(repo_url, branch)
        return {
            "local_path": local_path,
            "is_temporary": is_temp,
            "current_step": "cloned",
            "errors": state.get("errors", []),
        }
    except Exception as e:
        errors = list(state.get("errors", []))
        errors.append(f"Error en clonado: {str(e)}")
        return {
            "errors": errors,
            "current_step": "failed",
        }

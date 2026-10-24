import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Optional, Tuple, Union
from app.core.config import settings

PRAXIA_SENTINEL_FILE = ".opennavy_ephemeral"
LEGACY_PRAXIA_SENTINEL_FILE = ".praxia_ephemeral"


def is_safe_ephemeral_dir(path: Union[Path, str], base_storage: Optional[Path] = None) -> bool:
    """
    Verifica de forma estricta que una ruta sea un directorio temporal legítimo y seguro para eliminación:
    1. Debe existir y ser un directorio.
    2. Su ruta canónica resuelta (evitando symlinks y traversal) debe estar contenida estrictamente
       dentro de base_storage (por defecto settings.CLONE_STORAGE_PATH).
    3. No puede ser la raíz del almacenamiento (base_storage).
    4. Debe contener el archivo centinela .praxia_ephemeral creado al momento del clonado efímero.
    """
    try:
        dir_path = Path(path).resolve()
        storage_root = (base_storage or settings.CLONE_STORAGE_PATH).resolve()

        if not dir_path.exists() or not dir_path.is_dir():
            return False

        # Evitar borrar la raíz de almacenamiento o un ancestro
        if dir_path == storage_root:
            return False

        # Comprobar pertenencia estricta dentro de storage_root
        try:
            dir_path.relative_to(storage_root)
        except ValueError:
            return False

        # Comprobar archivo centinela obligatorio
        sentinel_path = dir_path / PRAXIA_SENTINEL_FILE
        if not sentinel_path.exists() or not sentinel_path.is_file():
            return False

        return True
    except Exception:
        return False


class RepoCloner:
    """Gestiona la descarga y clonado seguro de repositorios Git."""

    def __init__(self, base_storage_path: Optional[Path] = None):
        self.storage_path = base_storage_path or settings.CLONE_STORAGE_PATH
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def prepare_repo(self, repo_url_or_path: str, branch: str = "main") -> Tuple[str, str, bool]:
        """
        Prepara el repositorio para análisis.
        Si es una ruta local existente, la retorna directamente.
        Si es una URL remota de Git (http/https/git@), clona en carpeta temporal con shallow clone.

        Retorna:
            - local_path: Ruta al directorio local listo para ser analizado.
            - commit_sha: SHA del último commit (o 'local-head' si no aplica).
            - is_temporary: Booleano indicando si la carpeta debe ser eliminada tras el análisis.
        """
        # 1. Comprobar si es ruta local existente
        local_path = Path(repo_url_or_path)
        if local_path.exists() and local_path.is_dir():
            commit_sha = self._get_commit_sha(str(local_path)) or "local-head"
            return str(local_path), commit_sha, False

        # 2. Clonado remoto a directorio temporal aislado
        clone_id = f"repo_{uuid.uuid4().hex[:10]}"
        dest_dir = self.storage_path / clone_id

        cmd = [
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            branch,
            repo_url_or_path,
            str(dest_dir),
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=120,
            )
        except subprocess.CalledProcessError as e:
            err_output = (e.stderr or e.stdout or "").strip()
            # Si el error es explícitamente que la rama solicitada no existe, intentar fallback a default branch
            if "Remote branch" in err_output and "not found" in err_output:
                try:
                    cmd_fallback = [
                        "git",
                        "clone",
                        "--depth",
                        "1",
                        repo_url_or_path,
                        str(dest_dir),
                    ]
                    subprocess.run(
                        cmd_fallback,
                        capture_output=True,
                        text=True,
                        check=True,
                        timeout=120,
                    )
                except subprocess.CalledProcessError as ex_fb:
                    if dest_dir.exists():
                        (dest_dir / PRAXIA_SENTINEL_FILE).touch(exist_ok=True)
                        self.cleanup(str(dest_dir))
                    fb_err = (ex_fb.stderr or ex_fb.stdout or "").strip()
                    raise RuntimeError(f"La rama '{branch}' no fue encontrada en el repositorio remoto, y el intento con la rama predeterminada también falló: {fb_err}")
                except Exception as ex_gen:
                    if dest_dir.exists():
                        (dest_dir / PRAXIA_SENTINEL_FILE).touch(exist_ok=True)
                        self.cleanup(str(dest_dir))
                    raise RuntimeError(f"La rama '{branch}' no existe en el repositorio remoto.")
            else:
                if dest_dir.exists():
                    (dest_dir / PRAXIA_SENTINEL_FILE).touch(exist_ok=True)
                    self.cleanup(str(dest_dir))
                raise RuntimeError(err_output if err_output else f"Error al ejecutar git clone (código {e.returncode})")
        except Exception as ex:
            if dest_dir.exists():
                (dest_dir / PRAXIA_SENTINEL_FILE).touch(exist_ok=True)
                self.cleanup(str(dest_dir))
            raise RuntimeError(f"Error inesperado al clonar repositorio: {str(ex)}")

        # Marcar directorio como efímero y seguro mediante archivo centinela
        (dest_dir / PRAXIA_SENTINEL_FILE).touch(exist_ok=True)

        commit_sha = self._get_commit_sha(str(dest_dir)) or "remote-head"
        return str(dest_dir), commit_sha, True

    def _get_commit_sha(self, repo_path: str) -> Optional[str]:
        """Obtiene el SHA del commit actual usando git."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None

    def cleanup(self, path: str) -> bool:
        """
        Elimina el directorio temporal del repositorio clonado de manera segura.
        Solo procede si is_safe_ephemeral_dir confirma que el directorio es un clon
        efímero legítimo y reside estrictamente dentro de storage_path.
        Retorna True si se eliminó, False si fue rechazado por seguridad o no existía.
        """
        dir_path = Path(path)
        if not is_safe_ephemeral_dir(dir_path, self.storage_path):
            return False

        def on_rm_error(func, p, exc_info):
            # Manejar permisos de solo lectura en Windows (.git/objects)
            os.chmod(p, 0o777)
            try:
                func(p)
            except Exception:
                pass

        shutil.rmtree(dir_path, onerror=on_rm_error)
        return True

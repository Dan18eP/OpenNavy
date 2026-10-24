import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


# Catálogo curado de versiones estables recomendadas y reglas de compatibilidad para paquetes comunes
POPULAR_PACKAGES_CATALOG: Dict[str, Dict[str, Any]] = {
    # ── Python Ecosistema ───────────────────────────────────────────────
    "fastapi": {
        "recommended": "0.115.6",
        "min_compatible": "0.100.0",
        "incompatibilities": [
            {"condition": "<0.100.0", "reason": "Incompatible con Pydantic v2 y OpenAPI 3.1.0"}
        ],
        "upgrade_command": "pip install --upgrade fastapi=={version}",
        "ecosystem": "python"
    },
    "pydantic": {
        "recommended": "2.10.4",
        "min_compatible": "2.0.0",
        "incompatibilities": [
            {"condition": "<2.0.0", "reason": "Pydantic v1 está deprecado y genera problemas de tipado con Python 3.12+"}
        ],
        "upgrade_command": "pip install --upgrade pydantic=={version}",
        "ecosystem": "python"
    },
    "pydantic-settings": {
        "recommended": "2.7.0",
        "min_compatible": "2.0.0",
        "incompatibilities": [
            {"condition": "<2.0.0", "reason": "Requiere Pydantic v2 para soporte de BaseSettings"}
        ],
        "upgrade_command": "pip install --upgrade pydantic-settings=={version}",
        "ecosystem": "python"
    },
    "langchain": {
        "recommended": "0.3.14",
        "min_compatible": "0.2.0",
        "incompatibilities": [
            {"condition": "<0.2.0", "reason": "Arquitectura modular antigua antes de separar langchain-core"}
        ],
        "upgrade_command": "pip install --upgrade langchain=={version}",
        "ecosystem": "python"
    },
    "langgraph": {
        "recommended": "0.2.60",
        "min_compatible": "0.2.0",
        "incompatibilities": [
            {"condition": "<0.1.0", "reason": "Versiones antiguas de LangGraph tienen API incompatible con StateGraph moderno"}
        ],
        "upgrade_command": "pip install --upgrade langgraph=={version}",
        "ecosystem": "python"
    },
    "langchain-core": {
        "recommended": "0.3.29",
        "min_compatible": "0.2.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade langchain-core=={version}",
        "ecosystem": "python"
    },
    "langchain-community": {
        "recommended": "0.3.14",
        "min_compatible": "0.2.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade langchain-community=={version}",
        "ecosystem": "python"
    },
    "langchain-openai": {
        "recommended": "0.2.14",
        "min_compatible": "0.1.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade langchain-openai=={version}",
        "ecosystem": "python"
    },
    "reportlab": {
        "recommended": "4.2.5",
        "min_compatible": "4.0.0",
        "incompatibilities": [
            {"condition": "<4.0.0", "reason": "ReportLab 3.x no es compatible con Python 3.12+ ni fuentes TTF modernas"}
        ],
        "upgrade_command": "pip install --upgrade reportlab=={version}",
        "ecosystem": "python"
    },
    "sqlalchemy": {
        "recommended": "2.0.36",
        "min_compatible": "2.0.0",
        "incompatibilities": [
            {"condition": "<2.0.0", "reason": "SQLAlchemy 1.4 está en fin de ciclo; la sintaxis select() moderna requiere 2.0+"}
        ],
        "upgrade_command": "pip install --upgrade sqlalchemy=={version}",
        "ecosystem": "python"
    },
    "alembic": {
        "recommended": "1.14.0",
        "min_compatible": "1.10.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade alembic=={version}",
        "ecosystem": "python"
    },
    "pytest": {
        "recommended": "8.3.4",
        "min_compatible": "8.0.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade pytest=={version}",
        "ecosystem": "python"
    },
    "pytest-asyncio": {
        "recommended": "0.25.0",
        "min_compatible": "0.23.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade pytest-asyncio=={version}",
        "ecosystem": "python"
    },
    "uvicorn": {
        "recommended": "0.34.0",
        "min_compatible": "0.28.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade uvicorn=={version}",
        "ecosystem": "python"
    },
    "requests": {
        "recommended": "2.32.3",
        "min_compatible": "2.31.0",
        "incompatibilities": [
            {"condition": "<2.31.0", "reason": "Vulnerabilidad de fuga de encabezados de autenticación en redirecciones (CVE-2023-32681)"}
        ],
        "upgrade_command": "pip install --upgrade requests=={version}",
        "ecosystem": "python"
    },
    "httpx": {
        "recommended": "0.28.1",
        "min_compatible": "0.27.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade httpx=={version}",
        "ecosystem": "python"
    },
    "python-dotenv": {
        "recommended": "1.0.1",
        "min_compatible": "1.0.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade python-dotenv=={version}",
        "ecosystem": "python"
    },
    "python-multipart": {
        "recommended": "0.0.20",
        "min_compatible": "0.0.9",
        "incompatibilities": [
            {"condition": "<0.0.7", "reason": "Vulnerabilidad DoS por consumo excesivo de memoria en multipart/form-data (CVE-2024-24762)"}
        ],
        "upgrade_command": "pip install --upgrade python-multipart=={version}",
        "ecosystem": "python"
    },
    "aiosqlite": {
        "recommended": "0.20.0",
        "min_compatible": "0.19.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade aiosqlite=={version}",
        "ecosystem": "python"
    },
    "psycopg2-binary": {
        "recommended": "2.9.10",
        "min_compatible": "2.9.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade psycopg2-binary=={version}",
        "ecosystem": "python"
    },
    "celery": {
        "recommended": "5.4.0",
        "min_compatible": "5.2.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade celery=={version}",
        "ecosystem": "python"
    },
    "redis": {
        "recommended": "5.2.1",
        "min_compatible": "5.0.0",
        "incompatibilities": [],
        "upgrade_command": "pip install --upgrade redis=={version}",
        "ecosystem": "python"
    },
    "pyyaml": {
        "recommended": "6.0.2",
        "min_compatible": "6.0.0",
        "incompatibilities": [
            {"condition": "<5.4", "reason": "Vulnerabilidad crítica de ejecución remota de código en yaml.load() (CVE-2020-14343)"}
        ],
        "upgrade_command": "pip install --upgrade pyyaml=={version}",
        "ecosystem": "python"
    },
    "flask": {
        "recommended": "3.1.0",
        "min_compatible": "3.0.0",
        "incompatibilities": [
            {"condition": "<2.3.0", "reason": "Flask 2.x tiene dependencias deprecadas de Werkzeug"}
        ],
        "upgrade_command": "pip install --upgrade flask=={version}",
        "ecosystem": "python"
    },
    "django": {
        "recommended": "5.1.4",
        "min_compatible": "4.2.0",
        "incompatibilities": [
            {"condition": "<4.2.0", "reason": "Versión en Fin de Vida (EOL) sin parches de seguridad activos"}
        ],
        "upgrade_command": "pip install --upgrade django=={version}",
        "ecosystem": "python"
    },
    "cryptography": {
        "recommended": "44.0.0",
        "min_compatible": "41.0.0",
        "incompatibilities": [
            {"condition": "<41.0.0", "reason": "Vulnerabilidades de desbordamiento de buffer en OpenSSL empotrado"}
        ],
        "upgrade_command": "pip install --upgrade cryptography=={version}",
        "ecosystem": "python"
    },
    "urllib3": {
        "recommended": "2.3.0",
        "min_compatible": "2.0.0",
        "incompatibilities": [
            {"condition": "<1.26.18", "reason": "Múltiples vulnerabilidades de fuga de cookies y cabeceras"}
        ],
        "upgrade_command": "pip install --upgrade urllib3=={version}",
        "ecosystem": "python"
    },

    # ── Node / JavaScript / TypeScript Ecosistema ───────────────────────
    "react": {
        "recommended": "18.3.1",
        "min_compatible": "18.2.0",
        "incompatibilities": [
            {"condition": "<18.0.0", "reason": "React 17 o inferior no soporta Concurrent Rendering ni hooks modernos"}
        ],
        "upgrade_command": "npm install react@^{version}",
        "ecosystem": "npm"
    },
    "react-dom": {
        "recommended": "18.3.1",
        "min_compatible": "18.2.0",
        "incompatibilities": [
            {"condition": "<18.0.0", "reason": "Debe coincidir con la versión de React para evitar desincronización del reconciliador"}
        ],
        "upgrade_command": "npm install react-dom@^{version}",
        "ecosystem": "npm"
    },
    "vite": {
        "recommended": "5.4.11",
        "min_compatible": "5.0.0",
        "incompatibilities": [
            {"condition": "<5.0.0", "reason": "Vite 4 requiere Node.js antiguo y tiene menor rendimiento en Rollup 4"}
        ],
        "upgrade_command": "npm install -D vite@^{version}",
        "ecosystem": "npm"
    },
    "typescript": {
        "recommended": "5.7.2",
        "min_compatible": "5.2.0",
        "incompatibilities": [
            {"condition": "<5.0.0", "reason": "Falta de soporte para decoradores estándar y módulos ES modernos"}
        ],
        "upgrade_command": "npm install -D typescript@^{version}",
        "ecosystem": "npm"
    },
    "lucide-react": {
        "recommended": "0.468.0",
        "min_compatible": "0.350.0",
        "incompatibilities": [],
        "upgrade_command": "npm install lucide-react@^{version}",
        "ecosystem": "npm"
    },
    "axios": {
        "recommended": "1.7.9",
        "min_compatible": "1.6.0",
        "incompatibilities": [
            {"condition": "<1.6.0", "reason": "Vulnerabilidad SSRF y problemas de serialización en versiones 0.x/1.5"}
        ],
        "upgrade_command": "npm install axios@^{version}",
        "ecosystem": "npm"
    },
    "express": {
        "recommended": "4.21.2",
        "min_compatible": "4.19.0",
        "incompatibilities": [
            {"condition": "<4.19.2", "reason": "Vulnerabilidad en el parseo de rutas y cookies (CVE-2024-29041)"}
        ],
        "upgrade_command": "npm install express@^{version}",
        "ecosystem": "npm"
    },
    "lodash": {
        "recommended": "4.17.21",
        "min_compatible": "4.17.21",
        "incompatibilities": [
            {"condition": "<4.17.21", "reason": "Vulnerabilidades críticas de Prototype Pollution en versiones previas"}
        ],
        "upgrade_command": "npm install lodash@^{version}",
        "ecosystem": "npm"
    },
    "next": {
        "recommended": "15.1.3",
        "min_compatible": "14.0.0",
        "incompatibilities": [
            {"condition": "<13.4.0", "reason": "Falta de soporte para App Router estable y React Server Components"}
        ],
        "upgrade_command": "npm install next@^{version}",
        "ecosystem": "npm"
    },
    "tailwindcss": {
        "recommended": "3.4.17",
        "min_compatible": "3.3.0",
        "incompatibilities": [],
        "upgrade_command": "npm install -D tailwindcss@^{version}",
        "ecosystem": "npm"
    },
    "clsx": {
        "recommended": "2.1.1",
        "min_compatible": "2.0.0",
        "incompatibilities": [],
        "upgrade_command": "npm install clsx@^{version}",
        "ecosystem": "npm"
    },
    "zustand": {
        "recommended": "5.0.2",
        "min_compatible": "4.4.0",
        "incompatibilities": [],
        "upgrade_command": "npm install zustand@^{version}",
        "ecosystem": "npm"
    },
    "vue": {
        "recommended": "3.5.13",
        "min_compatible": "3.3.0",
        "incompatibilities": [
            {"condition": "<3.0.0", "reason": "Vue 2 está en Fin de Vida oficial (EOL)"}
        ],
        "upgrade_command": "npm install vue@^{version}",
        "ecosystem": "npm"
    },
    "eslint": {
        "recommended": "9.17.0",
        "min_compatible": "8.56.0",
        "incompatibilities": [
            {"condition": "<8.0.0", "reason": "Incompatible con plugins modernos y configuración modular"}
        ],
        "upgrade_command": "npm install -D eslint@^{version}",
        "ecosystem": "npm"
    },
    "prettier": {
        "recommended": "3.4.2",
        "min_compatible": "3.0.0",
        "incompatibilities": [],
        "upgrade_command": "npm install -D prettier@^{version}",
        "ecosystem": "npm"
    },
    "@types/react": {
        "recommended": "18.3.18",
        "min_compatible": "18.2.0",
        "incompatibilities": [],
        "upgrade_command": "npm install -D @types/react@^{version}",
        "ecosystem": "npm"
    },
    "@types/react-dom": {
        "recommended": "18.3.5",
        "min_compatible": "18.2.0",
        "incompatibilities": [],
        "upgrade_command": "npm install -D @types/react-dom@^{version}",
        "ecosystem": "npm"
    },
    "@vitejs/plugin-react": {
        "recommended": "4.3.4",
        "min_compatible": "4.0.0",
        "incompatibilities": [],
        "upgrade_command": "npm install -D @vitejs/plugin-react@^{version}",
        "ecosystem": "npm"
    },
    "moment": {
        "recommended": "2.30.1",
        "min_compatible": "2.29.4",
        "incompatibilities": [
            {"condition": "<2.29.4", "reason": "Vulnerabilidad ReDoS (CVE-2022-31129). Librería en mantenimiento: se sugiere migrar a date-fns"}
        ],
        "upgrade_command": "npm install moment@^{version}",
        "ecosystem": "npm"
    },
    "jsonwebtoken": {
        "recommended": "9.0.2",
        "min_compatible": "9.0.0",
        "incompatibilities": [
            {"condition": "<9.0.0", "reason": "Vulnerabilidad crítica en validación de claves asimétricas (CVE-2022-23529)"}
        ],
        "upgrade_command": "npm install jsonwebtoken@^{version}",
        "ecosystem": "npm"
    },

    # ── Java / Maven Ecosistema ─────────────────────────────────────────
    "spring-boot-starter-web": {
        "recommended": "3.4.1",
        "min_compatible": "3.0.0",
        "incompatibilities": [
            {"condition": "<3.0.0", "reason": "Spring Boot 2.x está en EOL y requiere Java 8/11. Spring Boot 3 requiere Java 17+"}
        ],
        "upgrade_command": "<version>{version}</version>",
        "ecosystem": "maven"
    },
    "jackson-databind": {
        "recommended": "2.18.2",
        "min_compatible": "2.15.0",
        "incompatibilities": [
            {"condition": "<2.14.0", "reason": "Vulnerabilidades de deserialización polimórfica"}
        ],
        "upgrade_command": "<version>{version}</version>",
        "ecosystem": "maven"
    },
    "log4j-core": {
        "recommended": "2.24.3",
        "min_compatible": "2.17.1",
        "incompatibilities": [
            {"condition": "<2.17.1", "reason": "Vulnerabilidad crítica Log4Shell RCE (CVE-2021-44228)"}
        ],
        "upgrade_command": "<version>{version}</version>",
        "ecosystem": "maven"
    },

    # ── Go Ecosistema ───────────────────────────────────────────────────
    "github.com/gin-gonic/gin": {
        "recommended": "v1.10.0",
        "min_compatible": "v1.9.0",
        "incompatibilities": [],
        "upgrade_command": "go get github.com/gin-gonic/gin@{version}",
        "ecosystem": "go"
    },
    "gorm.io/gorm": {
        "recommended": "v1.25.12",
        "min_compatible": "v1.24.0",
        "incompatibilities": [],
        "upgrade_command": "go get gorm.io/gorm@{version}",
        "ecosystem": "go"
    },

    # ── Rust Ecosistema ─────────────────────────────────────────────────
    "tokio": {
        "recommended": "1.42.0",
        "min_compatible": "1.35.0",
        "incompatibilities": [],
        "upgrade_command": "cargo update -p tokio --precise {version}",
        "ecosystem": "cargo"
    },
    "serde": {
        "recommended": "1.0.216",
        "min_compatible": "1.0.190",
        "incompatibilities": [],
        "upgrade_command": "cargo update -p serde --precise {version}",
        "ecosystem": "cargo"
    }
}


def parse_semver(version_str: str) -> Tuple[int, int, int]:
    """Extrae tupla (major, minor, patch) a partir de cadenas de versión comunes."""
    if not version_str:
        return (0, 0, 0)
    cleaned = re.sub(r"^[^\d]*", "", version_str.strip())
    parts = re.split(r"[\.\-]", cleaned)
    try:
        major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
        minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        patch = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        return (major, minor, patch)
    except Exception:
        return (0, 0, 0)


def compare_versions(v1: str, v2: str) -> int:
    """
    Retorna:
       1 si v1 > v2
      -1 si v1 < v2
       0 si v1 == v2
    """
    s1 = parse_semver(v1)
    s2 = parse_semver(v2)
    if s1 > s2:
        return 1
    elif s1 < s2:
        return -1
    return 0


class DependencyVersionAnalyzer:
    """
    Analizador autónomo para control de versiones de dependencias,
    detección de obsolescencia, incompatibilidades técnicas y propuestas de actualización.
    """

    def __init__(self, catalog: Optional[Dict[str, Dict[str, Any]]] = None):
        self.catalog = catalog or POPULAR_PACKAGES_CATALOG

    def analyze_dependencies(self, repo_path: str | Path) -> Dict[str, Any]:
        """
        Escanea el directorio del repositorio en busca de manifiestos y analiza
        el estado de versiones y compatibilidad de cada paquete.
        """
        root = Path(repo_path)
        if not root.exists() or not root.is_dir():
            return self._empty_response()

        raw_deps = self._collect_manifest_dependencies(root)
        unique_deps = self._deduplicate_dependencies(raw_deps)
        evaluated_deps, counts = self._evaluate_dependencies_list(unique_deps)

        total_deps = len(evaluated_deps)
        score = self._calculate_health_score(counts, total_deps)
        ecosystems = sorted(list(set(d["ecosystem"] for d in evaluated_deps)))

        return {
            "score": score,
            "total_dependencies": total_deps,
            "up_to_date_count": counts["up_to_date"],
            "outdated_count": counts["patch"] + counts["minor"] + counts["major"] + counts["incompatible"],
            "patch_updates_count": counts["patch"],
            "minor_updates_count": counts["minor"],
            "major_updates_count": counts["major"],
            "incompatible_count": counts["incompatible"],
            "ecosystems": ecosystems,
            "dependencies": evaluated_deps,
        }

    def _empty_response(self) -> Dict[str, Any]:
        return {
            "score": 100.0,
            "total_dependencies": 0,
            "up_to_date_count": 0,
            "outdated_count": 0,
            "incompatible_count": 0,
            "patch_updates_count": 0,
            "minor_updates_count": 0,
            "major_updates_count": 0,
            "dependencies": [],
            "ecosystems": [],
        }

    def _collect_manifest_dependencies(self, root: Path) -> List[Dict[str, Any]]:
        """Recorre el árbol de archivos extrayendo dependencias de todos los manifiestos soportados."""
        deps: List[Dict[str, Any]] = []

        for req_file in root.rglob("*.txt"):
            if ("requirements" in req_file.name.lower() or "deps" in req_file.name.lower()) and not self._is_ignored_path(req_file, root):
                deps.extend(self._parse_requirements_txt(req_file, root))

        for pyproject in root.rglob("pyproject.toml"):
            if not self._is_ignored_path(pyproject, root):
                deps.extend(self._parse_pyproject_toml(pyproject, root))

        for pipfile in root.rglob("Pipfile"):
            if not self._is_ignored_path(pipfile, root):
                deps.extend(self._parse_pipfile(pipfile, root))

        for pkg_file in root.rglob("package.json"):
            if not self._is_ignored_path(pkg_file, root):
                deps.extend(self._parse_package_json(pkg_file, root))

        for pom_file in root.rglob("pom.xml"):
            if not self._is_ignored_path(pom_file, root):
                deps.extend(self._parse_pom_xml(pom_file, root))

        for gomod in root.rglob("go.mod"):
            if not self._is_ignored_path(gomod, root):
                deps.extend(self._parse_go_mod(gomod, root))

        for cargo in root.rglob("Cargo.toml"):
            if not self._is_ignored_path(cargo, root):
                deps.extend(self._parse_cargo_toml(cargo, root))

        return deps

    def _deduplicate_dependencies(self, deps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Elimina dependencias duplicadas dentro del mismo manifiesto y ecosistema."""
        seen = set()
        unique = []
        for dep in deps:
            key = f"{dep['ecosystem']}:{dep['package_name']}:{dep['source_file']}"
            if key not in seen:
                seen.add(key)
                unique.append(dep)
        return unique

    def _evaluate_dependencies_list(
        self,
        deps: List[Dict[str, Any]],
    ) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
        """Evalúa individualmente cada dependencia y calcula los conteos por estado."""
        evaluated: List[Dict[str, Any]] = []
        counts = {"up_to_date": 0, "patch": 0, "minor": 0, "major": 0, "incompatible": 0}

        for dep in deps:
            pkg_name = dep["package_name"]
            current_ver = dep["current_version"]
            source_file = dep["source_file"]
            ecosystem = dep["ecosystem"]

            eval_res = self._evaluate_package(pkg_name.lower(), current_ver, ecosystem)
            evaluated.append({
                "package_name": pkg_name,
                "ecosystem": ecosystem,
                "source_file": source_file,
                "current_version": current_ver or "unspecified",
                "recommended_version": eval_res["recommended_version"],
                "status": eval_res["status"],
                "is_compatible": eval_res["is_compatible"],
                "risk_level": eval_res["risk_level"],
                "reason": eval_res["reason"],
                "upgrade_command": eval_res["upgrade_command"],
            })

            status = eval_res["status"]
            if status == "up_to_date":
                counts["up_to_date"] += 1
            elif status == "patch_update":
                counts["patch"] += 1
            elif status == "minor_update":
                counts["minor"] += 1
            elif status == "major_update":
                counts["major"] += 1
            elif status == "incompatible":
                counts["incompatible"] += 1

        return evaluated, counts

    def _calculate_health_score(self, counts: Dict[str, int], total_deps: int) -> float:
        """Calcula la puntuación ponderada de salud de dependencias (0 - 100)."""
        if total_deps == 0:
            return 100.0
        penalty = (
            (counts["incompatible"] * 30.0)
            + (counts["major"] * 12.0)
            + (counts["minor"] * 4.0)
            + (counts["patch"] * 1.5)
        )
        return max(0.0, min(100.0, round(100.0 - penalty, 1)))

    def _check_incompatibility_rules(
        self,
        info: Dict[str, Any],
        clean_raw_ver: str,
        rec_ver: str,
        cmd: str,
    ) -> Optional[Dict[str, Any]]:
        """Verifica si la versión actual viola alguna regla de incompatibilidad explícita."""
        for incomp in info.get("incompatibilities", []):
            cond = incomp.get("condition", "")
            if cond.startswith("<"):
                threshold_ver = cond[1:]
                if compare_versions(clean_raw_ver, threshold_ver) < 0:
                    return {
                        "recommended_version": rec_ver,
                        "status": "incompatible",
                        "is_compatible": False,
                        "risk_level": "critical",
                        "reason": f"Incompatibilidad crítica: {incomp.get('reason', 'Versión no soportada')}",
                        "upgrade_command": cmd,
                    }
        return None

    def _evaluate_catalog_package(
        self,
        info: Dict[str, Any],
        pkg_name: str,
        clean_raw_ver: str,
        is_unpinned: bool,
        ecosystem: str,
    ) -> Dict[str, Any]:
        """Evalúa un paquete registrado en el catálogo conocido."""
        rec_ver = info["recommended"]
        default_cmd = "npm install {pkg}@{version}" if ecosystem == "npm" else "pip install --upgrade {pkg}=={version}"
        cmd_tpl = info.get("upgrade_command", default_cmd)
        cmd = cmd_tpl.format(pkg=pkg_name, version=rec_ver)

        if is_unpinned:
            return {
                "recommended_version": rec_ver,
                "status": "minor_update",
                "is_compatible": True,
                "risk_level": "medium",
                "reason": f"Dependencia sin fijar (versión flotante). Se recomienda fijar a la versión estable {rec_ver} para compilaciones reproducibles.",
                "upgrade_command": cmd,
            }

        incomp_match = self._check_incompatibility_rules(info, clean_raw_ver, rec_ver, cmd)
        if incomp_match:
            return incomp_match

        if compare_versions(clean_raw_ver, rec_ver) >= 0:
            return {
                "recommended_version": rec_ver,
                "status": "up_to_date",
                "is_compatible": True,
                "risk_level": "low",
                "reason": "La dependencia se encuentra en una versión moderna, estable y compatible.",
                "upgrade_command": cmd,
            }

        cur_sem = parse_semver(clean_raw_ver)
        rec_sem = parse_semver(rec_ver)

        if cur_sem[0] < rec_sem[0]:
            return {
                "recommended_version": rec_ver,
                "status": "major_update",
                "is_compatible": False,
                "risk_level": "high",
                "reason": f"Salto de versión mayor disponible (v{cur_sem[0]} → v{rec_sem[0]}). Puede requerir revisión de breaking changes.",
                "upgrade_command": cmd,
            }
        elif cur_sem[1] < rec_sem[1]:
            return {
                "recommended_version": rec_ver,
                "status": "minor_update",
                "is_compatible": True,
                "risk_level": "medium",
                "reason": f"Actualización menor disponible (v{clean_raw_ver} → v{rec_ver}) con nuevas funciones y optimizaciones.",
                "upgrade_command": cmd,
            }
        else:
            return {
                "recommended_version": rec_ver,
                "status": "patch_update",
                "is_compatible": True,
                "risk_level": "low",
                "reason": f"Parche de estabilidad disponible (v{clean_raw_ver} → v{rec_ver}) con correcciones de errores.",
                "upgrade_command": cmd,
            }

    def _evaluate_generic_package(
        self,
        pkg_name: str,
        clean_raw_ver: str,
        is_unpinned: bool,
        ecosystem: str,
    ) -> Dict[str, Any]:
        """Evalúa un paquete no catalogado expresamente mediante heurísticas SemVer."""
        up_cmd = f"pip install --upgrade {pkg_name}" if ecosystem == "python" else f"npm update {pkg_name}"
        if is_unpinned:
            return {
                "recommended_version": "fijar versión",
                "status": "patch_update",
                "is_compatible": True,
                "risk_level": "medium",
                "reason": "Versión sin fijar en el manifiesto. Se aconseja especificar versión exacta o rango acotado.",
                "upgrade_command": up_cmd,
            }

        cur_sem = parse_semver(clean_raw_ver)
        if cur_sem == (0, 0, 0):
            return {
                "recommended_version": "1.0.0",
                "status": "up_to_date",
                "is_compatible": True,
                "risk_level": "low",
                "reason": "Versión activa sin advertencias conocidas.",
                "upgrade_command": up_cmd,
            }

        if cur_sem[0] == 0 and cur_sem[1] < 5:
            rec_v = f"0.{cur_sem[1] + 1}.0"
            rec_cmd = f"pip install --upgrade {pkg_name}=={rec_v}" if ecosystem == "python" else f"npm install {pkg_name}@{rec_v}"
            return {
                "recommended_version": rec_v,
                "status": "minor_update",
                "is_compatible": True,
                "risk_level": "medium",
                "reason": f"Paquete en fase inicial pre-1.0 (v{clean_raw_ver}). Se sugiere actualizar a versión reciente {rec_v}.",
                "upgrade_command": rec_cmd,
            }

        return {
            "recommended_version": f"{cur_sem[0]}.{cur_sem[1]}.{cur_sem[2]}",
            "status": "up_to_date",
            "is_compatible": True,
            "risk_level": "low",
            "reason": "Dependencia en versión funcional y estable.",
            "upgrade_command": up_cmd,
        }

    def _evaluate_package(self, pkg_name: str, current_ver: str, ecosystem: str) -> Dict[str, Any]:
        """Evalúa un paquete individual contra el catálogo o heurísticas semver."""
        info = self.catalog.get(pkg_name.lower())
        clean_raw_ver = str(current_ver).strip() if current_ver else ""
        is_unpinned = clean_raw_ver in ("", "unspecified", "*", "latest", "any")

        if info:
            return self._evaluate_catalog_package(info, pkg_name, clean_raw_ver, is_unpinned, ecosystem)
        return self._evaluate_generic_package(pkg_name, clean_raw_ver, is_unpinned, ecosystem)

    # ── Parsers de Manifiestos ─────────────────────────────────────────

    def _get_rel_source(self, file_path: Path, base_path: Optional[Path] = None) -> str:
        if base_path:
            try:
                return str(file_path.relative_to(base_path)).replace("\\", "/")
            except ValueError:
                pass
        return file_path.name

    def _parse_requirements_txt(self, file_path: Path, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        results = []
        source_name = self._get_rel_source(file_path, base_path)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for raw_line in f:
                    line = raw_line.split("#")[0].strip()
                    if not line or line.startswith("-") or line.startswith("@"):
                        continue
                    match = re.match(r"^([a-zA-Z0-9_\-\.]+)(?:\s*([=><~!^]+)\s*([\d\w\.\-]+))?", line)
                    if match:
                        name = match.group(1).strip()
                        raw_v = match.group(3) or "unspecified"
                        clean_v = re.sub(r"[\^~>=<]", "", raw_v).strip() if raw_v != "unspecified" else "unspecified"
                        results.append({
                            "package_name": name,
                            "current_version": clean_v or "unspecified",
                            "ecosystem": "python",
                            "source_file": source_name,
                        })
        except Exception:
            pass
        return results

    def _parse_package_json(self, file_path: Path, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        results = []
        source_name = self._get_rel_source(file_path, base_path)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
                all_npm_deps = {}
                for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
                    all_npm_deps.update(data.get(key) or {})

                for name, ver in all_npm_deps.items():
                    clean_ver = re.sub(r"[\^~>=<]", "", str(ver)).strip()
                    results.append({
                        "package_name": name,
                        "current_version": clean_ver or str(ver),
                        "ecosystem": "npm",
                        "source_file": source_name,
                    })
        except Exception:
            pass
        return results

    def _parse_pyproject_toml(self, file_path: Path, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        results = []
        source_name = self._get_rel_source(file_path, base_path)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                in_dependencies = False
                for raw_line in f:
                    line = raw_line.split("#")[0].strip()
                    if line.startswith("[") and ("dependencies" in line.lower() or "project" in line.lower()):
                        in_dependencies = True
                        continue
                    if line.startswith("[") and in_dependencies:
                        in_dependencies = False
                        continue
                    if in_dependencies and "=" in line:
                        parts = line.split("=", 1)
                        name = parts[0].strip().strip('"\'')
                        ver_raw = parts[1].strip().strip('"\'')
                        clean_ver = re.sub(r"[\^~>=<]", "", ver_raw).strip()
                        if name:
                            results.append({
                                "package_name": name,
                                "current_version": clean_ver or "unspecified",
                                "ecosystem": "python",
                                "source_file": source_name,
                            })
        except Exception:
            pass
        return results

    def _parse_pipfile(self, file_path: Path, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        results = []
        source_name = self._get_rel_source(file_path, base_path)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                in_packages = False
                for raw_line in f:
                    line = raw_line.split("#")[0].strip()
                    if line in ("[packages]", "[dev-packages]"):
                        in_packages = True
                        continue
                    elif line.startswith("["):
                        in_packages = False
                        continue
                    if in_packages and "=" in line:
                        parts = line.split("=", 1)
                        name = parts[0].strip().strip('"\'')
                        ver_raw = parts[1].strip().strip('"\'')
                        clean_ver = re.sub(r"[\^~>=<*]", "", ver_raw).strip()
                        if name:
                            results.append({
                                "package_name": name,
                                "current_version": clean_ver or "unspecified",
                                "ecosystem": "python",
                                "source_file": source_name,
                            })
        except Exception:
            pass
        return results

    def _parse_pom_xml(self, file_path: Path, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        results = []
        source_name = self._get_rel_source(file_path, base_path)
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            ns = {"m": root.tag.split("}")[0].strip("{")} if "}" in root.tag else {}
            prefix = "m:" if ns else ""
            
            for dep in root.findall(f".//{prefix}dependency", ns):
                art_elem = dep.find(f"{prefix}artifactId", ns)
                ver_elem = dep.find(f"{prefix}version", ns)
                if art_elem is not None and art_elem.text:
                    results.append({
                        "package_name": art_elem.text.strip(),
                        "current_version": ver_elem.text.strip() if ver_elem is not None and ver_elem.text else "unspecified",
                        "ecosystem": "maven",
                        "source_file": source_name,
                    })
        except Exception:
            pass
        return results

    def _parse_go_mod(self, file_path: Path, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        results = []
        source_name = self._get_rel_source(file_path, base_path)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                in_require = False
                for line in f:
                    line = line.strip()
                    if line.startswith("require ("):
                        in_require = True
                        continue
                    elif line == ")" and in_require:
                        in_require = False
                        continue
                    if (in_require or line.startswith("require ")) and line and not line.startswith("//"):
                        parts = line.replace("require ", "").strip().split()
                        if len(parts) >= 2:
                            name = parts[0]
                            ver = parts[1]
                            results.append({
                                "package_name": name,
                                "current_version": ver,
                                "ecosystem": "go",
                                "source_file": source_name,
                            })
        except Exception:
            pass
        return results

    def _parse_cargo_toml(self, file_path: Path, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        results = []
        source_name = self._get_rel_source(file_path, base_path)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                in_deps = False
                for raw_line in f:
                    line = raw_line.split("#")[0].strip()
                    if line in ("[dependencies]", "[dev-dependencies]"):
                        in_deps = True
                        continue
                    elif line.startswith("["):
                        in_deps = False
                        continue
                    if in_deps and "=" in line:
                        parts = line.split("=", 1)
                        name = parts[0].strip()
                        ver = parts[1].strip().strip('"\'')
                        results.append({
                            "package_name": name,
                            "current_version": ver,
                            "ecosystem": "cargo",
                            "source_file": source_name,
                        })
        except Exception:
            pass
        return results

    def _is_ignored_path(self, path: Path, base_path: Optional[Path] = None) -> bool:
        ignored = {
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
            ".pytest_cache",
            ".gemini",
            ".agents",
            "coverage",
            "temp_repos",
        }
        if base_path:
            try:
                rel = path.relative_to(base_path)
                return any(part in ignored for part in rel.parts)
            except ValueError:
                pass
        return any(part in ignored for part in path.parts)

import json
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import init_db
from app.analyzers.dependency_version_analyzer import (
    DependencyVersionAnalyzer,
    parse_semver,
    compare_versions,
)
from app.analyzers.manager import AnalyzerManager

client = TestClient(app)


def test_semver_parsing_and_comparison():
    assert parse_semver("1.2.3") == (1, 2, 3)
    assert parse_semver("^18.2.0") == (18, 2, 0)
    assert parse_semver("~=0.110.5") == (0, 110, 5)
    assert parse_semver("v2.10.4-beta") == (2, 10, 4)

    assert compare_versions("2.0.0", "1.9.9") == 1
    assert compare_versions("1.0.0", "2.0.0") == -1
    assert compare_versions("1.2.3", "1.2.3") == 0
    assert compare_versions("0.115.6", "0.100.0") == 1


def test_parse_requirements_txt_and_evaluate():
    analyzer = DependencyVersionAnalyzer()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        req_file = tmp_path / "requirements.txt"
        req_file.write_text(
            "fastapi==0.100.0\n"
            "pydantic==1.10.0\n"
            "pytest>=8.0.0\n"
            "reportlab~=4.2.0\n",
            encoding="utf-8"
        )

        res = analyzer.analyze_dependencies(tmp_path)
        assert res["total_dependencies"] == 4
        assert "python" in res["ecosystems"]

        # Check pydantic is detected as incompatible (condition < 2.0.0)
        pydantic_entry = next((d for d in res["dependencies"] if d["package_name"].lower() == "pydantic"), None)
        assert pydantic_entry is not None
        assert pydantic_entry["status"] == "incompatible"
        assert pydantic_entry["is_compatible"] is False
        assert pydantic_entry["recommended_version"] == "2.10.4"
        assert "pip install" in pydantic_entry["upgrade_command"]

        # Check fastapi is detected as minor/patch update
        fastapi_entry = next((d for d in res["dependencies"] if d["package_name"].lower() == "fastapi"), None)
        assert fastapi_entry is not None
        assert fastapi_entry["status"] in ("minor_update", "major_update")
        assert fastapi_entry["recommended_version"] == "0.115.6"

        assert res["score"] < 100.0


def test_parse_package_json_and_evaluate():
    analyzer = DependencyVersionAnalyzer()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        pkg_file = tmp_path / "package.json"
        pkg_content = {
            "name": "test-app",
            "dependencies": {
                "react": "16.8.0",
                "lodash": "4.17.21"
            },
            "devDependencies": {
                "vite": "5.4.11",
                "typescript": "5.7.2"
            }
        }
        pkg_file.write_text(json.dumps(pkg_content), encoding="utf-8")

        res = analyzer.analyze_dependencies(tmp_path)
        assert res["total_dependencies"] == 4
        assert "npm" in res["ecosystems"]

        # React 16.8 is incompatible (< 18.0.0)
        react_entry = next((d for d in res["dependencies"] if d["package_name"] == "react"), None)
        assert react_entry is not None
        assert react_entry["status"] == "incompatible"
        assert react_entry["recommended_version"] == "18.3.1"
        assert "npm install react@^18.3.1" in react_entry["upgrade_command"]

        # Lodash is up to date
        lodash_entry = next((d for d in res["dependencies"] if d["package_name"] == "lodash"), None)
        assert lodash_entry is not None
        assert lodash_entry["status"] == "up_to_date"


def test_manager_includes_dependency_analysis():
    manager = AnalyzerManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create a python source file
        py_file = tmp_path / "main.py"
        py_file.write_text("def hello():\n    return 'world'\n", encoding="utf-8")

        # Create requirements.txt
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("fastapi==0.115.6\npytest==8.3.4\n", encoding="utf-8")

        results = manager.analyze_repository(tmp_path)
        assert "dependencies" in results
        assert "dependency_score" in results["summary_metrics"]
        assert results["summary_metrics"]["total_dependencies"] == 2
        assert results["dependencies"]["score"] == 100.0


def test_dependencies_api_endpoint():
    init_db()

    # 1. Crear repo
    create_res = client.post("/api/v1/repos/", json={"url": "https://github.com/test-org/dep-test-repo", "name": "dep-test-repo"})
    repo_id = create_res.json()["id"]

    # 2. Trigger analysis
    client.post("/api/v1/repos/analyze", json={"repo_url": "https://github.com/test-org/dep-test-repo"})

    # 3. Consultar dependencias
    dep_res = client.get(f"/api/v1/repos/{repo_id}/dependencies")
    assert dep_res.status_code == 200
    data = dep_res.json()
    assert "score" in data
    assert "dependencies" in data

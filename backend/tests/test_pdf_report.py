from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db
from app.services.pdf_report import PDFReportGenerator

client = TestClient(app)


def test_pdf_generator_creates_valid_pdf():
    generator = PDFReportGenerator()
    pdf_bytes = generator.generate(
        repo_name="demo-orders",
        repo_url="https://github.com/org/demo-orders",
        branch="main",
        commit_sha="a1b2c3d4e5f6",
        global_score=78.5,
        metrics=[
            {"criterio": "maintainability_index", "valor": 72.0},
            {"criterio": "cyclomatic_complexity", "valor": 85.0},
            {"criterio": "solid_principles", "valor": 65.0},
            {"criterio": "code_duplication", "valor": 90.0},
            {"criterio": "dependency_version_control", "valor": 80.0},
        ],
        findings=[
            {
                "file_path": "src/orders/service.py",
                "function_name": "process_order",
                "line_number": 45,
                "criterio": "solid_principles",
                "severidad": "high",
                "explicacion": "Mezcla persistencia con lógica de negocio violando SRP.",
                "rag_source": "solid-principles.md#single-responsibility",
                "sugerencia": "Extraer OrderRepository como colaborador separado.",
            }
        ],
        architecture={
            "resumen": "Módulos analizados: 8. Ciclos: 0",
            "has_circular_dependencies": False,
            "ciclos_detectados": [],
        },
        generated_docs=[
            {"titulo": "Resumen de Arquitectura: demo-orders", "path": "module-docs/demo-orders.md", "tipo": "summary"}
        ],
        dependencies={
            "score": 80.0,
            "total_dependencies": 2,
            "up_to_date_count": 1,
            "outdated_count": 1,
            "incompatible_count": 0,
            "dependencies": [
                {
                    "package_name": "fastapi",
                    "ecosystem": "python",
                    "source_file": "requirements.txt",
                    "current_version": "0.100.0",
                    "recommended_version": "0.115.6",
                    "status": "minor_update",
                    "reason": "Actualización menor disponible",
                    "upgrade_command": "pip install --upgrade fastapi==0.115.6",
                }
            ],
        },
    )

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")


def test_pdf_endpoint_download():
    init_db()

    # 1. Crear repo
    create_res = client.post("/api/v1/repos/", json={"url": "https://github.com/test-org/pdf-test-repo", "name": "pdf-test-repo"})
    repo_id = create_res.json()["id"]

    # 2. Trigger analysis
    client.post("/api/v1/repos/analyze", json={"repo_url": "https://github.com/test-org/pdf-test-repo"})

    # 3. Descargar PDF
    pdf_res = client.get(f"/api/v1/repos/{repo_id}/report/pdf")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert "attachment" in pdf_res.headers["content-disposition"]
    assert pdf_res.content.startswith(b"%PDF")

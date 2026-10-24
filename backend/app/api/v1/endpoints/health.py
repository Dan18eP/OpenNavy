from pathlib import Path
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings

router = APIRouter()


@router.get("/health", summary="Health Check & System Status")
def health_check(db: Session = Depends(get_db)):
    # 1. Probar conexión a Base de Datos
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    # 2. Verificar existencia de la Base de Conocimiento y sus subdirectorios
    kb_path = Path(settings.KNOWLEDGE_BASE_PATH)
    kb_counts = {
        "criteria_documents": 0,
        "canonical_documents": 0,
        "team_standards_documents": 0,
        "module_docs_documents": 0,
        "adrs_documents": 0,
    }
    if kb_path.exists():
        for sub_dir, key in [
            ("criteria", "criteria_documents"),
            ("canonical", "canonical_documents"),
            ("team-standards", "team_standards_documents"),
            ("module-docs", "module_docs_documents"),
            ("adrs", "adrs_documents"),
        ]:
            target = kb_path / sub_dir
            if target.exists():
                kb_counts[key] = len(list(target.glob("*.md")))

    # 3. Detectar modelos locales de Ollama disponibles
    models_info = []
    try:
        import ollama
        client = ollama.Client(host=settings.OLLAMA_BASE_URL)
        resp = client.list()
        raw_models = getattr(resp, "models", [])
        for m in raw_models:
            if isinstance(m, dict):
                r_name = m.get("model") or m.get("name") or ""
                r_size = m.get("size") or 0
            else:
                r_name = getattr(m, "model", "") or getattr(m, "name", "")
                r_size = getattr(m, "size", 0)
            models_info.append({
                "name": r_name,
                "size_mb": round(r_size / (1024 * 1024), 1) if r_size else 0,
                "is_active": (r_name == settings.OLLAMA_MODEL) or r_name.startswith(settings.OLLAMA_MODEL)
            })
    except Exception:
        pass

    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": db_status,
        "active_model": settings.OLLAMA_MODEL,
        "local_tier": settings.PRAXIA_LOCAL_TIER,
        "installed_models": models_info,
        "knowledge_base": {
            "path": str(kb_path),
            **kb_counts,
        },
        "criteria_weights": settings.CRITERIA_WEIGHTS,
    }

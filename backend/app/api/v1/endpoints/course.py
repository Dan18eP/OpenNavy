import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import settings
from app.core.database import get_db
from app.models.entities import Repo
from app.api.v1.endpoints.sonar import sonar_hub
from app.core.ollama_client import ChatOllamaLocal
from app.services.anti_drift_service import anti_drift_service

logger = logging.getLogger(__name__)

router = APIRouter()


class CoursePlotRequest(BaseModel):
    repo_id: str = Field(..., description="ID del repositorio analizado o ruta local")
    mission: str = Field(..., description="Descripcion del issue, bounty o requerimiento")
    image_base64: Optional[str] = Field(None, description="Captura de pantalla o traza de error en Base64 (Multimodal)")
    officer_name: Optional[str] = Field("Commander", description="Nombre del oficial que solicita el rumbo")


class WaypointItem(BaseModel):
    file: str
    lines: List[int]
    reason: str


class BlastRadiusInfo(BaseModel):
    severity: str
    total_affected_count: int
    direct_dependents: List[str]
    indirect_dependents: List[str]


class CoursePlotResponse(BaseModel):
    mission: str
    thought_process: str
    waypoints: List[WaypointItem]
    reef_warnings: List[str]
    action_steps: List[str]
    pr_template: str
    drift_risk: Optional[str] = "LOW"
    blast_radius: Optional[Dict[str, Any]] = None
    adr_recommendation: Optional[str] = None


@router.post("/plot", response_model=CoursePlotResponse, summary="Trazar Rumbo de Navegacion (Course Plotter)")
async def plot_course(
    payload: CoursePlotRequest,
    db: Session = Depends(get_db),
):
    """
    Traza el rumbo de implementacion utilizando Google Gemma 4 sobre el AST local y Tarjan.
    Recibe texto o imagen multimodal, calcula los waypoints y difunde el blueprint por el Sonar LAN.
    Aplica el Motor Anti Code Drift para alertar sobre radio de impacto y violacion de capas.
    """
    repo = db.query(Repo).filter_by(id=payload.repo_id).first()
    repo_name = repo.name if repo else "OpenSource-Repo"

    # Resolver ruta fisica del repositorio para escaneo de topografia real
    workspace_root = Path(".").resolve()
    repo_dir = None
    if repo and Path(repo.url).exists():
        repo_dir = str(Path(repo.url).resolve())
    elif (workspace_root / "backend").exists() or (workspace_root / "frontend").exists():
        repo_dir = str(workspace_root)

    logger.info(f"[CoursePlotter] Trazando rumbo para mision: '{payload.mission}' en repo: '{repo_name}'")

    # 1. Obtener topografia AST real y arrecifes de Tarjan
    topography = {}
    if repo_dir:
        topography = anti_drift_service.get_repo_ast_topography(repo_dir, max_files=40)

    available_files = topography.get("files", [])[:35]
    scc_cycles = topography.get("scc_cycles", [])
    symbols_sample = topography.get("symbols", {})

    # Formatear contexto topologico para Gemma 4
    files_context = "\n".join(f"- {f}" for f in available_files) if available_files else "src/core.py\nsrc/api.py"
    reefs_context = ""
    if scc_cycles:
        reefs_list = [" -> ".join(c.get("cycle", [])) for c in scc_cycles[:3]]
        reefs_context = "\n[ARRECIFES DE CODIGO DETECTADOS POR TARJAN - PRECAUCION DE ACOPLAMIENTO]:\n" + "\n".join(f"* {r}" for r in reefs_list)

    # 2. Prompt estructurado para Google Gemma 4
    system_prompt = (
        "Eres el Almirante de OpenNavy (The Admiralty AI), un arquitecto de software supremo especializado "
        "en navegacion y contribucion soberana en repositorios open source.\n"
        "Tu mision es transformar el requerimiento o bug en un 'Plan de Vuelo Nautico' hiperpreciso.\n"
        "INSTRUCCIONES ESTRICTAS:\n"
        "1. Selecciona waypoints UNICAMENTE de los archivos reales listados en la topografia.\n"
        "2. Identifica las lineas aproximadas y la razon tecnica.\n"
        "3. Si un archivo objetivo se encuentra en los arrecifes de Tarjan, senala una advertencia de arrecife.\n"
        "4. Responde OBLIGATORIAMENTE en formato JSON valido con esta estructura exacta:\n"
        "{\n"
        '  "thought_process": "Explicacion de tu razonamiento arquitectonico...",\n'
        '  "waypoints": [\n'
        '    {"file": "ruta/al/archivo_real.py", "lines": [10, 35], "reason": "Por que modificar este archivo"}\n'
        '  ],\n'
        '  "reef_warnings": ["Advertencias de acoplamiento o dependencias circulares..."],\n'
        '  "action_steps": ["Paso 1...", "Paso 2...", "Paso 3..."],\n'
        '  "pr_template": "### Cambios realizados\\n..."\n'
        "}"
    )

    user_prompt = (
        f"Repositorio: {repo_name}\n"
        f"Mision / Issue: {payload.mission}\n\n"
        f"[TOPOGRAFIA REAL DE ARCHIVOS DEL REPOSITORIO]:\n{files_context}\n"
        f"{reefs_context}"
    )

    try:
        # Preparar mensajes para Ollama (con soporte multimodal si hay imagen)
        messages = [SystemMessage(content=system_prompt)]
        
        # Limpiar base64 si incluye encabezado data:image/...;base64,
        raw_b64 = None
        if payload.image_base64:
            raw_b64 = payload.image_base64
            if "," in raw_b64:
                raw_b64 = raw_b64.split(",", 1)[1]
            user_prompt += "\n\n[IMAGEN ADJUNTA]: Analiza la captura del error o interfaz adjunta para identificar el componente visual o traza afectada."
            messages.append(HumanMessage(content=user_prompt, additional_kwargs={"images": [raw_b64]}))
        else:
            messages.append(HumanMessage(content=user_prompt))

        # Invocar a Gemma 4 en Ollama
        llm = ChatOllamaLocal(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0.1,
            timeout=45.0,
        )

        raw_response = await llm.ainvoke(messages)
        content = raw_response.content if hasattr(raw_response, "content") else str(raw_response)

        # Parsear JSON de Gemma 4
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        parsed = json.loads(content)

        extracted_waypoints = [
            WaypointItem(
                file=wp.get("file", available_files[0] if available_files else "src/core.py"),
                lines=wp.get("lines", [1, 20]),
                reason=wp.get("reason", "Componente clave de la mision"),
            )
            for wp in parsed.get("waypoints", [])
        ]

        # 3. Aplicar Motor Anti Code Drift sobre los waypoints de Gemma 4
        raw_wp_dicts = [wp.dict() for wp in extracted_waypoints]
        drift_analysis = anti_drift_service.evaluate_course_drift(repo_name, raw_wp_dicts, repo_dir)

        # Combinar advertencias de arrecifes
        combined_reefs = parsed.get("reef_warnings", [])
        for rw in drift_analysis.get("reef_warnings", []):
            if rw not in combined_reefs and "No se detectaron" not in rw:
                combined_reefs.append(rw)
        if not combined_reefs:
            combined_reefs = ["No se detectaron arrecifes criticos."]

        response_data = CoursePlotResponse(
            mission=payload.mission,
            thought_process=parsed.get("thought_process", "Analisis topologico completado por el Almirante Gemma 4."),
            waypoints=extracted_waypoints,
            reef_warnings=combined_reefs,
            action_steps=parsed.get("action_steps", ["1. Inspeccionar modulos", "2. Aplicar cambio", "3. Ejecutar tests"]),
            pr_template=parsed.get("pr_template", "### Pull Request generado por OpenNavy"),
            drift_risk=drift_analysis.get("drift_risk", "LOW"),
            blast_radius=drift_analysis.get("blast_radius"),
            adr_recommendation=drift_analysis.get("adr_recommendation"),
        )

        # 4. Difundir el nuevo Blueprint enriquecido por el Sonar de Flota
        await sonar_hub.broadcast_course_plotted(
            officer_name=payload.officer_name or "Commander",
            mission=payload.mission,
            waypoints=[wp.dict() for wp in response_data.waypoints],
        )

        return response_data

    except Exception as e:
        logger.error(f"[CoursePlotter] Error al trazar rumbo con Gemma 4: {e}")
        # Fallback determinista inteligente vinculado a la topografia real del repositorio
        mission_words = [w.lower() for w in re.findall(r'\b\w{3,}\b', payload.mission)]
        scored_files = []
        for f in available_files:
            f_lower = f.lower()
            score = sum(2 for w in mission_words if w in f_lower)
            file_symbols = symbols_sample.get(f, [])
            for sym in file_symbols:
                sym_name = sym.get("name", "").lower() if isinstance(sym, dict) else str(sym).lower()
                if any(w in sym_name for w in mission_words):
                    score += 3
            scored_files.append((score, f))

        scored_files.sort(key=lambda x: x[0], reverse=True)
        relevant_candidates = [f for score, f in scored_files if score > 0]

        primary_file = relevant_candidates[0] if relevant_candidates else (available_files[0] if available_files else "backend/app/core/config.py")
        secondary_file = (
            relevant_candidates[1] if len(relevant_candidates) > 1
            else (available_files[1] if len(available_files) > 1 and available_files[1] != primary_file else "backend/app/main.py")
        )

        fallback_waypoints = [
            WaypointItem(file=primary_file, lines=[15, 35], reason="Modulo relevante identificado por coincidencia topologica AST"),
            WaypointItem(file=secondary_file, lines=[20, 45], reason="Modulo dependiente con acoplamiento de integracion"),
        ]

        raw_wp_dicts = [wp.dict() for wp in fallback_waypoints]
        drift_analysis = anti_drift_service.evaluate_course_drift(repo_name, raw_wp_dicts, repo_dir)

        fallback_response = CoursePlotResponse(
            mission=payload.mission,
            thought_process=f"Analisis sintactico y topologico completado en modo determinista local sobre {repo_name}.",
            waypoints=fallback_waypoints,
            reef_warnings=drift_analysis.get("reef_warnings", ["No se detectaron arrecifes criticos."]),
            action_steps=[
                f"1. Inspeccionar definicion en `{primary_file}`",
                f"2. Validar integracion en `{secondary_file}`",
                "3. Ejecutar tests unitarios",
            ],
            pr_template="### Pull Request (OpenNavy Course Plotter)\n- Implementa solucion modular\n- Preserva limites de arquitectura hexagonal\n",
            drift_risk=drift_analysis.get("drift_risk", "LOW"),
            blast_radius=drift_analysis.get("blast_radius"),
            adr_recommendation=drift_analysis.get("adr_recommendation"),
        )

        await sonar_hub.broadcast_course_plotted(
            officer_name=payload.officer_name or "Commander",
            mission=payload.mission,
            waypoints=[wp.dict() for wp in fallback_response.waypoints],
        )

        return fallback_response

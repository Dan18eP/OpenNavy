from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.entities import AIOpportunityAssessment
from app.schemas.api import AssessmentData, AssessmentVerdictResponse
from app.services.ai_assessment import (
    decide_assessment,
    parse_assessment_xlsx_bytes,
)

router = APIRouter()


@router.post("/evaluate", response_model=AssessmentVerdictResponse, summary="Evalúa un levantamiento de información JSON")
def evaluate_assessment_json(
    data: AssessmentData,
    db: Session = Depends(get_db),
):
    """
    Evalúa las respuestas de los 6 pasos del AI Opportunity Assessment y calcula el veredicto determinístico.
    Persiste el resultado en la base de datos de Praxia.
    """
    dict_data = data.model_dump()
    verdict = decide_assessment(dict_data)

    assessment_record = AIOpportunityAssessment(
        project_name=data.proyecto or "Proyecto sin nombre",
        team_name=data.equipo,
        problem_statement=data.problema or "No especificado",
        current_situation=data.situacion,
        expected_result=data.resultado or "No especificado",
        value_dimension=data.dimension,
        metric_name=data.metrica,
        target_goal=data.meta,
        cap_reglas=data.cap_reglas or "Por validar",
        cap_prediccion=data.cap_prediccion or "Por validar",
        cap_comprension=data.cap_comprension or "Por validar",
        cap_generacion=data.cap_generacion or "Por validar",
        cap_consulta=data.cap_consulta or "Por validar",
        cap_accion=data.cap_accion or "Por validar",
        cap_autonomia=data.cap_autonomia or "Por validar",
        simplicity_sufficient=data.suficiencia or "Por validar",
        simplest_solution=data.solucion_simple,
        data_needed=data.info_necesaria,
        data_exists=data.info_existe or "Por validar",
        data_accessible=data.info_accesible or "Por validar",
        data_reliable=data.info_confiable or "Por validar",
        data_sensitive=data.info_sensible or "Por validar",
        autonomy_level=data.autonomia_nivel or "Recomienda",
        initial_risk_description=data.riesgo_desc,
        initial_risk_level=data.riesgo_nivel or "Medio",
        hypothesis=data.hipotesis,
        verdict_key=verdict["key"],
        verdict_title=verdict["title"],
        verdict_lead=verdict["lead"],
        verdict_detail=verdict.get("detail"),
        verdict_reasons=verdict.get("why", []),
    )
    db.add(assessment_record)
    db.commit()
    db.refresh(assessment_record)

    return AssessmentVerdictResponse(
        id=assessment_record.id,
        key=verdict["key"],
        tag=verdict.get("tag", "Resultado del assessment"),
        title=verdict["title"],
        lead=verdict["lead"],
        detail=verdict.get("detail"),
        why=verdict.get("why", []),
        raw_data=dict_data,
        created_at=assessment_record.created_at,
    )


@router.post("/upload", response_model=AssessmentVerdictResponse, summary="Carga y evalúa archivo Excel (Levantamiento de Información.xlsx)")
async def upload_assessment_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Recibe un archivo XLSX con la hoja '01_Assessment', extrae los 6 pasos y genera el veredicto del dashboard.
    """
    if not file.filename.lower().endswith((".xlsx", ".xlsm")):
        raise HTTPException(status_code=400, detail="El archivo debe ser un libro Excel (.xlsx)")

    content = await file.read()
    try:
        raw_dict = parse_assessment_xlsx_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"No se pudo parsear el archivo Excel: {str(e)}")

    if not raw_dict:
        raise HTTPException(status_code=400, detail="No se encontraron datos válidos en la hoja '01_Assessment'")

    verdict = decide_assessment(raw_dict)

    assessment_record = AIOpportunityAssessment(
        project_name=raw_dict.get("proyecto", file.filename),
        team_name=raw_dict.get("equipo"),
        problem_statement=raw_dict.get("problema", "No especificado"),
        current_situation=raw_dict.get("situacion"),
        expected_result=raw_dict.get("resultado", "No especificado"),
        value_dimension=raw_dict.get("dimension", "Tiempo"),
        metric_name=raw_dict.get("metrica"),
        target_goal=raw_dict.get("meta"),
        cap_reglas=raw_dict.get("cap_reglas", "Por validar"),
        cap_prediccion=raw_dict.get("cap_prediccion", "Por validar"),
        cap_comprension=raw_dict.get("cap_comprension", "Por validar"),
        cap_generacion=raw_dict.get("cap_generacion", "Por validar"),
        cap_consulta=raw_dict.get("cap_consulta", "Por validar"),
        cap_accion=raw_dict.get("cap_accion", "Por validar"),
        cap_autonomia=raw_dict.get("cap_autonomia", "Por validar"),
        simplicity_sufficient=raw_dict.get("suficiencia", "Por validar"),
        simplest_solution=raw_dict.get("solucion_simple"),
        data_needed=raw_dict.get("info_necesaria"),
        data_exists=raw_dict.get("info_existe", "Por validar"),
        data_accessible=raw_dict.get("info_accesible", "Por validar"),
        data_reliable=raw_dict.get("info_confiable", "Por validar"),
        data_sensitive=raw_dict.get("info_sensible", "Por validar"),
        autonomy_level=raw_dict.get("autonomia_nivel", "Recomienda"),
        initial_risk_description=raw_dict.get("riesgo_desc"),
        initial_risk_level=raw_dict.get("riesgo_nivel", "Medio"),
        hypothesis=raw_dict.get("hipotesis"),
        verdict_key=verdict["key"],
        verdict_title=verdict["title"],
        verdict_lead=verdict["lead"],
        verdict_detail=verdict.get("detail"),
        verdict_reasons=verdict.get("why", []),
    )
    db.add(assessment_record)
    db.commit()
    db.refresh(assessment_record)

    return AssessmentVerdictResponse(
        id=assessment_record.id,
        key=verdict["key"],
        tag=verdict.get("tag", "Resultado del assessment"),
        title=verdict["title"],
        lead=verdict["lead"],
        detail=verdict.get("detail"),
        why=verdict.get("why", []),
        raw_data=raw_dict,
        created_at=assessment_record.created_at,
    )


@router.get("/list", response_model=List[AssessmentVerdictResponse], summary="Historial de assessments evaluados")
def list_assessments(
    db: Session = Depends(get_db),
):
    """Retorna la lista de evaluaciones de oportunidad realizadas."""
    items = db.query(AIOpportunityAssessment).order_by(AIOpportunityAssessment.created_at.desc()).limit(20).all()
    results = []
    for item in items:
        results.append(AssessmentVerdictResponse(
            id=item.id,
            key=item.verdict_key,
            tag="Resultado del assessment",
            title=item.verdict_title,
            lead=item.verdict_lead,
            detail=item.verdict_detail,
            why=item.verdict_reasons or [],
            raw_data={
                "proyecto": item.project_name,
                "equipo": item.team_name,
                "problema": item.problem_statement,
                "situacion": item.current_situation,
                "resultado": item.expected_result,
                "dimension": item.value_dimension,
                "metrica": item.metric_name,
                "meta": item.target_goal,
                "cap_reglas": item.cap_reglas,
                "cap_prediccion": item.cap_prediccion,
                "cap_comprension": item.cap_comprension,
                "cap_generacion": item.cap_generacion,
                "cap_consulta": item.cap_consulta,
                "cap_accion": item.cap_accion,
                "cap_autonomia": item.cap_autonomia,
                "suficiencia": item.simplicity_sufficient,
                "solucion_simple": item.simplest_solution,
                "info_necesaria": item.data_needed,
                "info_existe": item.data_exists,
                "info_accesible": item.data_accessible,
                "info_confiable": item.data_reliable,
                "info_sensible": item.data_sensitive,
                "autonomia_nivel": item.autonomy_level,
                "riesgo_desc": item.initial_risk_description,
                "riesgo_nivel": item.initial_risk_level,
                "hipotesis": item.hypothesis,
            },
            created_at=item.created_at,
        ))
    return results

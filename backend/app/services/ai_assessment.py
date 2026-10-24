import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Tuple


CAPINFO = {
    "cap_reglas": ("Reglas", "Decisiones conocidas y determinísticas", False),
    "cap_prediccion": ("Predicción", "Clasificar, estimar o detectar patrones", True),
    "cap_comprension": ("Comprensión", "Interpretar información no estructurada", True),
    "cap_generacion": ("Generación", "Producir respuestas, análisis o contenido", True),
    "cap_consulta": ("Consulta", "Consultar información o sistemas externos", False),
    "cap_accion": ("Acción", "Ejecutar acciones sobre otros sistemas", False),
    "cap_autonomia": ("Autonomía", "Coordinar varios pasos hacia un objetivo", False)
}
CAPKEYS = list(CAPINFO.keys())


def is_blank(v: str) -> bool:
    if not v:
        return True
    return v.strip().lower() in ("", "por validar", "por_validar", "?", "none")


def decide_assessment(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejecuta el algoritmo de evaluación determinística de la Sesión 01 (idéntico a Dashboard.html).
    Retorna veredicto con key ('op', 'auto', 'val'), título, lead, detalle y lista de razones ('why').
    """
    def val(k: str) -> str:
        return str(data.get(k, "") or "").strip()

    suf = val("suficiencia") or val("simplicity_sufficient")
    reglas = val("cap_reglas")
    
    adv_si = [k for k in ("cap_prediccion", "cap_comprension", "cap_generacion") if val(k) == "Sí"]
    adv_names = [CAPINFO[k][0].lower() for k in adv_si]
    
    caps_unanswered = [k for k in CAPKEYS if is_blank(val(k))]
    key_unanswered = len(caps_unanswered) + (1 if is_blank(suf) else 0)
    
    why: List[str] = []

    if is_blank(suf) or len(caps_unanswered) == len(CAPKEYS) or key_unanswered >= 6:
        why.append(f"Faltan respuestas clave (marcadas «Por validar» o vacías): {key_unanswered} de 8 campos determinantes.")
        why.append("Sin ese perfil no es posible determinar la capacidad requerida.")
        return {
            "key": "val",
            "tag": "Resultado del assessment",
            "title": "POR VALIDAR",
            "lead": "No existe información suficiente para determinar la capacidad requerida.",
            "detail": "Completa el perfil de capacidades y la pregunta de suficiencia para obtener una conclusión.",
            "why": why,
        }

    if len(adv_si) >= 1 and (suf in ("No", "Parcialmente")):
        why.append(f"Se marcaron como necesarias capacidades de inteligencia: {', '.join(adv_names)}.")
        why.append(f"Una solución más simple se considera «{suf.lower()}» suficiente.")
        if reglas == "Sí":
            why.append("Aunque hay una base de reglas, no bastan por sí solas para el resultado esperado.")
        return {
            "key": "op",
            "tag": "Resultado del assessment",
            "title": "OPORTUNIDAD POTENCIAL DE IA",
            "lead": f"Se identifican necesidades de {', '.join(adv_names)}, mientras que una solución puramente basada en reglas no parece suficiente.",
            "detail": "Conviene explorar una capacidad de IA para este problema, definiendo el resultado medible y validando la información necesaria.",
            "why": why,
        }

    if len(adv_si) == 0 and (reglas == "Sí") and (suf in ("Sí", "Parcialmente")):
        why.append("El problema se describe con reglas conocidas (Reglas = Sí).")
        why.append("No se marcan necesidades de predicción, comprensión ni generación.")
        why.append(f"Una solución más simple se considera «{suf.lower()}» suficiente.")
        return {
            "key": "auto",
            "tag": "Resultado del assessment",
            "title": "AUTOMATIZACIÓN CONVENCIONAL PODRÍA SER SUFICIENTE",
            "lead": "El problema está principalmente determinado por reglas conocidas y no se evidencian necesidades de predicción, comprensión o generación.",
            "detail": "Antes de introducir IA, valida si una automatización o digitalización resuelve el problema con menor complejidad y control.",
            "why": why,
        }

    if len(adv_si) >= 1 and suf == "Sí":
        why.append(f"Se marcaron capacidades avanzadas ({', '.join(adv_names)}) pero también que una solución simple es suficiente.")
        why.append("Estas dos respuestas son contradictorias y conviene revisarlas.")
        return {
            "key": "val",
            "tag": "Resultado del assessment",
            "title": "POR VALIDAR",
            "lead": "Hay señales contradictorias: se necesitan capacidades avanzadas y, a la vez, una solución simple se considera suficiente.",
            "detail": "Revisa la coherencia entre el perfil de capacidades y la pregunta de suficiencia.",
            "why": why,
        }

    why.append("El perfil no encaja claramente en oportunidad de IA ni en automatización suficiente.")
    why.append(f"Revisa suficiencia ({suf or '—'}) y las capacidades marcadas.")
    return {
        "key": "val",
        "tag": "Resultado del assessment",
        "title": "POR VALIDAR",
        "lead": "No hay evidencia suficiente para inclinar la conclusión hacia IA o hacia automatización convencional.",
        "detail": "Ajusta el perfil de capacidades o la métrica de resultado y vuelve a cargar el archivo.",
        "why": why,
    }


def parse_assessment_xlsx_bytes(file_bytes: bytes) -> Dict[str, Any]:
    """
    Parsea directamente el contenido binario de un archivo Excel de levantamiento de información
    extrayendo las claves y respuestas de la hoja '01_Assessment'.
    """
    import io
    extracted_data: Dict[str, str] = {}

    with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
        # 1. Extraer shared strings
        shared_strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si"):
                text = "".join(t.text for t in si.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t") if t.text)
                shared_strings.append(text)

        # 2. Localizar hoja '01_Assessment'
        wb_root = ET.fromstring(z.read("xl/workbook.xml"))
        sheet_target = "xl/worksheets/sheet2.xml"  # default
        for sheet_elem in wb_root.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet"):
            name = sheet_elem.attrib.get("name", "")
            if "assessment" in name.lower():
                sheet_id = sheet_elem.attrib.get("sheetId", "2")
                sheet_target = f"xl/worksheets/sheet{sheet_id}.xml"
                break

        if sheet_target not in z.namelist():
            for name in z.namelist():
                if name.startswith("xl/worksheets/sheet"):
                    sheet_target = name
                    break

        s_root = ET.fromstring(z.read(sheet_target))
        for row in s_root.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row"):
            row_vals: List[str] = []
            for c in row.findall("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c"):
                v = c.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")
                t = c.attrib.get("t")
                val = ""
                if t == "inlineStr":
                    is_t = c.find(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")
                    val = is_t.text if is_t is not None else ""
                elif v is not None and v.text is not None:
                    try:
                        val = shared_strings[int(v.text)] if t == "s" else v.text
                    except (IndexError, ValueError):
                        val = v.text
                row_vals.append(val)

            if len(row_vals) >= 3:
                key = row_vals[0].strip()
                ans = row_vals[2].strip()
                if key and key != "SEC" and not key.startswith("PASO"):
                    extracted_data[key] = ans

    return extracted_data

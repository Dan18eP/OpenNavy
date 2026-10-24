import io
from datetime import datetime
from typing import Dict, Any, List, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)

CRITERIA_LABELS = {
    "maintainability_index": "Índice de Mantenibilidad (MI)",
    "cyclomatic_complexity": "Complejidad Ciclomática (McCabe)",
    "solid_principles": "Principios de Diseño SOLID",
    "code_duplication": "Duplicación de Código (Clones Sintácticos)",
    "test_coverage": "Cobertura de Pruebas Automatizadas",
    "architecture": "Directrices de Arquitectura y Modularidad",
    "clean_code": "Estándares Clean Code y Calidad",
    "dependency_version_control": "Control de Versiones y Dependencias",
    "defect_density": "Métricas de Proceso / DORA",
}


class NumberedCanvas(canvas.Canvas):
    """Canvas personalizado para calcular y dibujar la numeración dinámica 'Página X de Y' y encabezado/pie institucional."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count: int):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748b"))

        # Encabezado en páginas posteriores a la primera
        if self._pageNumber > 1:
            self.drawString(36, 762, "Praxia — Informe de Auditoría de Código y Plan de Mejora")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 754, 576, 754)

        # Pie de página en todas las páginas
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(36, 36, 576, 36)

        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(576, 24, page_str)
        self.drawString(36, 24, "Documento confidencial generado automáticamente por Praxia AI Audit Engine")
        self.restoreState()


def clean_xml(text: Any) -> str:
    """Sanitiza cadenas para evitar errores de parseo XML en ReportLab Paragraphs."""
    if text is None:
        return ""
    s = str(text)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    s = s.replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
    s = s.replace("&lt;code&gt;", "<code>").replace("&lt;/code&gt;", "</code>")
    s = s.replace("&lt;font", "<font").replace("&lt;/font&gt;", "</font>")
    s = s.replace("&quot;", '"')
    return s


class PDFReportGenerator:
    """Generador de Informes Ejecutivos de Auditoría de Código, Dependencias y Plan de Mejora en formato PDF."""

    def generate(
        self,
        repo_name: str,
        repo_url: str,
        branch: str,
        commit_sha: str,
        global_score: float,
        metrics: List[Dict[str, Any]],
        findings: List[Dict[str, Any]],
        architecture: Dict[str, Any],
        generated_docs: List[Dict[str, Any]],
        dependencies: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=40,
            bottomMargin=48,
        )

        styles = getSampleStyleSheet()

        # Paleta y Estilos Tipográficos
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#1e1b4b"),
        )
        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#475569"),
        )
        heading_h1 = ParagraphStyle(
            "SectionH1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#1e1b4b"),
            spaceBefore=14,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11.5,
            textColor=colors.HexColor("#1e293b"),
        )
        bold_body = ParagraphStyle(
            "BoldBody",
            parent=body_style,
            fontName="Helvetica-Bold",
        )
        code_style = ParagraphStyle(
            "CodeText",
            parent=styles["Normal"],
            fontName="Courier",
            fontSize=7,
            leading=9.5,
            textColor=colors.HexColor("#0f172a"),
        )

        elements = []

        # ── 1. ENCABEZADO INSTITUCIONAL ─────────────────────────────────
        elements.append(Paragraph("🛡️ Praxia — Informe Ejecutivo de Auditoría y Plan de Mejora", title_style))
        elements.append(Paragraph("Evaluación Cualitativa Asistida por RAG, Métricas Estáticas Universales y Auditoría de Dependencias", subtitle_style))
        elements.append(Spacer(1, 8))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#4f46e5"), spaceAfter=10))

        # ── 2. METADATOS DEL REPOSITORIO Y AUDITORÍA ───────────────────
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        meta_data = [
            [
                Paragraph("<b>Repositorio:</b>", bold_body),
                Paragraph(f"{clean_xml(repo_name)} (<font size='7' color='#4338ca'>{clean_xml(repo_url)}</font>)", body_style),
                Paragraph("<b>Fecha Auditoría:</b>", bold_body),
                Paragraph(now_str, body_style),
            ],
            [
                Paragraph("<b>Rama Analizada:</b>", bold_body),
                Paragraph(f"<code>{clean_xml(branch or 'main')}</code>", body_style),
                Paragraph("<b>Commit SHA:</b>", bold_body),
                Paragraph(f"<code>{clean_xml(commit_sha[:12] if commit_sha else 'HEAD')}</code>", code_style),
            ],
        ]
        meta_table = Table(meta_data, colWidths=[80, 220, 90, 150])
        meta_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("PADDING", (0, 0), (-1, -1), 4.5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 10))

        # ── 3. SCORE GLOBAL Y DIAGNÓSTICO EJECUTIVO CONTEXTUAL ───────────
        score_val = global_score if global_score is not None else 0.0
        if score_val >= 80:
            score_status = "SALUDABLE / CUMPLE ESTÁNDARES"
            status_color = colors.HexColor("#059669")
            score_bg = colors.HexColor("#ecfdf5")
            rec_diag = "El proyecto mantiene una estructura modular sólida y niveles de complejidad controlados. Se recomienda atender los hallazgos menores para mantener la deuda técnica en mínimos."
        elif score_val >= 60:
            score_status = "MODERADO / REQUIERE ATENCIÓN"
            status_color = colors.HexColor("#d97706")
            score_bg = colors.HexColor("#fffbeb")
            rec_diag = "Se observan focos de acoplamiento, dependencias pendientes de actualización o funciones con alta complejidad ciclomática que deben priorizarse en los próximos sprints."
        else:
            score_status = "CRÍTICO / ALTA DEUDA TÉCNICA"
            status_color = colors.HexColor("#e11d48")
            score_bg = colors.HexColor("#fff1f2")
            rec_diag = "Se detectaron violaciones arquitectónicas severas, incompatibilidades en librerías o acumulaciones críticas de complejidad que ponen en riesgo la estabilidad del sistema."

        crit_count = sum(1 for f in findings if f.get("severidad") == "critical")
        high_count = sum(1 for f in findings if f.get("severidad") == "high")
        warn_count = sum(1 for f in findings if f.get("severidad") == "warning")
        info_count = sum(1 for f in findings if f.get("severidad") == "info")

        summary_html = (
            f"<b>Diagnóstico Ejecutivo:</b> Calificación global de <b>{score_val:.1f} / 100</b> ({score_status}).<br/>"
            f"<b>Distribución de Riesgos:</b> <font color='#e11d48'><b>{crit_count} Críticos</b></font> | "
            f"<font color='#ea580c'><b>{high_count} Altos</b></font> | "
            f"<font color='#d97706'><b>{warn_count} Medios</b></font> | "
            f"<font color='#2563eb'><b>{info_count} Informativos</b></font> (Total: <b>{len(findings)}</b> hallazgos).<br/>"
            f"<b>Evaluación Técnica:</b> {rec_diag}"
        )

        score_box_data = [
            [
                Paragraph(f"<font size='24' color='{status_color.hexval()}'><b>{score_val:.1f}</b></font><br/><font size='7.5' color='#64748b'>/ 100 PUNTOS</font>", ParagraphStyle("ScoreVal", alignment=1)),
                Paragraph(summary_html, body_style),
            ]
        ]
        score_table = Table(score_box_data, colWidths=[120, 420])
        score_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), score_bg),
            ("BOX", (0, 0), (-1, -1), 1.5, status_color),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING", (0, 0), (-1, -1), 7),
        ]))
        elements.append(score_table)
        elements.append(Spacer(1, 12))

        # ── 4. DESGLOSE TÉCNICO DE LOS 8 CRITERIOS DE CALIDAD ────────────
        elements.append(Paragraph("1. Desglose y Evaluación de los Criterios de Calidad", heading_h1))
        
        metrics_rows = [
            [
                Paragraph("<b>Criterio de Evaluación</b>", bold_body),
                Paragraph("<b>Puntaje</b>", bold_body),
                Paragraph("<b>Umbral Objetivo</b>", bold_body),
                Paragraph("<b>Diagnóstico de Estado</b>", bold_body),
            ]
        ]

        metrics_map = {m.get("criterio"): m.get("valor", 75.0) for m in metrics}
        for crit_key, label in CRITERIA_LABELS.items():
            val = float(metrics_map.get(crit_key, 75.0))
            if val >= 75:
                stat_text = "<font color='#059669'><b>✓ Aceptable / Conforme</b></font>"
            elif val >= 55:
                stat_text = "<font color='#d97706'><b>⚠️ Atención Requerida</b></font>"
            else:
                stat_text = "<font color='#e11d48'><b>❌ No Conforme / Crítico</b></font>"

            if "maintainability" in crit_key:
                target_val = "≥ 65.0 (Radon/Halstead)"
            elif "cyclomatic" in crit_key:
                target_val = "≤ 10 por función (McCabe)"
            elif "duplication" in crit_key:
                target_val = "< 5% duplicación"
            elif "coverage" in crit_key:
                target_val = "≥ 80% cobertura"
            elif "architecture" in crit_key:
                target_val = "0 dependencias circulares"
            elif "dependency" in crit_key:
                target_val = "100% al día / 0 vulnerabilidades"
            else:
                target_val = "0 violaciones de estándar"

            metrics_rows.append([
                Paragraph(f"<b>{label}</b>", body_style),
                Paragraph(f"<b>{val:.1f}</b> / 100", bold_body),
                Paragraph(target_val, body_style),
                Paragraph(stat_text, body_style),
            ])

        metrics_table = Table(metrics_rows, colWidths=[190, 95, 125, 130])
        metrics_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0e7ff")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("PADDING", (0, 0), (-1, -1), 3.5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(metrics_table)
        elements.append(Spacer(1, 10))

        # ── 5. DIAGNÓSTICO DE ARQUITECTURA Y MODULARIDAD ─────────────────
        elements.append(Paragraph("2. Diagnóstico de Arquitectura, Modularidad y Ciclos", heading_h1))
        has_cycles = architecture.get("has_circular_dependencies") or len(architecture.get("ciclos_detectados", [])) > 0
        cycles = architecture.get("ciclos_detectados", [])

        if has_cycles:
            arch_summary = (
                f"<font color='#e11d48'><b>⚠️ ALERTA ARQUITECTÓNICA CRÍTICA: Se detectaron {len(cycles)} dependencias circulares.</b></font><br/>"
                f"Las dependencias cíclicas impiden desacoplar módulos, bloquean pruebas aisladas y generan recompilaciones en cascada.<br/>"
                f"<b>Cadenas detectadas:</b><br/>" +
                "<br/>".join([f"• <code>{clean_xml(' → '.join(c))}</code>" for c in cycles])
            )
            arch_bg = colors.HexColor("#fff1f2")
            arch_border = colors.HexColor("#e11d48")
        else:
            arch_summary = (
                "<font color='#059669'><b>✓ Grafo Acíclico Dirigido (DAG) Conforme:</b></font><br/>"
                "No se detectaron dependencias circulares entre los módulos analizados. El flujo de invocación respeta "
                "la jerarquía y los límites de capas definidos en los estándares técnicos del equipo."
            )
            arch_bg = colors.HexColor("#f0fdf4")
            arch_border = colors.HexColor("#059669")

        arch_table = Table([[Paragraph(arch_summary, body_style)]], colWidths=[540])
        arch_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), arch_bg),
            ("BOX", (0, 0), (-1, -1), 1, arch_border),
            ("PADDING", (0, 0), (-1, -1), 7),
        ]))
        elements.append(arch_table)
        elements.append(Spacer(1, 12))

        # ── 6. AUDITORÍA EXHAUSTIVA DE DEPENDENCIAS Y COMPATIBILIDAD ────
        elements.append(Paragraph("3. Auditoría Exhaustiva de Dependencias y Control de Versiones", heading_h1))

        if dependencies and dependencies.get("dependencies"):
            tot_d = dependencies.get("total_dependencies", 0)
            up_d = dependencies.get("up_to_date_count", 0)
            out_d = dependencies.get("outdated_count", 0)
            incomp_d = dependencies.get("incompatible_count", 0)
            maj_d = dependencies.get("major_updates_count", 0)
            min_d = dependencies.get("minor_updates_count", 0)
            pat_d = dependencies.get("patch_updates_count", 0)
            d_score = dependencies.get("score", 100.0)

            dep_sum_html = (
                f"<b>Resumen de Ecosistema:</b> Total dependencias detectadas: <b>{tot_d}</b> | "
                f"<font color='#059669'><b>Al día: {up_d}</b></font> | "
                f"<font color='#d97706'><b>Desactualizadas: {out_d}</b></font> "
                f"(Parche: {pat_d}, Menor: {min_d}, Mayor: {maj_d}) | "
                f"<font color='#e11d48'><b>Incompatibles: {incomp_d}</b></font><br/>"
                f"<b>Índice de Salud de Dependencias:</b> <b>{d_score:.1f} / 100</b>. "
                f"A continuación se detalla el estado individual de cada paquete extraído de los manifiestos del proyecto."
            )
            dep_sum_table = Table([[Paragraph(dep_sum_html, body_style)]], colWidths=[540])
            dep_sum_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]))
            elements.append(dep_sum_table)
            elements.append(Spacer(1, 6))

            dep_rows = [
                [
                    Paragraph("<b>Paquete / Manifiesto</b>", bold_body),
                    Paragraph("<b>Versión Actual</b>", bold_body),
                    Paragraph("<b>Versión Recomendada</b>", bold_body),
                    Paragraph("<b>Estado / Riesgo</b>", bold_body),
                    Paragraph("<b>Diagnóstico & Comando CLI Sugerido</b>", bold_body),
                ]
            ]

            for d_item in dependencies.get("dependencies", []):
                st = d_item.get("status", "up_to_date")
                risk = d_item.get("risk_level", "low").upper()
                if st == "incompatible":
                    st_label = f"<font color='#e11d48'><b>Incompatible</b><br/>[{risk}]</font>"
                elif st == "major_update":
                    st_label = f"<font color='#ea580c'><b>Major Update</b><br/>[{risk}]</font>"
                elif st == "minor_update":
                    st_label = f"<font color='#d97706'><b>Minor Update</b><br/>[{risk}]</font>"
                elif st == "patch_update":
                    st_label = f"<font color='#2563eb'><b>Patch</b><br/>[{risk}]</font>"
                else:
                    st_label = "<font color='#059669'><b>Al Día</b><br/>[LOW]</font>"

                src_name = f"<b>{clean_xml(d_item.get('package_name', ''))}</b><br/><font size='6.5' color='#64748b'>({clean_xml(d_item.get('source_file', 'manifiesto'))} - {d_item.get('ecosystem', '')})</font>"
                cmd_txt = clean_xml(d_item.get("upgrade_command") or "—")
                reason_txt = clean_xml(d_item.get("reason", ""))

                detail_p = f"<font size='6.5' color='#475569'>{reason_txt}</font><br/><code>{cmd_txt}</code>"

                dep_rows.append([
                    Paragraph(src_name, body_style),
                    Paragraph(f"<code>{clean_xml(d_item.get('current_version', 'N/A'))}</code>", body_style),
                    Paragraph(f"<b><code>{clean_xml(d_item.get('recommended_version', 'N/A'))}</code></b>", bold_body),
                    Paragraph(st_label, body_style),
                    Paragraph(detail_p, body_style),
                ])

            dep_table = Table(dep_rows, colWidths=[120, 75, 85, 75, 185])
            dep_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("PADDING", (0, 0), (-1, -1), 3.5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            elements.append(KeepTogether([dep_table]))
        else:
            no_deps_p = (
                "<b>Aviso de Dependencias:</b> No se detectaron manifiestos de dependencias "
                "(<code>requirements.txt</code>, <code>package.json</code>, <code>pom.xml</code>, <code>go.mod</code>, <code>Cargo.toml</code>) "
                "en la raíz o subdirectorios del repositorio. Asegúrese de incluir los archivos de configuración para auditar versiones de paquetes."
            )
            no_dep_table = Table([[Paragraph(no_deps_p, body_style)]], colWidths=[540])
            no_dep_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]))
            elements.append(no_dep_table)

        elements.append(Spacer(1, 12))

        # ── 7. PLAN DE MEJORA Y ACCIONES PRIORIZADAS (HALLAZGOS DETALLADOS) ─
        elements.append(Paragraph("4. Plan de Mejora y Acciones Priorizadas (Hallazgos Detallados)", heading_h1))

        if not findings:
            elements.append(Paragraph("✓ No se encontraron violaciones críticas ni advertencias de deuda técnica en el código analizado.", body_style))
        else:
            crit_findings = [f for f in findings if f.get("severidad") in ("critical", "high")]
            other_findings = [f for f in findings if f.get("severidad") not in ("critical", "high")]
            ordered_findings = crit_findings + other_findings

            for idx, f in enumerate(ordered_findings[:20], 1):
                sev = f.get("severidad", "info").upper()
                if sev == "CRITICAL":
                    sev_color = "#e11d48"
                    sev_badge = "CRÍTICO"
                    header_bg = colors.HexColor("#ffe4e6")
                elif sev == "HIGH":
                    sev_color = "#ea580c"
                    sev_badge = "ALTO"
                    header_bg = colors.HexColor("#ffedd5")
                elif sev == "WARNING":
                    sev_color = "#d97706"
                    sev_badge = "MEDIO"
                    header_bg = colors.HexColor("#fef3c7")
                else:
                    sev_color = "#2563eb"
                    sev_badge = "INFO"
                    header_bg = colors.HexColor("#eff6ff")

                file_line = f"{clean_xml(f.get('file_path', ''))}" + (f":L{f.get('line_number')}" if f.get('line_number') else "")
                fn_name = f" | Función/Clase: <code>{clean_xml(f.get('function_name'))}</code>" if f.get('function_name') else ""
                rag_ref = f" | Rúbrica RAG: <i>{clean_xml(f.get('rag_source'))}</i>" if f.get('rag_source') else ""
                crit_title = f.get('criterio', '').replace('_', ' ').upper()

                header_text = (
                    f"<b>#{idx}. [{sev_badge}] {crit_title}</b> — <code>{file_line}</code>{fn_name}{rag_ref}"
                )

                finding_rows = [
                    [
                        Paragraph(header_text, ParagraphStyle("FindingH", fontName="Helvetica-Bold", fontSize=8, textColor=colors.HexColor(sev_color))),
                    ],
                    [
                        Paragraph(f"<b>Diagnóstico y Causa Raíz:</b> {clean_xml(f.get('explicacion', ''))}", body_style),
                    ],
                    [
                        Paragraph(f"<b>Plan de Refactorización Recomendado:</b> {clean_xml(f.get('sugerencia', 'Refactorizar de acuerdo al estándar de ingeniería.'))}", ParagraphStyle("SuggP", fontName="Helvetica", fontSize=7.5, leading=10.5, textColor=colors.HexColor("#065f46"))),
                    ],
                ]

                f_table = Table(finding_rows, colWidths=[540])
                f_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), header_bg),
                    ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#ffffff")),
                    ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#f0fdf4")),
                    ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
                    ("PADDING", (0, 0), (-1, -1), 4),
                ]))
                elements.append(KeepTogether([f_table, Spacer(1, 6)]))

        # ── 8. DOCUMENTACIÓN Y REGISTROS DE DECISIÓN DE ARQUITECTURA (ADR) ─
        if generated_docs:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph("5. Architecture Decision Records (ADRs) Vivos Autogenerados", heading_h1))
            for doc_item in generated_docs:
                doc_title = clean_xml(doc_item.get("titulo", "ADR"))
                doc_path = clean_xml(doc_item.get("path", ""))
                elements.append(Paragraph(f"• <b>{doc_title}</b> (Ubicación: <code>{doc_path}</code>)", body_style))

        # Compilar documento final con canvas numerado
        doc.build(elements, canvasmaker=NumberedCanvas)
        buffer.seek(0)
        return buffer.getvalue()

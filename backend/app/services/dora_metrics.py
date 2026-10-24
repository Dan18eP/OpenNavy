"""
Integración con Issue Trackers y Métricas DORA.

Este módulo conecta Praxia con sistemas externos (Jira, GitHub Issues, Linear)
para calcular los últimos dos criterios de calidad:
- Densidad de Defectos (defectos reportados por KLOC)
- Change Failure Rate / Tasa de Fallos en Cambios (DORA)
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DefectRecord:
    """Representa un defecto o incidente registrado en el tracker."""
    id: str
    title: str
    created_at: datetime
    resolved_at: Optional[datetime]
    severity: str  # critical, high, medium, low
    related_file: Optional[str] = None


class DORAMetricsCalculator:
    """
    Calcula las cuatro métricas DORA (Accelerate):
    1. Deployment Frequency
    2. Lead Time for Changes
    3. Change Failure Rate (CFR) — usada en los 8 criterios
    4. Time to Restore Service (MTTR)
    """

    def calculate_change_failure_rate(
        self, total_deployments: int, failed_deployments: int
    ) -> Dict[str, Any]:
        """
        CFR = (failed_deployments / total_deployments) * 100

        Umbrales DORA Elite:
        - Elite: < 5%
        - High: 5-10%
        - Medium: 10-15%
        - Low: > 15%
        """
        if total_deployments == 0:
            return {"cfr_percent": 0.0, "dora_level": "unknown", "score": 75.0}

        cfr_pct = (failed_deployments / total_deployments) * 100

        if cfr_pct < 5:
            dora_level = "Elite"
            score = 100.0
        elif cfr_pct < 10:
            dora_level = "High"
            score = 80.0
        elif cfr_pct < 15:
            dora_level = "Medium"
            score = 60.0
        else:
            dora_level = "Low"
            score = max(0.0, 100.0 - cfr_pct * 2)

        return {
            "cfr_percent": round(cfr_pct, 2),
            "dora_level": dora_level,
            "score": round(score, 1),
            "total_deployments": total_deployments,
            "failed_deployments": failed_deployments,
        }

    def calculate_defect_density(
        self, defects: List[DefectRecord], total_kloc: float
    ) -> Dict[str, Any]:
        """
        Defect Density = defects / KLOC

        Umbrales industria:
        - Excellent: < 0.5 / KLOC
        - Good: 0.5–1.0 / KLOC
        - Warning: 1.0–5.0 / KLOC
        - Critical: > 5.0 / KLOC
        """
        if total_kloc <= 0:
            return {"density": 0.0, "score": 75.0, "level": "unknown"}

        density = len(defects) / total_kloc
        critical_count = sum(1 for d in defects if d.severity in ("critical", "high"))

        if density < 0.5:
            score = 100.0
            level = "Excellent"
        elif density < 1.0:
            score = 85.0
            level = "Good"
        elif density < 5.0:
            score = max(40.0, 85.0 - (density - 1.0) * 15)
            level = "Warning"
        else:
            score = max(0.0, 40.0 - (density - 5.0) * 5)
            level = "Critical"

        # Penalización por defectos críticos
        if critical_count > 0:
            score = max(0.0, score - critical_count * 5)

        return {
            "density": round(density, 3),
            "score": round(score, 1),
            "level": level,
            "total_defects": len(defects),
            "critical_defects": critical_count,
            "kloc": round(total_kloc, 2),
        }


class MockIssueTrackerClient:
    """
    Cliente simulado de integración con Jira / GitHub Issues / Linear.
    En producción se reemplazaría con llamadas HTTP reales a la API del tracker.
    """

    def __init__(self, tracker_url: str = "", api_token: str = ""):
        self.tracker_url = tracker_url
        self.api_token = api_token

    def get_open_bugs(self, repo_name: str) -> List[DefectRecord]:
        """Retorna los bugs abiertos para el repositorio dado."""
        # Stub: en producción, llamar a Jira/GitHub Issues API
        return []

    def get_deployment_stats(self, repo_name: str, days: int = 30) -> Dict[str, int]:
        """Retorna estadísticas de despliegue del período indicado."""
        # Stub: en producción, llamar a CI/CD API (GitHub Actions, GitLab CI, etc.)
        return {"total_deployments": 0, "failed_deployments": 0}

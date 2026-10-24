from app.services.dora_metrics import DORAMetricsCalculator, DefectRecord
from datetime import datetime


def test_change_failure_rate_elite():
    calc = DORAMetricsCalculator()
    result = calc.calculate_change_failure_rate(total_deployments=100, failed_deployments=3)
    assert result["dora_level"] == "Elite"
    assert result["cfr_percent"] == 3.0
    assert result["score"] == 100.0


def test_change_failure_rate_critical():
    calc = DORAMetricsCalculator()
    result = calc.calculate_change_failure_rate(total_deployments=100, failed_deployments=20)
    assert result["dora_level"] == "Low"
    assert result["cfr_percent"] == 20.0
    assert result["score"] <= 60.0


def test_change_failure_rate_zero_deployments():
    calc = DORAMetricsCalculator()
    result = calc.calculate_change_failure_rate(total_deployments=0, failed_deployments=0)
    assert result["dora_level"] == "unknown"


def test_defect_density_excellent():
    calc = DORAMetricsCalculator()
    defects = [DefectRecord(id="1", title="Minor bug", created_at=datetime.now(), resolved_at=None, severity="low")]
    result = calc.calculate_defect_density(defects=defects, total_kloc=10.0)
    assert result["density"] == 0.1
    assert result["level"] == "Excellent"
    assert result["score"] == 100.0


def test_defect_density_critical():
    calc = DORAMetricsCalculator()
    defects = [
        DefectRecord(id=str(i), title=f"Bug {i}", created_at=datetime.now(), resolved_at=None, severity="critical")
        for i in range(60)
    ]
    result = calc.calculate_defect_density(defects=defects, total_kloc=5.0)
    assert result["level"] == "Critical"
    assert result["score"] < 40.0
    assert result["critical_defects"] == 60

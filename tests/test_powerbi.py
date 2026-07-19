"""Tests for Power BI documentation helpers."""

from __future__ import annotations

from powerbi.datasets import dashboard_kpis, gold_dataset_requirements


def test_powerbi_kpis_defined() -> None:
    kpis = dashboard_kpis()
    assert len(kpis) >= 5
    assert any(kpi.name == "Fleet Health Score" for kpi in kpis)
    assert "gold_fleet_kpis" in gold_dataset_requirements()

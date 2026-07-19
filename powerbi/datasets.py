"""Power BI dataset notes for the Gold layer outputs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardKPI:
    """A dashboard metric that should be available in Power BI."""

    name: str
    description: str
    grain: str


def dashboard_kpis() -> list[DashboardKPI]:
    """Return the main KPIs expected by the fleet dashboard."""

    return [
        DashboardKPI("Vehicle Count", "Distinct vehicles active in the selected period", "daily"),
        DashboardKPI("Average Speed", "Average telemetry speed per vehicle type", "daily and route"),
        DashboardKPI("Fuel Consumption", "Fuel consumption trend and totals", "daily and route"),
        DashboardKPI("Fleet Health Score", "Composite health score derived from telemetry signals", "daily and vehicle"),
        DashboardKPI("Engine Temperature", "Temperature trend and alert distribution", "vehicle and route"),
        DashboardKPI("Battery Status", "Battery voltage distribution and exceptions", "vehicle"),
        DashboardKPI("Top Anomalies", "Anomalies ranked by severity and recency", "daily"),
        DashboardKPI("Route Analysis", "Route-level telemetry summary", "route"),
        DashboardKPI("Daily Summary", "Daily fleet metrics for leadership reporting", "daily"),
        DashboardKPI("Fleet Map", "Geospatial fleet snapshot for operations", "live"),
    ]


def gold_dataset_requirements() -> list[str]:
    """Describe the Gold layer tables that should be exposed to Power BI."""

    return [
        "gold_fleet_kpis",
        "gold_vehicle_summaries",
        "gold_route_summaries",
        "gold_driver_summaries",
        "gold_daily_statistics",
        "gold_anomaly_summary",
    ]

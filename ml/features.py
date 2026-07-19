"""Feature engineering for the anomaly detection model."""

from __future__ import annotations

import pandas as pd

FEATURE_COLUMNS = [
    "speed",
    "rpm",
    "engine_temperature",
    "fuel_level",
    "battery_voltage",
    "acceleration",
    "brake_pressure",
    "gps_accuracy",
    "tire_pressure",
    "humidity",
    "fuel_consumption",
    "health_score",
]


def build_feature_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Create model-ready features from telemetry data."""

    output = frame.copy()
    output["temperature_gap"] = output["engine_temperature"] - 90.0
    output["speed_to_rpm_ratio"] = output["speed"].div(output["rpm"].replace(0, pd.NA)).fillna(0.0)
    output["fuel_stress"] = 100.0 - output["fuel_level"]
    output["battery_deviation"] = (output["battery_voltage"] - 12.6).abs()
    output["health_score"] = output.get("health_score", 100.0)
    return output


def prepare_training_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Select the final numerical columns used by Isolation Forest."""

    feature_frame = build_feature_frame(frame)
    return feature_frame[FEATURE_COLUMNS + ["temperature_gap", "speed_to_rpm_ratio", "fuel_stress", "battery_deviation"]]

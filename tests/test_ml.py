"""Tests for ML feature engineering and training."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ml.evaluate import evaluate_model
from ml.predict import score_anomalies
from ml.train import train_isolation_forest


def _sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "speed": 40.0,
                "rpm": 1800,
                "engine_temperature": 88.0,
                "fuel_level": 70.0,
                "battery_voltage": 12.5,
                "acceleration": 0.2,
                "brake_pressure": 5.0,
                "gps_accuracy": 2.0,
                "tire_pressure": 34.0,
                "humidity": 40.0,
                "fuel_consumption": 0.8,
                "health_score": 92.0,
                "is_anomaly": 0,
            },
            {
                "speed": 120.0,
                "rpm": 5000,
                "engine_temperature": 118.0,
                "fuel_level": 12.0,
                "battery_voltage": 11.2,
                "acceleration": 4.5,
                "brake_pressure": 20.0,
                "gps_accuracy": 15.0,
                "tire_pressure": 28.0,
                "humidity": 80.0,
                "fuel_consumption": 5.2,
                "health_score": 20.0,
                "is_anomaly": 1,
            },
            {
                "speed": 55.0,
                "rpm": 2200,
                "engine_temperature": 91.0,
                "fuel_level": 60.0,
                "battery_voltage": 12.7,
                "acceleration": 0.7,
                "brake_pressure": 7.0,
                "gps_accuracy": 3.0,
                "tire_pressure": 33.0,
                "humidity": 55.0,
                "fuel_consumption": 1.1,
                "health_score": 86.0,
                "is_anomaly": 0,
            },
        ]
    )


def test_train_and_score(tmp_path: Path) -> None:
    frame = _sample_frame()
    model_path = tmp_path / "model.joblib"

    result = train_isolation_forest(frame, model_path=model_path, contamination=0.34, random_state=1)
    assert result.model_path.exists()

    scored = score_anomalies(frame, model_path=model_path)
    assert "anomaly_flag" in scored.columns
    assert "anomaly_score" in scored.columns

    metrics = evaluate_model(frame, model_path=str(model_path))
    assert 0.0 <= metrics.accuracy <= 1.0
    assert len(metrics.confusion_matrix) == 2

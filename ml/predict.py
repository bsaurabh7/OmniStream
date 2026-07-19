"""Prediction helpers for anomaly scoring."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from .features import prepare_training_data


def load_model(model_path: str | Path) -> tuple[object, list[str]]:
    """Load a persisted Isolation Forest model and its feature columns."""

    payload = joblib.load(Path(model_path))
    return payload["model"], payload["feature_columns"]


def score_anomalies(frame: pd.DataFrame, model_path: str | Path) -> pd.DataFrame:
    """Score telemetry rows and return anomaly flags."""

    model, feature_columns = load_model(model_path)
    feature_frame = prepare_training_data(frame)[feature_columns]
    predictions = model.predict(feature_frame)
    decision_scores = model.decision_function(feature_frame)
    output = frame.copy()
    output["anomaly_flag"] = (predictions == -1).astype(int)
    output["anomaly_score"] = decision_scores
    return output

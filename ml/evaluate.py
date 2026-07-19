"""Evaluation helpers for anomaly detection models."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

from .features import prepare_training_data
from .predict import load_model


@dataclass(slots=True)
class ModelMetrics:
    """Basic classification metrics for anomaly detection."""

    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: list[list[int]]


def evaluate_model(frame: pd.DataFrame, model_path: str) -> ModelMetrics:
    """Evaluate a saved model using a labelled telemetry frame."""

    model, feature_columns = load_model(model_path)
    feature_frame = prepare_training_data(frame)[feature_columns]
    predicted = (model.predict(feature_frame) == -1).astype(int)
    actual = frame["is_anomaly"].astype(int)
    return ModelMetrics(
        accuracy=accuracy_score(actual, predicted),
        precision=precision_score(actual, predicted, zero_division=0),
        recall=recall_score(actual, predicted, zero_division=0),
        f1_score=f1_score(actual, predicted, zero_division=0),
        confusion_matrix=confusion_matrix(actual, predicted).tolist(),
    )

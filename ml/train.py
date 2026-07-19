"""Training workflow for Isolation Forest anomaly detection."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

from config.logging import get_logger
from .features import prepare_training_data

logger = get_logger(__name__)


@dataclass(slots=True)
class TrainingResult:
    """Artifacts produced by a training run."""

    model_path: Path
    feature_columns: list[str]
    contamination: float


def train_isolation_forest(
    frame: pd.DataFrame,
    model_path: str | Path,
    contamination: float = 0.02,
    random_state: int = 42,
) -> TrainingResult:
    """Train and persist an Isolation Forest model."""

    feature_frame = prepare_training_data(frame)
    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=random_state,
    )
    model.fit(feature_frame)

    output_path = Path(model_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "feature_columns": list(feature_frame.columns)}, output_path)
    logger.info("Saved Isolation Forest model to %s", output_path)
    return TrainingResult(
        model_path=output_path,
        feature_columns=list(feature_frame.columns),
        contamination=contamination,
    )

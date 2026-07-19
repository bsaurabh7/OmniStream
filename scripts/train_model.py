"""Train the Isolation Forest anomaly detection model from telemetry data."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config.config import load_config
from config.logging import configure_logging
from ml.train import train_isolation_forest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train the telemetry anomaly model")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def main() -> None:
    configure_logging()
    config = load_config()
    parser = build_parser()
    args = parser.parse_args()
    output_path = args.output or config.model_path
    frame = pd.read_csv(args.input)
    train_isolation_forest(
        frame=frame,
        model_path=output_path,
        contamination=config.contamination,
        random_state=config.random_state,
    )


if __name__ == "__main__":
    main()

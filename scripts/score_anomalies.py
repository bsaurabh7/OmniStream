"""Score telemetry records with a trained Isolation Forest model."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config.config import load_config
from config.logging import configure_logging
from ml.predict import score_anomalies


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score telemetry anomalies")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", type=Path, default=None)
    return parser


def main() -> None:
    configure_logging()
    config = load_config()
    parser = build_parser()
    args = parser.parse_args()
    model_path = args.model or config.model_path
    frame = pd.read_csv(args.input)
    scored = score_anomalies(frame, model_path=model_path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    scored.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()

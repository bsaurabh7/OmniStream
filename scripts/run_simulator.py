"""Command-line entry point for generating telemetry batches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from config.config import load_config
from config.logging import configure_logging
from vehicle_simulator.generator import VehicleTelemetryGenerator


def build_parser() -> argparse.ArgumentParser:
    """Create the simulator CLI parser."""

    parser = argparse.ArgumentParser(description="Generate fleet telemetry samples")
    parser.add_argument("--output", type=Path, default=Path("sample_data/generated/telemetry.jsonl"))
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--batches", type=int, default=1)
    return parser


def main() -> None:
    """Generate batches of telemetry and write them to a JSONL file."""

    configure_logging()
    config = load_config()
    parser = build_parser()
    args = parser.parse_args()

    batch_size = args.batch_size or config.batch_size
    generator = VehicleTelemetryGenerator(
        vehicle_count=config.vehicle_count,
        seed=config.simulator_seed,
        vehicle_types=config.vehicle_types,
        enable_noise=config.enable_noise,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as file_handle:
        for _ in range(args.batches):
            for record in generator.generate_batch(batch_size=batch_size):
                file_handle.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()

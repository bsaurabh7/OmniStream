"""Generate sample telemetry datasets for documentation and testing."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from config.config import load_config
from vehicle_simulator.generator import VehicleTelemetryGenerator


def main() -> None:
    """Write JSON and CSV sample files to the sample_data directory."""

    config = load_config()
    generator = VehicleTelemetryGenerator(
        vehicle_count=min(config.vehicle_count, 100),
        seed=config.simulator_seed,
        vehicle_types=config.vehicle_types,
        enable_noise=config.enable_noise,
    )
    output_dir = Path("sample_data")
    output_dir.mkdir(parents=True, exist_ok=True)
    records = generator.generate_batch(batch_size=50)

    json_path = output_dir / "telemetry_sample.json"
    csv_path = output_dir / "telemetry_sample.csv"
    anomaly_path = output_dir / "anomaly_sample.json"

    json_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    anomaly_records = [record | {"anomaly_flag": 1, "anomaly_type": "temperature_spike"} for record in records[:5]]
    anomaly_path.write_text(json.dumps(anomaly_records, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    main()

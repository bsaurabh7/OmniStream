"""Configuration loading for OmniStream."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

from .constants import DEFAULT_VEHICLE_TYPES


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Runtime configuration values loaded from environment variables."""

    event_hub_connection_string: str | None
    event_hub_name: str | None
    event_hub_consumer_group: str
    mongodb_uri: str | None
    mongodb_database: str
    mongodb_collection: str
    vehicle_count: int
    event_rate_per_second: int
    batch_size: int
    simulator_seed: int
    model_path: Path
    delta_base_path: Path
    bronze_path: Path
    silver_path: Path
    gold_path: Path
    checkpoint_path: Path
    random_state: int
    contamination: float
    enable_noise: bool
    vehicle_types: tuple[str, ...]


def _get_bool(name: str, default: bool) -> bool:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    raw_value = os.getenv(name)
    return default if raw_value is None else int(raw_value)


def _get_float(name: str, default: float) -> float:
    raw_value = os.getenv(name)
    return default if raw_value is None else float(raw_value)


def load_config() -> AppConfig:
    """Load application settings from environment variables and .env files."""

    load_dotenv(override=False)

    delta_base_path = Path(os.getenv("DELTA_BASE_PATH", "./lakehouse")).resolve()
    bronze_path = Path(os.getenv("BRONZE_PATH", delta_base_path / "bronze")).resolve()
    silver_path = Path(os.getenv("SILVER_PATH", delta_base_path / "silver")).resolve()
    gold_path = Path(os.getenv("GOLD_PATH", delta_base_path / "gold")).resolve()
    checkpoint_path = Path(
        os.getenv("CHECKPOINT_PATH", delta_base_path / "checkpoints")
    ).resolve()

    vehicle_types = tuple(
        vehicle_type.strip()
        for vehicle_type in os.getenv("SIMULATOR_VEHICLE_TYPES", ",".join(DEFAULT_VEHICLE_TYPES)).split(",")
        if vehicle_type.strip()
    )

    return AppConfig(
        event_hub_connection_string=os.getenv("EVENT_HUB_CONNECTION_STRING"),
        event_hub_name=os.getenv("EVENT_HUB_NAME"),
        event_hub_consumer_group=os.getenv("EVENT_HUB_CONSUMER_GROUP", "$Default"),
        mongodb_uri=os.getenv("MONGODB_URI"),
        mongodb_database=os.getenv("MONGODB_DATABASE", "omnistream"),
        mongodb_collection=os.getenv("MONGODB_COLLECTION", "anomalies"),
        vehicle_count=_get_int("SIMULATOR_VEHICLE_COUNT", 5000),
        event_rate_per_second=_get_int("SIMULATOR_EVENT_RATE_PER_SECOND", 100),
        batch_size=_get_int("SIMULATOR_BATCH_SIZE", 100),
        simulator_seed=_get_int("SIMULATOR_SEED", 42),
        model_path=Path(os.getenv("MODEL_PATH", "./artifacts/isolation_forest.joblib")).resolve(),
        delta_base_path=delta_base_path,
        bronze_path=bronze_path,
        silver_path=silver_path,
        gold_path=gold_path,
        checkpoint_path=checkpoint_path,
        random_state=_get_int("ML_RANDOM_STATE", 42),
        contamination=_get_float("ANOMALY_CONTAMINATION", 0.02),
        enable_noise=_get_bool("SIMULATOR_ENABLE_NOISE", True),
        vehicle_types=vehicle_types,
    )

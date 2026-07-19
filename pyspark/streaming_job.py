"""Databricks Structured Streaming job for telemetry ingestion."""

from __future__ import annotations

from dataclasses import dataclass

try:
    from pyspark.sql import DataFrame, SparkSession
    from pyspark.sql import functions as F
except ImportError:  # pragma: no cover - Spark may not be available in unit tests
    DataFrame = SparkSession = object  # type: ignore[assignment]
    F = object  # type: ignore[assignment]

from config.logging import get_logger
from delta.bronze import write_bronze
from delta.gold import write_gold
from delta.silver import build_silver_frame, write_silver
from .schemas import telemetry_schema
from .transformations import add_derived_features, clean_telemetry, deduplicate_events, validate_telemetry

logger = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class StreamingPaths:
    """Paths required by the streaming job."""

    bronze_path: str
    silver_path: str
    gold_path: str
    checkpoint_path: str


def parse_eventhub_stream(raw_stream: DataFrame) -> DataFrame:
    """Parse the Event Hubs binary stream into a structured telemetry frame."""

    parsed = raw_stream.select(
        F.col("enqueuedTime").alias("event_enqueued_time"),
        F.col("body").cast("string").alias("body"),
    )
    return parsed.select(F.from_json(F.col("body"), telemetry_schema).alias("payload"), "event_enqueued_time").select("payload.*", "event_enqueued_time")


def build_streaming_pipeline(raw_stream: DataFrame) -> DataFrame:
    """Apply the telemetry transformations used in the lakehouse pipeline."""

    frame = parse_eventhub_stream(raw_stream)
    frame = validate_telemetry(frame)
    frame = clean_telemetry(frame)
    frame = deduplicate_events(frame)
    frame = add_derived_features(frame)
    return frame


def run_streaming_job(spark: SparkSession, raw_stream: DataFrame, paths: StreamingPaths) -> None:
    """Execute the Structured Streaming flow and materialize Delta layers."""

    logger.info("Starting streaming job")
    structured_frame = build_streaming_pipeline(raw_stream)
    silver_frame = build_silver_frame(structured_frame)

    write_bronze(structured_frame, paths.bronze_path, paths.checkpoint_path)
    write_silver(silver_frame, paths.silver_path, paths.checkpoint_path)
    write_gold(silver_frame, paths.gold_path, paths.checkpoint_path)
    logger.info("Streaming job definitions created successfully")

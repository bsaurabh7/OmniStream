"""Reusable PySpark transformations for telemetry processing."""

from __future__ import annotations

try:
    from pyspark.sql import DataFrame
    from pyspark.sql import functions as F
    from pyspark.sql import Window
except ImportError:  # pragma: no cover - Spark may not be available in unit tests
    DataFrame = object  # type: ignore[assignment]
    F = Window = object  # type: ignore[assignment]


def validate_telemetry(frame: DataFrame) -> DataFrame:
    """Filter out rows with missing critical fields."""

    critical_columns = [
        "vehicle_id",
        "timestamp",
        "vehicle_type",
        "latitude",
        "longitude",
        "speed",
        "rpm",
        "engine_temperature",
        "fuel_level",
        "battery_voltage",
    ]
    return frame.dropna(subset=critical_columns)


def clean_telemetry(frame: DataFrame) -> DataFrame:
    """Normalize telemetry values and clip obvious outliers."""

    return (
        frame.withColumn("speed", F.greatest(F.lit(0.0), F.col("speed")))
        .withColumn("rpm", F.greatest(F.lit(0), F.col("rpm")))
        .withColumn("fuel_level", F.when(F.col("fuel_level") < 0, 0.0).otherwise(F.col("fuel_level")))
        .withColumn("engine_temperature", F.when(F.col("engine_temperature") < 0, 0.0).otherwise(F.col("engine_temperature")))
    )


def deduplicate_events(frame: DataFrame) -> DataFrame:
    """Drop duplicate records using the vehicle-trip timestamp key."""

    return frame.dropDuplicates(["vehicle_id", "trip_id", "timestamp"])


def add_derived_features(frame: DataFrame) -> DataFrame:
    """Add simple engineered features for analytics and anomaly detection."""

    timestamp_col = F.to_timestamp("timestamp")
    return (
        frame.withColumn("event_timestamp", timestamp_col)
        .withColumn("engine_temperature_delta", F.col("engine_temperature") - F.lit(90.0))
        .withColumn("fuel_efficiency_proxy", F.when(F.col("fuel_consumption") > 0, F.col("speed") / F.col("fuel_consumption")).otherwise(F.lit(0.0)))
        .withColumn("health_score", F.greatest(F.lit(0.0), F.lit(100.0) - F.abs(F.col("engine_temperature") - F.lit(90.0)) - (F.col("speed") / F.lit(5.0))))
    )


def add_rolling_average(frame: DataFrame, partition_column: str, value_column: str, output_column: str, rows: int = 5) -> DataFrame:
    """Compute a rolling average within each vehicle partition."""

    window_spec = Window.partitionBy(partition_column).orderBy("event_timestamp").rowsBetween(-rows + 1, 0)
    return frame.withColumn(output_column, F.avg(F.col(value_column)).over(window_spec))

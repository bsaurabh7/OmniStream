"""Silver layer transformations for cleaned telemetry."""

from __future__ import annotations

try:
    from pyspark.sql import DataFrame
    from pyspark.sql import functions as F
except ImportError:  # pragma: no cover
    DataFrame = object  # type: ignore[assignment]
    F = object  # type: ignore[assignment]


def build_silver_frame(frame: DataFrame) -> DataFrame:
    """Create the cleaned and validated Silver DataFrame."""

    return (
        frame.withColumn("event_date", F.to_date("event_timestamp"))
        .withColumn("speed_kph", F.round(F.col("speed"), 2))
        .withColumn("temperature_band", F.when(F.col("engine_temperature") >= 100, "critical").when(F.col("engine_temperature") >= 90, "warning").otherwise("normal"))
        .dropDuplicates(["vehicle_id", "trip_id", "event_timestamp"])
    )


def write_silver(frame: DataFrame, silver_path: str, checkpoint_path: str) -> None:
    """Write cleaned telemetry to the Silver Delta layer."""

    query = (
        frame.writeStream.format("delta")
        .outputMode("append")
        .option("checkpointLocation", f"{checkpoint_path}/silver")
        .option("path", silver_path)
    )
    query.trigger(availableNow=True).start()

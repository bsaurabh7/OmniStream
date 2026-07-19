"""Gold layer aggregations for Power BI and reporting."""

from __future__ import annotations

try:
    from pyspark.sql import DataFrame
    from pyspark.sql import functions as F
except ImportError:  # pragma: no cover
    DataFrame = object  # type: ignore[assignment]
    F = object  # type: ignore[assignment]


def build_gold_metrics(frame: DataFrame) -> DataFrame:
    """Aggregate fleet KPIs from the Silver layer."""

    return frame.groupBy("event_date", "vehicle_type").agg(
        F.countDistinct("vehicle_id").alias("vehicle_count"),
        F.avg("speed").alias("avg_speed"),
        F.avg("fuel_level").alias("avg_fuel_level"),
        F.avg("engine_temperature").alias("avg_engine_temperature"),
        F.avg("battery_voltage").alias("avg_battery_voltage"),
        F.avg("health_score").alias("avg_health_score"),
        F.sum("fuel_consumption").alias("total_fuel_consumption"),
    )


def write_gold(frame: DataFrame, gold_path: str, checkpoint_path: str) -> None:
    """Write Gold-level aggregates for dashboard consumption."""

    query = (
        frame.writeStream.format("delta")
        .outputMode("complete")
        .option("checkpointLocation", f"{checkpoint_path}/gold")
        .option("path", gold_path)
    )
    query.trigger(availableNow=True).start()

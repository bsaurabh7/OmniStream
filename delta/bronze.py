"""Bronze layer write helpers."""

from __future__ import annotations

try:
    from pyspark.sql import DataFrame
except ImportError:  # pragma: no cover
    DataFrame = object  # type: ignore[assignment]


def write_bronze(frame: DataFrame, bronze_path: str, checkpoint_path: str) -> None:
    """Define the Bronze Delta write for raw telemetry events."""

    query = (
        frame.writeStream.format("delta")
        .outputMode("append")
        .option("checkpointLocation", f"{checkpoint_path}/bronze")
        .option("path", bronze_path)
    )
    query.trigger(availableNow=True).start()

"""Explicit schemas used by Structured Streaming jobs."""

from __future__ import annotations

try:
    from pyspark.sql.types import (
        DoubleType,
        IntegerType,
        StringType,
        StructField,
        StructType,
    )
except ImportError:  # pragma: no cover - Spark may not be available in unit tests
    StructField = StructType = DoubleType = IntegerType = StringType = object  # type: ignore[assignment]


telemetry_schema = StructType(
    [
        StructField("vehicle_id", StringType(), False),
        StructField("timestamp", StringType(), False),
        StructField("vehicle_type", StringType(), False),
        StructField("driver_id", StringType(), False),
        StructField("trip_id", StringType(), False),
        StructField("route_id", StringType(), False),
        StructField("latitude", DoubleType(), False),
        StructField("longitude", DoubleType(), False),
        StructField("speed", DoubleType(), False),
        StructField("rpm", IntegerType(), False),
        StructField("engine_temperature", DoubleType(), False),
        StructField("fuel_level", DoubleType(), False),
        StructField("battery_voltage", DoubleType(), False),
        StructField("gear", IntegerType(), False),
        StructField("odometer", DoubleType(), False),
        StructField("acceleration", DoubleType(), False),
        StructField("brake_pressure", DoubleType(), False),
        StructField("gps_accuracy", DoubleType(), False),
        StructField("tire_pressure", DoubleType(), False),
        StructField("outside_temperature", DoubleType(), False),
        StructField("humidity", DoubleType(), False),
        StructField("fuel_consumption", DoubleType(), False),
        StructField("engine_status", StringType(), False),
        StructField("heading", DoubleType(), False),
        StructField("altitude", DoubleType(), False),
    ]
)

"""Tests for PySpark telemetry transformations."""

from __future__ import annotations

import pytest

from pyspark.sql import Row

from pyspark.transformations import add_derived_features, clean_telemetry, deduplicate_events, validate_telemetry


@pytest.mark.usefixtures("spark")
def test_transformation_pipeline(spark) -> None:
    rows = [
        Row(
            vehicle_id="VH-000001",
            timestamp="2026-01-01T00:00:00Z",
            vehicle_type="Sedan",
            driver_id="DR-00001",
            trip_id="TP-0001",
            route_id="RT-0001",
            latitude=12.9,
            longitude=77.6,
            speed=45.0,
            rpm=1800,
            engine_temperature=95.0,
            fuel_level=60.0,
            battery_voltage=12.6,
            gear=3,
            odometer=12345.6,
            acceleration=0.3,
            brake_pressure=4.0,
            gps_accuracy=2.5,
            tire_pressure=34.0,
            outside_temperature=31.0,
            humidity=55.0,
            fuel_consumption=0.9,
            engine_status="ON",
            heading=80.0,
            altitude=250.0,
        ),
        Row(
            vehicle_id="VH-000001",
            timestamp="2026-01-01T00:00:00Z",
            vehicle_type="Sedan",
            driver_id="DR-00001",
            trip_id="TP-0001",
            route_id="RT-0001",
            latitude=12.9,
            longitude=77.6,
            speed=45.0,
            rpm=1800,
            engine_temperature=95.0,
            fuel_level=60.0,
            battery_voltage=12.6,
            gear=3,
            odometer=12345.6,
            acceleration=0.3,
            brake_pressure=4.0,
            gps_accuracy=2.5,
            tire_pressure=34.0,
            outside_temperature=31.0,
            humidity=55.0,
            fuel_consumption=0.9,
            engine_status="ON",
            heading=80.0,
            altitude=250.0,
        ),
    ]
    frame = spark.createDataFrame(rows)

    validated = validate_telemetry(frame)
    cleaned = clean_telemetry(validated)
    deduped = deduplicate_events(cleaned)
    enriched = add_derived_features(deduped)

    assert enriched.count() == 1
    record = enriched.collect()[0]
    assert record["engine_temperature_delta"] == pytest.approx(5.0)
    assert record["health_score"] <= 100.0

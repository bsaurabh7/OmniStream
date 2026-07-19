"""Tests for the vehicle simulator."""

from __future__ import annotations

from vehicle_simulator.generator import VehicleTelemetryGenerator


def test_generator_produces_expected_fields() -> None:
    generator = VehicleTelemetryGenerator(vehicle_count=10, seed=7)
    record = generator.generate_batch(batch_size=1)[0]

    expected_keys = {
        "vehicle_id",
        "timestamp",
        "vehicle_type",
        "driver_id",
        "trip_id",
        "route_id",
        "latitude",
        "longitude",
        "speed",
        "rpm",
        "engine_temperature",
        "fuel_level",
        "battery_voltage",
        "gear",
        "odometer",
        "acceleration",
        "brake_pressure",
        "gps_accuracy",
        "tire_pressure",
        "outside_temperature",
        "humidity",
        "fuel_consumption",
        "engine_status",
        "heading",
        "altitude",
        "metadata",
    }

    assert expected_keys.issubset(record.keys())
    assert record["speed"] >= 0
    assert 0 <= record["heading"] <= 360

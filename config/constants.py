"""Project-wide constants used across simulator, streaming, and analytics code."""

from __future__ import annotations

from typing import Final, Tuple

DEFAULT_VEHICLE_TYPES: Final[Tuple[str, ...]] = (
    "Sedan",
    "SUV",
    "Truck",
    "Electric Vehicle",
    "Bus",
    "Motorcycle",
)

EVENT_FIELDS: Final[Tuple[str, ...]] = (
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
)

DEFAULT_LATITUDE_RANGE: Final[tuple[float, float]] = (12.7, 13.2)
DEFAULT_LONGITUDE_RANGE: Final[tuple[float, float]] = (77.4, 77.9)
DEFAULT_SPEED_RANGE: Final[tuple[float, float]] = (0.0, 120.0)
DEFAULT_RPM_RANGE: Final[tuple[int, int]] = (600, 5200)
DEFAULT_FUEL_LEVEL_RANGE: Final[tuple[float, float]] = (5.0, 100.0)
DEFAULT_BATTERY_VOLTAGE_RANGE: Final[tuple[float, float]] = (11.8, 14.8)
DEFAULT_GPS_ACCURACY_RANGE: Final[tuple[float, float]] = (1.5, 12.0)
DEFAULT_TIRE_PRESSURE_RANGE: Final[tuple[float, float]] = (28.0, 42.0)
DEFAULT_OUTSIDE_TEMPERATURE_RANGE: Final[tuple[float, float]] = (-5.0, 45.0)
DEFAULT_HUMIDITY_RANGE: Final[tuple[float, float]] = (10.0, 95.0)
DEFAULT_ODOMETER_INCREMENT_RANGE: Final[tuple[float, float]] = (0.1, 2.4)
DEFAULT_DRIVER_POOL_SIZE: Final[int] = 2500
DEFAULT_CHUNK_SLEEP_SECONDS: Final[float] = 1.0
DEFAULT_CHECKPOINT_SUBDIR: Final[str] = "checkpoints"
DEFAULT_BRONZE_LAYER: Final[str] = "bronze"
DEFAULT_SILVER_LAYER: Final[str] = "silver"
DEFAULT_GOLD_LAYER: Final[str] = "gold"

"""Data models for simulated vehicle telemetry."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class VehicleType(str, Enum):
    """Supported vehicle categories for the simulator."""

    SEDAN = "Sedan"
    SUV = "SUV"
    TRUCK = "Truck"
    ELECTRIC_VEHICLE = "Electric Vehicle"
    BUS = "Bus"
    MOTORCYCLE = "Motorcycle"


@dataclass(slots=True)
class VehicleEvent:
    """Single telemetry event emitted by the simulator."""

    vehicle_id: str
    timestamp: str
    vehicle_type: str
    driver_id: str
    trip_id: str
    route_id: str
    latitude: float
    longitude: float
    speed: float
    rpm: int
    engine_temperature: float
    fuel_level: float
    battery_voltage: float
    gear: int
    odometer: float
    acceleration: float
    brake_pressure: float
    gps_accuracy: float
    tire_pressure: float
    outside_temperature: float
    humidity: float
    fuel_consumption: float
    engine_status: str
    heading: float
    altitude: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert the event to a JSON-serialisable dictionary."""

        payload = {
            "vehicle_id": self.vehicle_id,
            "timestamp": self.timestamp,
            "vehicle_type": self.vehicle_type,
            "driver_id": self.driver_id,
            "trip_id": self.trip_id,
            "route_id": self.route_id,
            "latitude": round(self.latitude, 6),
            "longitude": round(self.longitude, 6),
            "speed": round(self.speed, 2),
            "rpm": int(self.rpm),
            "engine_temperature": round(self.engine_temperature, 2),
            "fuel_level": round(self.fuel_level, 2),
            "battery_voltage": round(self.battery_voltage, 2),
            "gear": int(self.gear),
            "odometer": round(self.odometer, 3),
            "acceleration": round(self.acceleration, 3),
            "brake_pressure": round(self.brake_pressure, 2),
            "gps_accuracy": round(self.gps_accuracy, 2),
            "tire_pressure": round(self.tire_pressure, 2),
            "outside_temperature": round(self.outside_temperature, 2),
            "humidity": round(self.humidity, 2),
            "fuel_consumption": round(self.fuel_consumption, 3),
            "engine_status": self.engine_status,
            "heading": round(self.heading, 2),
            "altitude": round(self.altitude, 2),
        }
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload

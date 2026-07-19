"""Telemetry generator for realistic vehicle movement and sensor data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import math
import random
from typing import Iterable

from config.constants import (
    DEFAULT_BATTERY_VOLTAGE_RANGE,
    DEFAULT_DRIVER_POOL_SIZE,
    DEFAULT_FUEL_LEVEL_RANGE,
    DEFAULT_GPS_ACCURACY_RANGE,
    DEFAULT_HUMIDITY_RANGE,
    DEFAULT_LATITUDE_RANGE,
    DEFAULT_LONGITUDE_RANGE,
    DEFAULT_ODOMETER_INCREMENT_RANGE,
    DEFAULT_OUTSIDE_TEMPERATURE_RANGE,
    DEFAULT_RPM_RANGE,
    DEFAULT_SPEED_RANGE,
    DEFAULT_TIRE_PRESSURE_RANGE,
    DEFAULT_VEHICLE_TYPES,
)

from .models import VehicleEvent, VehicleType


@dataclass(slots=True)
class VehicleState:
    """Mutable state used to simulate a vehicle over time."""

    vehicle_id: str
    vehicle_type: VehicleType
    driver_id: str
    route_id: str
    trip_id: str
    latitude: float
    longitude: float
    speed: float
    rpm: int
    engine_temperature: float
    fuel_level: float
    battery_voltage: float
    gear: int
    odometer: float
    brake_pressure: float
    gps_accuracy: float
    tire_pressure: float
    outside_temperature: float
    humidity: float
    fuel_consumption: float
    engine_status: str
    heading: float
    altitude: float
    last_timestamp: datetime


class VehicleTelemetryGenerator:
    """Generate realistic telemetry for a fleet of virtual vehicles."""

    def __init__(
        self,
        vehicle_count: int,
        seed: int = 42,
        vehicle_types: Iterable[str] | None = None,
        enable_noise: bool = True,
    ) -> None:
        self._random = random.Random(seed)
        self._vehicle_count = vehicle_count
        self._vehicle_types = tuple(vehicle_types or DEFAULT_VEHICLE_TYPES)
        self._enable_noise = enable_noise
        self._states = [self._create_state(index) for index in range(vehicle_count)]

    def _create_state(self, index: int) -> VehicleState:
        vehicle_type_name = self._random.choice(self._vehicle_types)
        vehicle_type = VehicleType(vehicle_type_name)
        latitude = self._random.uniform(*DEFAULT_LATITUDE_RANGE)
        longitude = self._random.uniform(*DEFAULT_LONGITUDE_RANGE)
        speed = self._random.uniform(0, 70)
        fuel_level = self._random.uniform(*DEFAULT_FUEL_LEVEL_RANGE)
        battery_voltage = self._random.uniform(*DEFAULT_BATTERY_VOLTAGE_RANGE)
        tire_pressure = self._random.uniform(*DEFAULT_TIRE_PRESSURE_RANGE)
        outside_temperature = self._random.uniform(*DEFAULT_OUTSIDE_TEMPERATURE_RANGE)
        humidity = self._random.uniform(*DEFAULT_HUMIDITY_RANGE)
        return VehicleState(
            vehicle_id=f"VH-{index + 1:06d}",
            vehicle_type=vehicle_type,
            driver_id=f"DR-{self._random.randint(1, DEFAULT_DRIVER_POOL_SIZE):05d}",
            route_id=f"RT-{self._random.randint(1, 500):04d}",
            trip_id=f"TP-{self._random.randint(1, 1_000_000):08d}",
            latitude=latitude,
            longitude=longitude,
            speed=speed,
            rpm=900,
            engine_temperature=self._random.uniform(70.0, 92.0),
            fuel_level=fuel_level,
            battery_voltage=battery_voltage,
            gear=1,
            odometer=self._random.uniform(5_000.0, 180_000.0),
            brake_pressure=0.0,
            gps_accuracy=self._random.uniform(*DEFAULT_GPS_ACCURACY_RANGE),
            tire_pressure=tire_pressure,
            outside_temperature=outside_temperature,
            humidity=humidity,
            fuel_consumption=0.0,
            engine_status="ON",
            heading=self._random.uniform(0.0, 359.9),
            altitude=self._random.uniform(10.0, 1200.0),
            last_timestamp=datetime.now(UTC) - timedelta(seconds=self._random.randint(0, 120)),
        )

    def _advance_state(self, state: VehicleState, timestamp: datetime) -> VehicleEvent:
        time_delta_seconds = max((timestamp - state.last_timestamp).total_seconds(), 1.0)
        speed_target = self._random.uniform(*DEFAULT_SPEED_RANGE)
        speed_delta = (speed_target - state.speed) * 0.15
        speed_noise = self._random.uniform(-2.0, 2.0) if self._enable_noise else 0.0
        state.speed = max(0.0, min(140.0, state.speed + speed_delta + speed_noise))

        state.rpm = int(700 + state.speed * 42 + self._random.uniform(-120, 120))
        state.gear = self._gear_from_speed(state.speed, state.vehicle_type)
        state.brake_pressure = max(0.0, min(100.0, self._random.gauss(12 if state.speed > 10 else 3, 8)))
        state.engine_temperature = max(
            55.0,
            min(125.0, state.engine_temperature + (state.speed / 90.0) + self._random.uniform(-0.8, 0.8)),
        )
        battery_drift = -0.01 if state.vehicle_type == VehicleType.ELECTRIC_VEHICLE else -0.003
        state.battery_voltage = max(
            10.8,
            min(15.2, state.battery_voltage + battery_drift + self._random.uniform(-0.04, 0.04)),
        )
        fuel_drop = (state.speed / 250_000.0) * time_delta_seconds
        state.fuel_level = max(0.0, state.fuel_level - fuel_drop)
        state.fuel_consumption = max(0.0, fuel_drop * 100.0)
        distance_delta = state.speed * (time_delta_seconds / 3600.0)
        state.odometer += distance_delta
        state.heading = (state.heading + self._random.uniform(-8.0, 8.0)) % 360.0
        state.latitude, state.longitude = self._move_coordinates(
            state.latitude,
            state.longitude,
            state.heading,
            distance_delta,
        )
        state.gps_accuracy = max(0.5, min(25.0, state.gps_accuracy + self._random.uniform(-0.4, 0.4)))
        state.tire_pressure = max(20.0, min(50.0, state.tire_pressure + self._random.uniform(-0.1, 0.1)))
        state.outside_temperature = max(-20.0, min(55.0, state.outside_temperature + self._random.uniform(-0.2, 0.2)))
        state.humidity = max(0.0, min(100.0, state.humidity + self._random.uniform(-0.5, 0.5)))
        state.altitude = max(0.0, state.altitude + self._random.uniform(-1.5, 1.5))
        state.engine_status = "OFF" if state.speed < 0.5 and state.fuel_level < 1 else "ON"
        state.last_timestamp = timestamp

        return VehicleEvent(
            vehicle_id=state.vehicle_id,
            timestamp=timestamp.isoformat(),
            vehicle_type=state.vehicle_type.value,
            driver_id=state.driver_id,
            trip_id=state.trip_id,
            route_id=state.route_id,
            latitude=state.latitude,
            longitude=state.longitude,
            speed=state.speed,
            rpm=state.rpm,
            engine_temperature=state.engine_temperature,
            fuel_level=state.fuel_level,
            battery_voltage=state.battery_voltage,
            gear=state.gear,
            odometer=state.odometer,
            acceleration=speed_delta,
            brake_pressure=state.brake_pressure,
            gps_accuracy=state.gps_accuracy,
            tire_pressure=state.tire_pressure,
            outside_temperature=state.outside_temperature,
            humidity=state.humidity,
            fuel_consumption=state.fuel_consumption,
            engine_status=state.engine_status,
            heading=state.heading,
            altitude=state.altitude,
            metadata={"source": "vehicle_simulator"},
        )

    @staticmethod
    def _gear_from_speed(speed: float, vehicle_type: VehicleType) -> int:
        if vehicle_type == VehicleType.ELECTRIC_VEHICLE:
            return 1
        if speed < 5:
            return 1
        if speed < 20:
            return 2
        if speed < 40:
            return 3
        if speed < 60:
            return 4
        if speed < 90:
            return 5
        return 6

    @staticmethod
    def _move_coordinates(latitude: float, longitude: float, heading: float, distance_km: float) -> tuple[float, float]:
        if distance_km <= 0:
            return latitude, longitude

        earth_radius_km = 6371.0
        angular_distance = distance_km / earth_radius_km
        heading_rad = math.radians(heading)
        latitude_rad = math.radians(latitude)
        longitude_rad = math.radians(longitude)

        new_latitude = math.asin(
            math.sin(latitude_rad) * math.cos(angular_distance)
            + math.cos(latitude_rad) * math.sin(angular_distance) * math.cos(heading_rad)
        )
        new_longitude = longitude_rad + math.atan2(
            math.sin(heading_rad) * math.sin(angular_distance) * math.cos(latitude_rad),
            math.cos(angular_distance) - math.sin(latitude_rad) * math.sin(new_latitude),
        )

        return math.degrees(new_latitude), math.degrees(new_longitude)

    def generate_event(self, vehicle_index: int, timestamp: datetime | None = None) -> VehicleEvent:
        """Generate one event for the selected vehicle."""

        current_timestamp = timestamp or datetime.now(UTC)
        state = self._states[vehicle_index % self._vehicle_count]
        return self._advance_state(state, current_timestamp)

    def generate_batch(self, batch_size: int, timestamp: datetime | None = None) -> list[dict[str, object]]:
        """Generate a JSON-ready batch of telemetry events."""

        current_timestamp = timestamp or datetime.now(UTC)
        return [
            self.generate_event(vehicle_index=index, timestamp=current_timestamp).to_dict()
            for index in range(batch_size)
        ]

    def stream_events(self, batch_size: int, interval_seconds: float) -> Iterable[list[dict[str, object]]]:
        """Yield telemetry batches indefinitely for streaming workloads."""

        while True:
            yield self.generate_batch(batch_size=batch_size)
            if interval_seconds > 0:
                import time

                time.sleep(interval_seconds)

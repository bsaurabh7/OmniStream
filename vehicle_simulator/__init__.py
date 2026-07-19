"""Vehicle simulator package."""

from .generator import VehicleTelemetryGenerator, VehicleState
from .models import VehicleEvent, VehicleType
from .producer import EventHubTelemetryProducer

__all__ = [
    "EventHubTelemetryProducer",
    "VehicleEvent",
    "VehicleState",
    "VehicleTelemetryGenerator",
    "VehicleType",
]

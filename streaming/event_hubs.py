"""Utilities for consuming Azure Event Hubs from Spark."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EventHubsSettings:
    """Connection settings used by Databricks Structured Streaming."""

    connection_string: str
    event_hub_name: str
    consumer_group: str = "$Default"

    @property
    def spark_connection_string(self) -> str:
        """Return the Event Hubs connection string in Spark's expected format."""

        return self.connection_string


def build_event_hubs_conf(settings: EventHubsSettings) -> dict[str, str]:
    """Build the minimal Spark configuration dictionary for Event Hubs."""

    return {
        "eventhubs.connectionString": settings.spark_connection_string,
        "eventhubs.consumerGroup": settings.consumer_group,
        "eventhubs.eventHubName": settings.event_hub_name,
    }

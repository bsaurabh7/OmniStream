"""Azure Event Hubs producer for vehicle telemetry."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Iterable

try:
    from azure.eventhub import EventData, EventHubProducerClient
except ImportError:  # pragma: no cover - handled in environments without Azure SDK
    EventData = object  # type: ignore[assignment]
    EventHubProducerClient = object  # type: ignore[assignment]

from config.logging import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class ProducerConfig:
    """Configuration for Event Hubs publishing."""

    connection_string: str
    event_hub_name: str
    batch_size: int = 100
    retry_attempts: int = 3
    retry_delay_seconds: float = 1.5


class EventHubTelemetryProducer:
    """Publish telemetry batches to Azure Event Hubs with retry handling."""

    def __init__(self, config: ProducerConfig) -> None:
        self._config = config
        self._client = EventHubProducerClient.from_connection_string(
            conn_str=config.connection_string,
            eventhub_name=config.event_hub_name,
        )

    def close(self) -> None:
        """Close the underlying Event Hubs client."""

        self._client.close()

    def _send_batch_once(self, events: Iterable[dict[str, object]]) -> None:
        event_data_batch = self._client.create_batch()
        for event in events:
            payload = json.dumps(event).encode("utf-8")
            try:
                event_data_batch.add(EventData(payload))
            except ValueError:
                logger.info("Batch full, sending current batch before continuing")
                self._client.send_batch(event_data_batch)
                event_data_batch = self._client.create_batch()
                event_data_batch.add(EventData(payload))
        if len(event_data_batch) > 0:
            self._client.send_batch(event_data_batch)

    def send_events(self, events: Iterable[dict[str, object]]) -> None:
        """Send telemetry events with bounded retry attempts."""

        last_error: Exception | None = None
        for attempt in range(1, self._config.retry_attempts + 1):
            try:
                logger.info("Sending telemetry batch to Event Hubs", extra={"attempt": attempt})
                self._send_batch_once(events)
                return
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                logger.exception("Event Hubs publish failed on attempt %s", attempt)
                if attempt < self._config.retry_attempts:
                    import time

                    time.sleep(self._config.retry_delay_seconds)
        if last_error is not None:
            raise last_error

"""Streaming helpers for Azure Event Hubs ingestion."""

from .event_hubs import EventHubsSettings, build_event_hubs_conf

__all__ = ["EventHubsSettings", "build_event_hubs_conf"]

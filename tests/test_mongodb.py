"""Tests for MongoDB repository utilities."""

from __future__ import annotations

import mongomock

from mongodb.client import MongoConnectionManager
from mongodb.repository import AnomalyRepository


class MockConnectionManager(MongoConnectionManager):
    def __init__(self) -> None:
        self._mock_client = mongomock.MongoClient()
        super().__init__(uri="mongodb://localhost:27017")

    def client(self):  # type: ignore[override]
        return self._mock_client


def test_repository_insert_and_query() -> None:
    repository = AnomalyRepository(
        connection_manager=MockConnectionManager(),
        database_name="omnistream",
        collection_name="anomalies",
    )
    repository.ensure_indexes()
    inserted_id = repository.insert_anomaly(
        {
            "vehicle_id": "VH-000001",
            "timestamp": "2026-01-01T00:00:00Z",
            "anomaly_type": "engine_overheating",
        }
    )
    assert inserted_id
    records = repository.find_recent(limit=1)
    assert records[0]["vehicle_id"] == "VH-000001"

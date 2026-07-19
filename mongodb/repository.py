"""Repository utilities for anomaly events in MongoDB Atlas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config.logging import get_logger
from .client import MongoConnectionManager

logger = get_logger(__name__)


@dataclass(slots=True)
class AnomalyRepository:
    """Persist and retrieve anomaly events."""

    connection_manager: MongoConnectionManager
    database_name: str
    collection_name: str

    def _collection(self):
        client = self.connection_manager.client()
        database = client[self.database_name]
        return database[self.collection_name]

    def ensure_indexes(self) -> None:
        """Create the indexes used by dashboard and operational queries."""

        collection = self._collection()
        collection.create_index([("vehicle_id", 1), ("timestamp", -1)])
        collection.create_index([("anomaly_type", 1), ("timestamp", -1)])
        collection.create_index([("trip_id", 1)])
        logger.info("MongoDB indexes ensured")

    def insert_anomaly(self, document: dict[str, Any]) -> str:
        """Insert one anomaly record and return its string identifier."""

        collection = self._collection()
        result = collection.insert_one(document)
        logger.info("Stored anomaly event", extra={"inserted_id": str(result.inserted_id)})
        return str(result.inserted_id)

    def insert_many(self, documents: list[dict[str, Any]]) -> list[str]:
        """Insert a batch of anomaly documents."""

        if not documents:
            return []
        collection = self._collection()
        result = collection.insert_many(documents)
        identifiers = [str(inserted_id) for inserted_id in result.inserted_ids]
        logger.info("Stored anomaly batch", extra={"count": len(identifiers)})
        return identifiers

    def find_recent(self, limit: int = 25) -> list[dict[str, Any]]:
        """Fetch the most recent anomaly documents."""

        collection = self._collection()
        return list(collection.find().sort("timestamp", -1).limit(limit))

    def delete_by_vehicle(self, vehicle_id: str) -> int:
        """Delete anomaly records for a specific vehicle."""

        collection = self._collection()
        result = collection.delete_many({"vehicle_id": vehicle_id})
        logger.info("Deleted anomaly records for vehicle", extra={"vehicle_id": vehicle_id, "deleted": result.deleted_count})
        return result.deleted_count

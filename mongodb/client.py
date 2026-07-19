"""MongoDB connection helpers."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

try:
    from pymongo import MongoClient
except ImportError:  # pragma: no cover - optional in unit tests
    MongoClient = object  # type: ignore[assignment]

from config.logging import get_logger

logger = get_logger(__name__)


@dataclass(slots=True)
class MongoConnectionManager:
    """Manage a cached MongoDB client connection."""

    uri: str

    @lru_cache(maxsize=1)
    def client(self) -> MongoClient:
        """Create or return a cached MongoDB client."""

        logger.info("Creating MongoDB client")
        return MongoClient(self.uri)

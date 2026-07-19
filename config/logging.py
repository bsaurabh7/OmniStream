"""Logging helpers for OmniStream."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def configure_logging(log_dir: str | Path = "logs") -> None:
    """Configure console and rotating file logging for the project."""

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.handlers:
        root_logger.handlers.clear()

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    app_handler = RotatingFileHandler(
        log_path / "omnistream.log",
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    app_handler.setFormatter(formatter)

    error_handler = RotatingFileHandler(
        log_path / "errors.log",
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger for a project component."""

    return logging.getLogger(name)
